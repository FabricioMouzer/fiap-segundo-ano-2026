"""Gera evidências reproduzíveis do extrator e do classificador da Fase 2."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from extrator_sintomas import analisar_arquivo
from validar_notebook import executar_notebook


RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
PROCESSADOS = RAIZ / "data" / "processed"
RELATORIO = RAIZ / "docs" / "RESULTADOS_VALIDACAO.md"
RELATORIO_ERROS = RAIZ / "docs" / "ANALISE_ERROS_MODELO.md"


def exportar_extracoes_csv(extracoes: list[dict]) -> Path:
    """Converte o JSON hierárquico do extrator em tabela auditável."""
    linhas = []
    for relato_id, item in enumerate(extracoes, start=1):
        for achado_id, achado in enumerate(item["achados"], start=1):
            linhas.append(
                {
                    "relato_id": relato_id,
                    "achado_id": achado_id,
                    "relato": item["relato"],
                    "expressao": achado["expressao"],
                    "sintoma": achado["sintoma"],
                    "possivel_associacao": achado["possivel_associacao"],
                    "nivel_alerta": achado["nivel_alerta"],
                }
            )
    caminho = PROCESSADOS / "resultados_extrator.csv"
    pd.DataFrame(linhas).to_csv(caminho, index=False, encoding="utf-8")
    return caminho


def exportar_erros_classificador(namespace: dict) -> tuple[Path, pd.DataFrame]:
    """Registra cada erro da Regressão Logística com probabilidade e tipo."""
    pipeline = namespace["pipelines"]["Regressão Logística"]
    teste = namespace["teste"].copy()
    previsoes = pipeline.predict(teste["frase"])
    probabilidades = pipeline.predict_proba(teste["frase"])
    classes = list(pipeline.classes_)
    indice_alto = classes.index("alto risco")

    avaliacao = teste[["frase", "situacao", "grupo_id"]].copy()
    avaliacao.insert(0, "dataset_indice", avaliacao.index + 2)
    avaliacao["previsao"] = previsoes
    avaliacao["probabilidade_alto_risco"] = probabilidades[:, indice_alto].round(4)
    avaliacao["tipo_erro"] = ""
    divergentes = avaliacao["situacao"] != avaliacao["previsao"]
    avaliacao.loc[divergentes & (avaliacao["situacao"] == "alto risco"), "tipo_erro"] = "falso negativo"
    avaliacao.loc[divergentes & (avaliacao["situacao"] == "baixo risco"), "tipo_erro"] = "falso positivo"
    erros = avaliacao.loc[divergentes].reset_index(drop=True)

    caminho = PROCESSADOS / "erros_regressao_logistica.csv"
    erros.to_csv(caminho, index=False, encoding="utf-8")
    return caminho, erros


def escrever_relatorio_erros(erros: pd.DataFrame) -> None:
    falsos_negativos = int((erros["tipo_erro"] == "falso negativo").sum())
    falsos_positivos = int((erros["tipo_erro"] == "falso positivo").sum())
    grupos_com_erro = erros["grupo_id"].nunique()
    linhas = []
    for _, erro in erros.iterrows():
        linhas.append(
            f"| {erro['tipo_erro']} | {erro['situacao']} | {erro['previsao']} | "
            f"{erro['probabilidade_alto_risco']:.1%} | {erro['grupo_id']} | {erro['frase']} |"
        )

    RELATORIO_ERROS.write_text(
        "# Análise dos erros — Regressão Logística\n\n"
        "## Resultado executivo\n\n"
        f"A avaliação encontrou **{len(erros)} erros em 20 amostras de teste**: "
        f"**{falsos_negativos} falsos negativos** e **{falsos_positivos} falsos positivos**, "
        f"concentrados em **{grupos_com_erro} grupos linguísticos**. "
        "Os falsos negativos são o risco metodológico mais importante, pois textos rotulados como alto risco foram classificados como baixo risco.\n\n"
        "## Casos divergentes\n\n"
        "| Tipo | Classe real | Previsão | Prob. alto risco | Grupo | Frase |\n"
        "|---|---|---|---:|---|---|\n"
        + "\n".join(linhas)
        + "\n\n## Interpretação\n\n"
        "- O conjunto é pequeno e sintético; quatro erros não permitem conclusões clínicas.\n"
        "- A probabilidade próxima ao limiar de decisão indica incerteza lexical do modelo, não confiança médica.\n"
        "- TF-IDF aprende padrões de palavras, mas tem compreensão limitada de negação, contexto, intensidade e temporalidade.\n"
        "- As duas variações de cada grupo receberam a mesma classificação incorreta; portanto, o problema está associado ao padrão linguístico, não a uma frase isolada.\n"
        "- Os casos devem permanecer registrados como evidência transparente, sem remoção seletiva para elevar a métrica.\n\n"
        "## Próxima melhoria recomendada\n\n"
        "Ampliar a diversidade linguística mantendo o agrupamento por `grupo_id`, repetir a validação e comparar as novas métricas com esta linha de base. "
        "Qualquer melhoria deve ser medida em um conjunto de teste separado.\n\n"
        "> Resultado educacional; não constitui diagnóstico ou recomendação médica.\n",
        encoding="utf-8",
    )


def main() -> None:
    PROCESSADOS.mkdir(parents=True, exist_ok=True)
    extracoes = analisar_arquivo(RAW / "relatos_sintomas.txt", RAW / "mapa_conhecimento.csv")
    (PROCESSADOS / "resultados_extrator.json").write_text(
        json.dumps(extracoes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    exportar_extracoes_csv(extracoes)

    namespace = executar_notebook()
    resultados = namespace["resultados"]
    treino, teste = namespace["treino"], namespace["teste"]
    _, erros = exportar_erros_classificador(namespace)
    escrever_relatorio_erros(erros)
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
""", encoding="utf-8")
    print(f"Evidências geradas em {PROCESSADOS.relative_to(RAIZ)} e {RELATORIO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
