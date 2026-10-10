# Steering checklist

Roteiro para o `rules.md`. Passe por cada item e registre só o que se aplica à ferramenta. Cada regra numa linha, no imperativo, com o porquê quando ele não for óbvio.

## Segurança

- Quais operações gastam dinheiro (ativar campanha, aumentar orçamento, enviar mensagem paga)?
- Quais são irreversíveis (apagar, enviar e-mail ou WhatsApp, publicar, cobrar, arquivar sem restauração)?
- Qual é o default seguro de criação (pausado, rascunho, privado, test mode)?
- Existe dry-run, sandbox, modo test ou validação (`validate_only`, `dry_run`)? Como se usa?
- O que exige confirmação explícita do usuário antes de executar? Escreva como gate: "mostre X, Y e Z e espere um sim".

## Limites e mecânica

- Limite de taxa e como a API sinaliza (status 429, cabeçalhos, códigos de erro próprios).
- Paginação: tipo, tamanho máximo de página, como saber que acabou.
- Lotes: quantos itens por chamada, se o lote é atômico ou parcial.
- Tempo de propagação: o que demora para aparecer depois de criado (revisão de anúncio, indexação de busca).
- Versão da API em uso e data de expiração conhecida.

## Formatos que enganam

- Dinheiro: unidade (centavos, micros), moeda da conta.
- Datas: fuso da conta versus UTC, formato (ISO, epoch em segundos ou milissegundos).
- IDs: string ou número, prefixos (`act_`, `gid://`), IDs diferentes entre ambiente de teste e produção.
- Enums: valores aceitos e diferença entre rótulo exibido e valor na API.
- Campos que só aceitam escrita na criação, ou que a API ignora em silêncio.

## Convenções da conta

- Padrão de nomes (campanha, adset, lista, tarefa) com exemplo real anonimizado.
- Numeração sequencial e onde conferir o próximo número.
- Tags, pastas, responsáveis ou funis padrão.
- Quem é dono de quê: conta que não deve ser mexida, objetos gerenciados por automação.

## Quando parar e perguntar

- Conta, funil ou objeto ambíguo (mais de um candidato com o mesmo nome).
- Operação fora das que o mapa cobre.
- Resposta da API diferente do que o mapa diz (o mapa pode estar velho: sugira atualizar).
- Pedido que esbarra numa regra de segurança acima.

## Erros conhecidos

Para cada erro visto durante o mapeamento: mensagem ou código, causa e correção. Esta seção cresce com o uso; diga ao usuário que vale acrescentar erros novos quando aparecerem.
