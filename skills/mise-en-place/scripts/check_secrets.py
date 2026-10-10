#!/usr/bin/env python3
"""Scan a map written by the mise-en-place skill for secrets and personal data.

Usage: python3 check_secrets.py [--public] [--include-local] <folder-or-file> [...]
       python3 check_secrets.py --self-test

--public         also flag real IDs (act_123..., gid://..., numbers with 15+
                 digits) in files that will live in a public repo.
--include-local  also scan *.local.json and *.local.md, which by convention
                 hold the real IDs and stay out of git (skipped by default).

Exits with code 1 if anything is found. Placeholders such as <TOKEN>, $VAR
and values containing "example" are ignored. Names and addresses have no
reliable pattern: review them by hand.
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
        r"(?<![A-Za-z0-9_-])(?![A-Za-z_-]*(?:next|page|continuation|sync|cursor)[_-])(?:[A-Za-z]+[_-])*"
        r"(?:token|secret|password|passwd|api[_-]?key|client[_-]?secret)[\"']?\s*[:=]\s*[\"']?(?![<$\{])([A-Za-z0-9._~+/=-]{16,})",
        re.I,
    )),
    ("E-mail", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("Phone number", re.compile(r"(?<![\w-])\+\d{1,3}[\s-]?\(?\d{2,3}\)?[\s-]?\d{4,5}[\s-]?\d{4}\b")),
    ("Phone number (BR)", re.compile(r"(?<![\w+])\(\d{2}\)\s?9?\d{4}-?\d{4}\b")),
    ("Phone number (BR)", re.compile(r"(?<![\w+(])\d{2}\s9\d{4}-?\d{4}\b")),
    ("CPF", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b")),
    ("CNPJ", re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")),
]

# Digits-only values collide with numeric IDs, so they only count when the line has a label.
LABELED = [
    ("Phone number (digits)", re.compile(r"(?:tel|fone|phone|celular|whats|contato)", re.I),
     re.compile(r"\b(?:55)?\d{2}9?\d{8}\b")),
    ("CPF (digits)", re.compile(r"\bcpf\b", re.I), re.compile(r"\b\d{11}\b")),
    ("CNPJ (digits)", re.compile(r"\bcnpj\b", re.I), re.compile(r"\b\d{14}\b")),
]

PUBLIC_IDS = [
    ("Real ID (act_)", re.compile(r"\bact_\d{6,}")),
    ("Real ID (gid://)", re.compile(r"gid://[A-Za-z]+/[A-Za-z]+/\d+")),
    ("Real ID (15+ digits)", re.compile(r"(?<![\w.])\d{15,}(?![\w.])")),
]

ALLOWED_EMAIL = re.compile(r"(?:example\.(?:com|org|net)|users\.noreply\.github\.com|noreply@)", re.I)
HEX_TOKEN = re.compile(r"(?<![A-Za-z0-9_$<{-])[0-9a-fA-F]{32,}(?![A-Za-z0-9_>}-])")
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
HASH_CONTEXT = re.compile(r"(?:image_hash|hash|sha\d*|md5|checksum|etag)\W", re.I)
HIGH_ENTROPY = re.compile(r"(?<![A-Za-z0-9_$<{-])[A-Za-z0-9_+/=-]{32,}(?![A-Za-z0-9_>}-])")


def entropy(s: str) -> float:
    counts = {c: s.count(c) for c in set(s)}
    return -sum(n / len(s) * math.log2(n / len(s)) for n in counts.values())


def scan_line(line: str, public: bool = False):
    hits = []
    for label, context, pattern in LABELED:
        if context.search(line):
            hits += [(label, m.group(0)) for m in pattern.finditer(line)]
    if public:
        for label, pattern in PUBLIC_IDS:
            hits += [(label, m.group(0)) for m in pattern.finditer(line)]
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


def is_local(f: Path) -> bool:
    return ".local." in f.name


def iter_files(paths, include_local=False):
    for p in paths:
        path = Path(p)
        if path.is_file():
            yield path
        elif path.is_dir():
            for f in sorted(path.rglob("*")):
                if not f.is_file() or ".git" in f.parts or f.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                if is_local(f) and not include_local:
                    continue
                yield f


def redact(text: str) -> str:
    return text if len(text) <= 12 else f"{text[:6]}…{text[-4:]}"


SELF_TEST = [
    ('"access_token": "aB3dE5fG7hJ9kL1mN3pQ5r"', True),
    ("auth_token: aB3dE5fG7hJ9kL1mN3pQ5r", True),
    ("refresh_token=aB3dE5fG7hJ9kL1mN3pQ5r", True),
    ("token: abcdefghijklmnop1234", True),
    ("Authorization: Bearer abcDEF1234567890abcdefXYZ987", True),
    ("Telefone: 11 98765-4321", True),
    ("whatsapp 5511987654321", True),
    ("tel (11) 98765-4321", True),
    ("CPF 12345678901", True),
    ("cpf 123.456.789-09", True),
    ("joao.silva@gmail.com", True),
    ("Access-Token: 9f8e7d6c5b4a39281706f5e4d3c2b1a0aabbccdd", True),
    ("Authorization: Bearer $KOMMO_TOKEN", False),
    ('"access_token": "<TOKEN>"', False),
    ('"next_page_token": "Xk29fjaLq0Pz81mVn3TyBw7Rq2Ls"', False),
    ('"image_hash": "9f8e7d6c5b4a39281706f5e4d3c2b1a0"', False),
    ("id 3fa85f64-5717-4562-b3fc-2c963f66afa6", False),
    ("pipeline_id 12345678901", False),
    ("dev@example.com", False),
]


def self_test():
    failed = 0
    for line, expected in SELF_TEST:
        got = bool(scan_line(line))
        if got != expected:
            failed += 1
            print(f"FAILED: expected {'a finding' if expected else 'clean'}: {line}")
    if not scan_line("ad account act_1234567890", public=True):
        failed += 1
        print("FAILED: --public should flag act_1234567890")
    print("self-test ok" if not failed else f"{failed} case(s) failed")
    return 1 if failed else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    public = "--public" in argv
    include_local = "--include-local" in argv
    argv = [a for a in argv if not a.startswith("--")]
    if not argv:
        print(__doc__.strip())
        return 2
    found = 0
    for f in iter_files(argv, include_local):
        try:
            lines = f.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(lines, 1):
            for label, text in scan_line(line, public):
                found += 1
                print(f"{f}:{n}: {label}: {redact(text)}")
    if found:
        print(f"\n{found} finding(s). Replace them with a placeholder or an environment variable, or explain the false positive.")
        return 1
    print("Nothing found.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
