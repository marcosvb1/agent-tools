# plugins/

Um plugin (ou mod) por pasta. Cada um tem seu próprio `.claude-plugin/plugin.json`:

```
plugins/<nome>/
  .claude-plugin/plugin.json   # { "name", "version", "description" }
  skills/<skill>/SKILL.md      # opcional
  commands/  agents/  hooks/   # opcionais
```

Depois de criar, adicione uma entrada em `.claude-plugin/marketplace.json`:

```json
{ "name": "<nome>", "source": "./plugins/<nome>", "description": "..." }
```
