#!/usr/bin/env python3
"""Procura segredos e dados pessoais num mapa gerado pela skill mise-en-place.

Uso: python3 check_secrets.py <pasta-ou-arquivo> [...]

Sai com código 1 se encontrar algo. Placeholders como <TOKEN>, $VAR e
exemplos com "example" são ignorados.
"""

import math
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".txt", ".csv", ".env", ".toml", ".ini", ""}

PATTERNS = [
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("Bearer token", re.compile(r"Bearer\s+(?![<$\{])[A-Za-z0-9._~+/=-]{20,}")),
    ("Meta access token", re.compile(r"\bEAA[A-Za-z0-9]{30,}")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})")),
    ("Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("Stripe key", re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}")),
    ("Anthropic/OpenAI key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_-]{20,}")),
    ("Shopify token", re.compile(r"\bshp(?:at|ss|ca|pa)_[A-Fa-f0-9]{20,}")),
    ("Notion token", re.compile(r"\b(?:ntn_|secret_)[A-Za-z0-9]{30,}")),
    ("HubSpot private app token", re.compile(r"\bpat-(?:na|eu|ap)\d-[0-9a-f-]{30,}")),
    ("ClickUp token", re.compile(r"\bpk_\d+_[A-Z0-9]{20,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("Private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Credential in URL", re.compile(r"https?://[^\s/:@]+:[^\s/@]+@")),
    ("Token in query string", re.compile(r"[?&](?:access_token|api_key|apikey|token|key|secret)=(?![<$\{])[^\s&\"']{12,}", re.I)),
    ("Secret assignment", re.compile(
        r"(?<![A-Za-z_])(?<!page_)(?<!next_)(?<!continuation_)(?:token|secret|password|passwd|api[_-]?key|client[_-]?secret)\"?\s*[:=]\s*\"?(?![<$\{])([A-Za-z0-9._~+/=-]{16,})",
        re.I,
    )),
    ("E-mail", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("Phone number", re.compile(r"(?<![\w-])\+\d{1,3}[\s-]?\(?\d{2,3}\)?[\s-]?\d{4,5}[\s-]?\d{4}\b")),
    ("Phone number (BR)", re.compile(r"(?<![\w+])\(\d{2}\)\s?9?\d{4}-?\d{4}\b")),
    ("CPF", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
    ("CNPJ", re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")),
]

ALLOWED_EMAIL = re.compile(r"(?:example\.(?:com|org|net)|users\.noreply\.github\.com|noreply@)", re.I)
HEX_TOKEN = re.compile(r"(?<![A-Za-z0-9_$<{-])[0-9a-fA-F]{32,}(?![A-Za-z0-9_>}-])")
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
HASH_CONTEXT = re.compile(r"(?:image_hash|hash|sha\d*|md5|checksum|etag)\W", re.I)
HIGH_ENTROPY = re.compile(r"(?<![A-Za-z0-9_$<{-])[A-Za-z0-9_+/=-]{32,}(?![A-Za-z0-9_>}-])")


def entropy(s: str) -> float:
    counts = {c: s.count(c) for c in set(s)}
    return -sum(n / len(s) * math.log2(n / len(s)) for n in counts.values())


def scan_line(line: str):
    hits = []
    for label, pattern in PATTERNS:
        for m in pattern.finditer(line):
            text = m.group(0)
            if label == "E-mail" and ALLOWED_EMAIL.search(text):
                continue
            if "example" in text.lower() or "exemplo" in text.lower():
                continue
            hits.append((label, text))
    covered = " ".join(t for _, t in hits)
    if not HASH_CONTEXT.search(line):
        for m in HEX_TOKEN.finditer(line):
            text = m.group(0)
            if text in covered or text.isdigit() or UUID.match(text):
                continue
            if entropy(text) > 3.5:
                hits.append(("Hex token", text))
                covered += " " + text
    for m in HIGH_ENTROPY.finditer(line):
        text = m.group(0)
        if text in covered or text.isdigit():
            continue
        has_mix = any(c.isdigit() for c in text) and any(c.isalpha() for c in text)
        if has_mix and entropy(text) > 4.0:
            hits.append(("High-entropy string", text))
    return hits


def iter_files(paths):
    for p in paths:
        path = Path(p)
        if path.is_file():
            yield path
        elif path.is_dir():
            for f in sorted(path.rglob("*")):
                if f.is_file() and f.suffix.lower() in TEXT_SUFFIXES and ".git" not in f.parts:
                    yield f


def redact(text: str) -> str:
    return text if len(text) <= 12 else f"{text[:6]}…{text[-4:]}"


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    found = 0
    for f in iter_files(argv):
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            for label, text in scan_line(line):
                found += 1
                print(f"{f}:{n}: {label}: {redact(text)}")
    if found:
        print(f"\n{found} ocorrência(s). Troque por placeholder ou variável de ambiente, ou justifique o falso positivo.")
        return 1
    print("Nada encontrado.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
