# Evidências de validação do pipeline

## Resultado executivo

O pipeline foi executado de ponta a ponta com **80 relatos sintéticos**, sendo 60 para treino e 20 para teste. A separação por `grupo_id` foi preservada, sem colocar variações da mesma frase nos dois conjuntos.

| Modelo | Acurácia | Precisão — alto risco | Recall — alto risco | F1 — alto risco |
|---|---:|---:|---:|---:|
| Regressão Logística | 80.0% | 80.0% | 80.0% | 80.0% |
| Árvore de Decisão | 30.0% | 25.0% | 20.0% | 22.2% |

## Interpretação

A **Regressão Logística** apresentou o melhor equilíbrio e é o modelo recomendado para a demonstração acadêmica. No conjunto de teste, identificou 8 de 10 relatos de alto risco. Os dois falsos negativos reforçam que o protótipo não pode ser usado para decisão clínica.

A Árvore de Decisão apresentou desempenho baixo nesta base textual pequena. O resultado foi mantido como comparação transparente, não como falha a ocultar.

## Evidências geradas

- `data/processed/resultados_extrator.json`: achados dos 10 relatos;
- `data/processed/resultados_extrator.csv`: achados em formato tabular;
- `data/processed/metricas_modelos.json`: métricas e matrizes de confusão;
- `data/processed/erros_regressao_logistica.csv`: quatro previsões divergentes;
- `docs/ANALISE_ERROS_MODELO.md`: interpretação rastreável dos erros;
- `notebooks/classificador_risco_tfidf.ipynb`: método, treinamento, avaliação e análise crítica;
- `tests/`: verificações automáticas dos dados e do extrator.

## Como reproduzir

```bash
python src/gerar_dados.py
python -m unittest discover -s tests -v
python src/gerar_evidencias.py
```

## Limitações

Os dados são sintéticos, pequenos e construídos com padrões linguísticos controlados. As métricas não demonstram validade clínica nem capacidade de generalização. Uma solução real exigiria dados representativos, validação externa, supervisão médica e avaliação ética e regulatória.
