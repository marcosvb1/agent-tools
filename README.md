# agent-tools

Este repositório é dedicado ao desenvolvimento de skills e plugins para o Claude em geral: ferramentas, fluxos e extensões reutilizáveis que ampliam o que o Claude consegue fazer em diferentes projetos.

Ele funciona como um marketplace de plugins do Claude Code.

## Estrutura

- `.claude-plugin/marketplace.json`: catálogo do marketplace. Todo plugin, mod ou pacote de skills precisa estar listado aqui.
- `plugins/`: plugins e mods, uma pasta por plugin (veja [plugins/README.md](plugins/README.md)).
- `skills/`: skills avulsas, uma pasta por skill (veja [skills/README.md](skills/README.md)).

## Instalação

```bash
/plugin marketplace add marcosvb1/agent-tools
/plugin install <plugin>@agent-tools
```

Por projeto: `claude plugin install <plugin>@agent-tools --scope project`.
