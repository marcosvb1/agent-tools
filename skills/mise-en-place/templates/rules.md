# <Ferramenta>: regras de uso

> Steering para qualquer sessão que opere <Ferramenta>. Atualizado em AAAA-MM-DD.

## Antes de agir

- Leia [README.md](README.md) e confirme a conta com o usuário quando houver mais de uma.
- <Outra pré-condição.>

## Segurança

- <Crie sempre <pausado/rascunho>; ativar gasta dinheiro e exige confirmação explícita.>
- <Mostre <conta, valor, público, link> e espere um sim antes de <operação irreversível>.>
- Nunca grave credenciais em arquivo; use `$<FERRAMENTA>_TOKEN`.

## Limites e mecânica

- <Limite de taxa: <n> req/s; em 429 espere `Retry-After`.>
- <Paginação por <cursor/offset>, máximo <n> por página.>

## Formatos

- <Valores em <centavos/micros> da moeda da conta.>
- <Datas no fuso da conta.>

## Convenções da conta

- <Padrão de nome: `<PADRÃO>`; exemplo: `<EXEMPLO ANONIMIZADO>`.>

## Pare e pergunte quando

- <Conta, funil ou objeto ambíguo.>
- <A resposta da API não bater com o mapa (sugira atualizar o mapa).>

## Erros conhecidos

| Erro | Causa | Correção |
| --- | --- | --- |
| `<código>` | <causa> | <correção> |
