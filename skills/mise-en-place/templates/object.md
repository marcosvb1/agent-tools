# <Objeto> (<Ferramenta>)

> Atualizado em AAAA-MM-DD. Schema lido de `<endpoint ou tool de metadados>`.

<Uma frase: o que é este objeto no negócio do usuário.>

## Propriedades

| Nome na API | Rótulo | Tipo | Obrig. | Só leitura | Notas | Origem |
| --- | --- | --- | --- | --- | --- | --- |
| `<name>` | <Nome> | string | sim | não | | verificado AAAA-MM-DD |
| `<price>` | <Valor> | integer | não | não | centavos | docs |
| `<custom_field_123>` | <Origem do lead> | enum | não | não | opções abaixo | verificado AAAA-MM-DD |

## Opções de enum

### `<custom_field_123>` — <Origem do lead>

| Rótulo | ID / valor |
| --- | --- |
| <Instagram> | `<ENUM_ID>` |

## Estágios / status

| Funil / grupo | Estágio | ID |
| --- | --- | --- |
| <Vendas> | <Qualificado> | `<STATUS_ID>` |

## Relações

- <Pertence a> `<outro objeto>` via `<campo>`.
- <Tem muitos> `<outro objeto>`; buscar com `<endpoint ou tool>`.

## Exemplo (anonimizado)

```json
{
  "id": "<ID>",
  "name": "<NOME>"
}
```
