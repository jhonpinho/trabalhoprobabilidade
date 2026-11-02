# Máquina Estatística – Trabalho I (Probabilidade e Estatística I, IFES Serra, 2026/2)

**Integrantes:** Jhon Pinho e Marlon Silva (dupla)

## Como executar
```
python simulador.py                # exibe uma rodada, executa E1–E5 e extras; gera ./resultados
python -m unittest testes -v       # 6 verificações automatizadas
python gerar_relatorio.py          # (opcional) recompõe o relatório PDF
```
Requisitos: Python 3 com `matplotlib` (e `reportlab` apenas para o relatório). O sorteio usa só a biblioteca padrão
(`random.Random(semente).randrange(5)`), com a semente iniciada **uma vez** por experimento.

## Sementes
E1/E2/E4/E5: 2026 (E2 também 10 e 123456) · E3: 42 · Extras: 1000–1029 (IC), 43 (mesma média), 77 (exposição).

## Onde estão os resultados (`resultados/`)
`e1_distribuicao.csv`, `e1_rodadas.csv`, `e2_medias_acumuladas.csv`, `e3_participantes.csv`, `e3_resumo.csv`,
`e4_condicional.csv`, `e5_comparacao.csv`, `extra_ic.csv`, `extra_mesma_media.csv`, `extra_exposicao.csv`,
`extra_sensibilidade.csv`, gráficos `fig_*.png`, `resultados.json` e `ambiente.txt` (versão e gerador usados).

## Extras feitos
Intervalos de confiança, mesma média/riscos diferentes, limites de exposição, análise de sensibilidade, validação automatizada.

## Declaração de uso de IA
Usamos o assistente Claude (Anthropic) para estruturar e escrever o simulador, os testes, os gráficos e o rascunho do relatório,
e para pesquisar notícias sobre a MP 1.394/2026. O grupo deve conferir: contas teóricas (E[X] = −0,16; RTP 84% e 92,4%),
execução em Python 3.14 (os números gerados aqui usaram Python 3.12; reexecutar e comparar), fontes citadas e a
correspondência entre relatório e arquivos. Ambos os integrantes devem compreender o conteúdo entregue.
