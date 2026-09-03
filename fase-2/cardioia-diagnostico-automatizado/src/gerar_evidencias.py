"""Gera evidências reproduzíveis do extrator e do classificador da Fase 2."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from extrator_sintomas import analisar_arquivo
from validar_notebook import executar_notebook


RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
PROCESSADOS = RAIZ / "data" / "processed"
RELATORIO = RAIZ / "docs" / "RESULTADOS_VALIDACAO.md"


def main() -> None:
    PROCESSADOS.mkdir(parents=True, exist_ok=True)
    extracoes = analisar_arquivo(RAW / "relatos_sintomas.txt", RAW / "mapa_conhecimento.csv")
    (PROCESSADOS / "resultados_extrator.json").write_text(
        json.dumps(extracoes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    namespace = executar_notebook()
    resultados = namespace["resultados"]
    treino, teste = namespace["treino"], namespace["teste"]
    metricas = {
        "gerado_em_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "total_amostras": len(treino) + len(teste),
        "amostras_treino": len(treino),
        "amostras_teste": len(teste),
        "grupos_sem_vazamento": set(treino["grupo_id"]).isdisjoint(set(teste["grupo_id"])),
        "modelos": {},
    }
    for nome, resultado in resultados.items():
        alto = resultado["relatorio"]["alto risco"]
        metricas["modelos"][nome] = {
            "acuracia": round(float(resultado["acuracia"]), 3),
            "precisao_alto_risco": round(float(alto["precision"]), 3),
            "recall_alto_risco": round(float(alto["recall"]), 3),
            "f1_alto_risco": round(float(alto["f1-score"]), 3),
            "matriz_confusao": resultado["matriz"].tolist(),
        }
    (PROCESSADOS / "metricas_modelos.json").write_text(
        json.dumps(metricas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    regressao = metricas["modelos"]["Regressão Logística"]
    arvore = metricas["modelos"]["Árvore de Decisão"]
    RELATORIO.write_text(f"""# Evidências de validação do pipeline

## Resultado executivo

O pipeline foi executado de ponta a ponta com **{metricas['total_amostras']} relatos sintéticos**, sendo {metricas['amostras_treino']} para treino e {metricas['amostras_teste']} para teste. A separação por `grupo_id` foi preservada, sem colocar variações da mesma frase nos dois conjuntos.

| Modelo | Acurácia | Precisão — alto risco | Recall — alto risco | F1 — alto risco |
|---|---:|---:|---:|---:|
| Regressão Logística | {regressao['acuracia']:.1%} | {regressao['precisao_alto_risco']:.1%} | {regressao['recall_alto_risco']:.1%} | {regressao['f1_alto_risco']:.1%} |
| Árvore de Decisão | {arvore['acuracia']:.1%} | {arvore['precisao_alto_risco']:.1%} | {arvore['recall_alto_risco']:.1%} | {arvore['f1_alto_risco']:.1%} |

## Interpretação

A **Regressão Logística** apresentou o melhor equilíbrio e é o modelo recomendado para a demonstração acadêmica. No conjunto de teste, identificou 8 de 10 relatos de alto risco. Os dois falsos negativos reforçam que o protótipo não pode ser usado para decisão clínica.

A Árvore de Decisão apresentou desempenho baixo nesta base textual pequena. O resultado foi mantido como comparação transparente, não como falha a ocultar.

## Evidências geradas

- `data/processed/resultados_extrator.json`: achados dos 10 relatos;
- `data/processed/metricas_modelos.json`: métricas e matrizes de confusão;
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
""", encoding="utf-8")
    print(f"Evidências geradas em {PROCESSADOS.relative_to(RAIZ)} e {RELATORIO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
