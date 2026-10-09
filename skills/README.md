# skills/

Skills avulsas, uma pasta por skill:

```
skills/<nome>/
  SKILL.md        # frontmatter com name e description
  references/     # opcional, carregado sob demanda
  scripts/        # opcional
```

Regras para uma skill "universal" (funciona no Claude Code, no claude.ai e no Cowork):

- Nada de dado pessoal ou de cliente fixo no texto: IDs de conta, URLs, nomes de empresa e paletas de marca viram parâmetros, perguntas ao usuário ou um arquivo de configuração de exemplo.
- Credenciais só por variável de ambiente ou conector, nunca no arquivo.
- Caminhos relativos à própria skill, sem depender de uma pasta específica da máquina.
- Se a skill depende de uma ferramenta (MCP, CLI), diga qual e o que fazer quando ela não existir.

Para instalar pelo marketplace, a skill entra numa entrada do `.claude-plugin/marketplace.json` que aponta para a raiz e lista as skills:

```json
{
  "name": "<pacote>",
  "source": "./",
  "strict": false,
  "description": "...",
  "skills": ["./skills/<nome>"]
}
```
