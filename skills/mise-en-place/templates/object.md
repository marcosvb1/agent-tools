# <Object> (<Tool>)

> Updated YYYY-MM-DD. Schema read from `<metadata endpoint or tool>`.

<One sentence: what this object is in the user's business.>

## Properties

| API name | Label | Type | Required | Read-only | Notes | Source |
| --- | --- | --- | --- | --- | --- | --- |
| `<name>` | <Name> | string | yes | no | | verified YYYY-MM-DD |
| `<price>` | <Value> | integer | no | no | cents | docs |
| `<custom_field_123>` | <Lead source> | enum | no | no | options below | verified YYYY-MM-DD |

## Enum options

### `<custom_field_123>` — <Lead source>

| Label | ID / value |
| --- | --- |
| <Instagram> | `<ENUM_ID>` |

## Stages / statuses

| Pipeline / group | Stage | ID |
| --- | --- | --- |
| <Sales> | <Qualified> | `<STATUS_ID>` |

## Relations

- <Belongs to> `<other object>` via `<field>`.
- <Has many> `<other object>`; fetch with `<endpoint or tool>`.

## Example (anonymized)

```json
{
  "id": "<ID>",
  "name": "<NAME>"
}
```
