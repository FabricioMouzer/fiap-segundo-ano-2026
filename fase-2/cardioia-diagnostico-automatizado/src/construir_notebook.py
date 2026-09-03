"""Constrói o notebook reproduzível de classificação de risco."""

import json
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
SAIDA = RAIZ / "notebooks" / "classificador_risco_tfidf.ipynb"


def codigo(texto: str) -> dict:
    linhas = [linha + "\n" for linha in texto.strip().splitlines()]
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": linhas}


def markdown(texto: str) -> dict:
    linhas = [linha + "\n" for linha in texto.strip().splitlines()]
    return {"cell_type": "markdown", "metadata": {}, "source": linhas}


nb = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"},
    },
}
nb["cells"] = [
    markdown("""
# CardioIA — Classificador de risco textual com TF-IDF

## tl;dr

Este notebook treina e compara Regressão Logística e Árvore de Decisão sobre relatos sintéticos rotulados como **baixo risco** ou **alto risco**. O objetivo é reproduzir uma triagem acadêmica, sem validade clínica.
"""),
    markdown("""
## Contexto e métodos

O texto é transformado por TF-IDF dentro de um pipeline, evitando ajustar o vetorizador com os dados de teste. A divisão é estratificada e determinística.

### Premissas principais

- todos os dados são sintéticos;
- as classes foram balanceadas;
- as métricas descrevem apenas esta pequena base acadêmica;
- falsos negativos de alto risco merecem atenção especial.
"""),
    codigo("""
from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

SEMENTE = 42
RAIZ = Path.cwd()
if not (RAIZ / "data").exists():
    RAIZ = Path.cwd().parent
DATASET = RAIZ / "data" / "raw" / "dataset_risco.csv"
"""),
    markdown("## Dados"),
    codigo("""
dados = pd.read_csv(DATASET)
assert list(dados.columns) == ["frase", "situacao", "grupo_id"]
assert dados["frase"].notna().all()
assert dados["situacao"].isin(["baixo risco", "alto risco"]).all()
assert not dados["frase"].duplicated().any()
print(f"Linhas: {len(dados)}")
print(dados["situacao"].value_counts())
dados.head()
"""),
    codigo("""
divisor = StratifiedGroupKFold(n_splits=4, shuffle=True, random_state=SEMENTE)
indices_treino, indices_teste = next(
    divisor.split(dados["frase"], dados["situacao"], groups=dados["grupo_id"])
)
treino = dados.iloc[indices_treino]
teste = dados.iloc[indices_teste]
X_treino, y_treino = treino["frase"], treino["situacao"]
X_teste, y_teste = teste["frase"], teste["situacao"]
assert set(treino["grupo_id"]).isdisjoint(set(teste["grupo_id"]))
print(f"Treino: {len(X_treino)} | Teste: {len(X_teste)}")
"""),
    markdown("## Resultados"),
    codigo("""
modelos = {
    "Regressão Logística": LogisticRegression(max_iter=1000, random_state=SEMENTE),
    "Árvore de Decisão": DecisionTreeClassifier(max_depth=6, random_state=SEMENTE),
}

resultados = {}
pipelines = {}
for nome, modelo in modelos.items():
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
        ("modelo", modelo),
    ])
    pipeline.fit(X_treino, y_treino)
    previsoes = pipeline.predict(X_teste)
    resultados[nome] = {
        "acuracia": accuracy_score(y_teste, previsoes),
        "relatorio": classification_report(y_teste, previsoes, output_dict=True, zero_division=0),
        "matriz": confusion_matrix(y_teste, previsoes, labels=["baixo risco", "alto risco"]),
    }
    pipelines[nome] = pipeline

pd.DataFrame({nome: {"acuracia": item["acuracia"]} for nome, item in resultados.items()}).T
"""),
    codigo("""
for nome, item in resultados.items():
    print(f"\\n{nome} — acurácia: {item['acuracia']:.3f}")
    print(pd.DataFrame(item["relatorio"]).T.round(3))
"""),
    codigo("""
fig, eixos = plt.subplots(1, 2, figsize=(11, 4))
for eixo, (nome, item) in zip(eixos, resultados.items()):
    sns.heatmap(item["matriz"], annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=["baixo risco", "alto risco"],
                yticklabels=["baixo risco", "alto risco"], ax=eixo)
    eixo.set_title(nome)
    eixo.set_xlabel("Previsto")
    eixo.set_ylabel("Real")
plt.tight_layout()
plt.show()
"""),
    markdown("### Testes com frases inéditas"),
    codigo("""
modelo_escolhido = max(resultados, key=lambda nome: resultados[nome]["relatorio"]["alto risco"]["recall"])
pipeline_final = pipelines[modelo_escolhido]
frases_ineditas = [
    "Estou com aperto forte no peito, suor frio e dificuldade para respirar.",
    "Senti tensão leve no ombro depois da academia e consigo trabalhar normalmente.",
    "Minha fala ficou enrolada e perdi a força de um lado do corpo.",
    "Não sinto dor no peito, apenas desconforto muscular ao mover o braço.",
]
pd.DataFrame({"frase": frases_ineditas, "previsao": pipeline_final.predict(frases_ineditas)})
"""),
    markdown("""
## Conclusões e limitações

- A comparação considera o **recall de alto risco**, não apenas a acurácia.
- A base é pequena, sintética e contém padrões construídos; o desempenho não pode ser generalizado para pacientes reais.
- TF-IDF não interpreta adequadamente contexto, negação, intensidade ou temporalidade em todos os casos.
- Uma aplicação real exigiria dados clínicos representativos, validação externa, supervisão médica, governança e avaliação regulatória.

> **Aviso:** resultado educacional; não constitui diagnóstico médico.
"""),
]

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(SAIDA)
