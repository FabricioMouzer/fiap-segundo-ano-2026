"""Reutiliza ativos da Fase 1 em exploração de dados e NLP, sem treinar modelos.

Mantém os rótulos sintéticos originais e separa esta auditoria do experimento
de classificação das 80 frases da Fase 2. Usa somente a biblioteca padrão.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
REPOSITORIO = RAIZ.parents[1]
FASE1 = REPOSITORIO / "fase-1" / "cardioia-batimentos-de-dados"
CSV_FASE1 = FASE1 / "data" / "numericos" / "cardioia_pacientes_sinteticos.csv"
TEXTOS = (
    FASE1 / "assets" / "textos" / "texto_01_disturbances_of_the_heart_contexto.txt",
    FASE1 / "assets" / "textos" / "texto_02_lettsomian_lectures_contexto.txt",
)
ROTULO_MAIOR = "higher_simulated_risk"
ROTULO_MENOR = "lower_simulated_risk"
PALAVRAS_FUNCIONAIS = frozenset("""
a ao aos as ate com como da das de do dos e ela elas ele eles em entre era
essa essas esse esses esta estas este estes ha isso mais mas na nas no nos
o os ou para pela pelas pelo pelos por qual quais que se sem ser seu seus
sua suas sobre tambem um uma umas uns sao e foram foi pode podem permite
""".split())


def identificar_fonte(caminho: Path) -> dict:
    conteudo = caminho.read_bytes()
    return {
        "caminho": caminho.relative_to(REPOSITORIO).as_posix(),
        "sha256": hashlib.sha256(conteudo).hexdigest(),
        "bytes": len(conteudo),
    }


def faixa_etaria(idade: int) -> str:
    """Faixas descritivas do projeto, sem significado clínico atribuído."""
    return "menos de 45" if idade < 45 else ("45 a 59" if idade < 60 else "60 ou mais")


def analisar_texto(caminho: Path) -> dict:
    texto = caminho.read_text(encoding="utf-8")
    # Exclui cabeçalho, links, perguntas propostas e limitações da contagem.
    # Os arquivos são resumos contextuais autorais, não as obras integrais.
    if "\nCONTEXTO\n" not in texto or "\nPERGUNTAS DE NLP\n" not in texto:
        raise ValueError(f"Seções esperadas ausentes em {caminho.name}")
    contexto = texto.split("\nCONTEXTO\n", 1)[1].split("\nPERGUNTAS DE NLP\n", 1)[0].strip()
    normalizado = "".join(
        char for char in unicodedata.normalize("NFKD", contexto.casefold())
        if not unicodedata.combining(char)
    )
    tokens = re.findall(r"[a-z]+", normalizado)
    termos = Counter(t for t in tokens if len(t) >= 3 and t not in PALAVRAS_FUNCIONAIS)
    frequencias = [
        {"termo": termo, "ocorrencias": ocorrencias}
        for termo, ocorrencias in sorted(termos.items(), key=lambda item: (-item[1], item[0]))
    ]
    return {
        "fonte": identificar_fonte(caminho),
        "natureza": "resumo contextual autoral em português sobre obra histórica",
        "secao_analisada": "CONTEXTO",
        "tokens_antes_filtragem": len(tokens),
        "tokens_apos_filtragem": sum(termos.values()),
        "termos_distintos": len(termos),
        "frequencias": frequencias,
    }


def auditar() -> dict:
    """Lê fontes versionadas e retorna evidência determinística sem gravá-las."""
    with CSV_FASE1.open(encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        colunas = list(leitor.fieldnames or [])
        dados = list(leitor)
    if not dados:
        raise ValueError("O CSV da Fase 1 está vazio")
    rotulos = Counter(linha["cardio_risk_label_synthetic"] for linha in dados)
    if set(rotulos) != {ROTULO_MAIOR, ROTULO_MENOR}:
        raise ValueError("Rótulos da Fase 1 foram alterados; revisar a auditoria")

    subgrupos = []
    dimensoes = {
        "sex_at_birth": lambda linha: linha["sex_at_birth"],
        "faixa_etaria": lambda linha: faixa_etaria(int(linha["age_years"])),
    }
    for dimensao, chave in dimensoes.items():
        grupos = sorted({chave(linha) for linha in dados})
        for grupo in grupos:
            registros = [linha for linha in dados if chave(linha) == grupo]
            maior = sum(linha["cardio_risk_label_synthetic"] == ROTULO_MAIOR for linha in registros)
            subgrupos.append({
                "dimensao": dimensao,
                "grupo": grupo,
                "registros": len(registros),
                ROTULO_MAIOR: maior,
                ROTULO_MENOR: len(registros) - maior,
                "proporcao_rotulo_maior": round(maior / len(registros), 6),
            })

    textos = [analisar_texto(caminho) for caminho in TEXTOS]
    vocabularios = [{item["termo"] for item in texto["frequencias"]} for texto in textos]
    return {
        "versao_auditoria": 1,
        "finalidade": "continuidade, representação dos dados e exploração lexical; sem treinamento",
        "fonte_tabular": identificar_fonte(CSV_FASE1),
        "fonte_regra_simulacao": identificar_fonte(FASE1 / "scripts" / "gerar_dataset_sintetico.py"),
        "tabela": {
            "registros": len(dados),
            "colunas": colunas,
            "identificadores_unicos": len({linha["patient_id_synthetic"] for linha in dados}),
            "celulas_vazias": sum(valor in (None, "") for linha in dados for valor in linha.values()),
            "rotulos_originais": dict(sorted(rotulos.items())),
            "idade_minima": min(int(linha["age_years"]) for linha in dados),
            "idade_maxima": max(int(linha["age_years"]) for linha in dados),
            "proporcao_classe_majoritaria": max(rotulos.values()) / len(dados),
        },
        "subgrupos": subgrupos,
        "nlp": {
            "metodo": "seção CONTEXTO; minúsculas; remoção de acentos; tokens alfabéticos; mínimo 3 letras; palavras funcionais excluídas",
            "palavras_funcionais_excluidas": sorted(PALAVRAS_FUNCIONAIS),
            "textos": textos,
            "termos_comuns": sorted(set.intersection(*vocabularios)),
        },
        "experimento_classificacao_fase2": {
            "fonte": identificar_fonte(RAIZ / "data" / "raw" / "dataset_risco.csv"),
            "origem": "frases elaboradas separadamente em src/gerar_dados.py",
            "derivado_do_csv_fase1": False,
            "treinado_nesta_auditoria": False,
            "observacao": "Os rótulos alto risco/baixo risco das frases não equivalem aos rótulos originais da Fase 1.",
        },
    }


def gerar_documentacao(auditoria: dict) -> str:
    tabela = auditoria["tabela"]
    contagens = tabela["rotulos_originais"]
    linhas_subgrupos = "\n".join(
        f"| {s['dimensao']} | {s['grupo']} | {s['registros']} | {s[ROTULO_MAIOR]} | "
        f"{s[ROTULO_MENOR]} | {s['proporcao_rotulo_maior']:.1%} |"
        for s in auditoria["subgrupos"]
    )
    linhas_textos = "\n".join(
        f"| {Path(t['fonte']['caminho']).name} | {t['tokens_apos_filtragem']} | "
        f"{t['termos_distintos']} | "
        + ", ".join(f"{item['termo']} ({item['ocorrencias']})" for item in t['frequencias'][:5]) + " |"
        for t in auditoria["nlp"]["textos"]
    )
    fontes = [auditoria["fonte_tabular"], auditoria["fonte_regra_simulacao"]]
    fontes += [t["fonte"] for t in auditoria["nlp"]["textos"]]
    fontes.append(auditoria["experimento_classificacao_fase2"]["fonte"])
    linhas_fontes = "\n".join(f"| `{f['caminho']}` | `{f['sha256']}` |" for f in fontes)
    return f"""# Continuidade verificável entre a Fase 1 e a Fase 2

Esta auditoria executa leitura e análise de ativos da Fase 1. Antes desta ponte,
o pipeline da Fase 2 utilizava dados criados na própria Fase 2; a continuidade
era temática, organizacional e de governança. O classificador principal continua
usando seu conjunto independente de 80 frases sintéticas.

## O que foi efetivamente aproveitado

| Ativo da Fase 1 | Uso executado nesta Fase 2 | Limite |
|---|---|---|
| CSV de pacientes sintéticos | leitura dos {tabela['registros']} registros e {len(tabela['colunas'])} colunas; representação por sexo, idade e rótulo original | não treina o classificador das 80 frases |
| Dois TXT de contexto histórico | normalização, tokenização e frequência de termos na seção CONTEXTO | resumos autorais em português; não são relatos de pacientes ou obras integrais |
| Script gerador do CSV | identificação por hash e análise documentada das regras de simulação | nenhum dado é regenerado ou rótulo alterado |
| Governança e dicionário | continuidade da finalidade acadêmica, categorias documentadas e rastreabilidade | governança não demonstra validade clínica |
| Dois PDFs em assets/textos | permanecem disponíveis como referências do projeto | não são lidos por esta auditoria nem usados no treinamento |
| XLSX e 100 imagens sintéticas de ECG | preservados como entregáveis da Fase 1 e material para extensões | não entram no pipeline obrigatório textual da Fase 2 |

Os 10 relatos de sintomas, as 45 expressões do mapa e as 80 frases rotuladas
foram elaborados para a Fase 2. Não existe vínculo entre essas frases e os
identificadores `SYN-XXXX` do CSV da Fase 1. Os modelos de Regressão Logística e
Árvore de Decisão são treinados exclusivamente com `data/raw/dataset_risco.csv`.

## Representação e viés de simulação

A base da Fase 1 contém **{contagens[ROTULO_MENOR]} rótulos `{ROTULO_MENOR}` e
{contagens[ROTULO_MAIOR]} rótulos `{ROTULO_MAIOR}`**. São {tabela['identificadores_unicos']}
identificadores sintéticos distintos, {tabela['celulas_vazias']} células vazias e
idades entre {tabela['idade_minima']} e {tabela['idade_maxima']} anos.

| Dimensão | Grupo | Registros | Higher | Lower | Proporção Higher |
|---|---|---:|---:|---:|---:|
{linhas_subgrupos}

As faixas etárias são agrupamentos descritivos deste projeto, sem significado
clínico atribuído. As proporções descrevem **rótulos do gerador**, não prevalência
de doença. Não são métricas de desempenho ou de equidade de um modelo.

O script original adiciona `0.45` ao escore de simulação quando `sex_at_birth == "M"`;
idade e outras variáveis também integram a fórmula. A diferença observada entre
grupos foi, portanto, influenciada pelas decisões do gerador. Não é evidência
populacional. A baixa contagem de rótulos Higher, especialmente no grupo F,
impede conclusões robustas por subgrupo.

Prever sempre a classe majoritária acertaria **{tabela['proporcao_classe_majoritaria']:.1%}**
destas linhas, mas encontraria zero exemplos da classe minoritária. Esse cálculo
descritivo ilustra por que acurácia isolada pode enganar; não é um modelo treinado
nem um resultado de teste. Ele não deve ser comparado aos 80% do experimento textual,
que tem outra tarefa, outros rótulos e outra divisão de dados.

## NLP exploratório sobre os textos da Fase 1

Método: extrair somente a seção `CONTEXTO`; transformar em minúsculas; remover
acentos; separar tokens alfabéticos; excluir tokens com menos de três letras e
uma lista explícita de palavras funcionais, versionada no script e no JSON.
Cabeçalhos, URLs, perguntas propostas e a seção de limitações não entram na contagem.
Não há lematização, extração clínica, rotulagem ou treinamento neste passo.

| Texto | Tokens após filtro | Termos distintos | Cinco termos mais frequentes |
|---|---:|---:|---|
{linhas_textos}

Os termos comuns e as frequências completas estão nos arquivos de evidência.
Os dois textos contextualizam obras históricas; as obras originais não foram
baixadas nem processadas nesta etapa. A amostra é pequena e não representa um
corpus clínico contemporâneo.

## Decisão metodológica

A continuidade tem evidências executáveis de exploração de dados, NLP e análise
do viés de geração a partir dos ativos da Fase 1. Na Parte 2, o enunciado detalhado
pede montar uma pequena base simulada em CSV com frases rotuladas; essa tarefa é
atendida pelo conjunto independente de 80 frases da Fase 2.

O CSV de 150 registros não treinou o modelo textual. Seus rótulos originais
descrevem um escore didático calculado pelo gerador a partir de atributos tabulares;
os rótulos das 80 frases foram definidos para o exercício de classificação de
relatos. Equiparar esses rótulos ou unir as bases confundiria tarefas distintas.
A decisão foi reutilizar os ativos originais para NLP exploratório e análise de
vieses e construir o corpus próprio de classificação solicitado, mantendo
rastreabilidade, avaliações e resultados separados.

## Reproduzir e localizar as evidências

Na pasta da Fase 2:

```bash
python src/auditar_continuidade_fase1.py
python -m unittest discover -s tests -p 'test_continuidade_fase1.py' -v
```

- `data/processed/continuidade_fase1.json`: auditoria, fontes, hashes e termos;
- `data/processed/representacao_fase1.csv`: contagens por sexo e faixa etária;
- `data/processed/termos_fase1.csv`: frequência completa por texto;
- `docs/CONTINUIDADE_FASE1.md`: este relatório, gerado pelo script.

Nenhum arquivo da Fase 1 nem as 80 frases da Fase 2 é modificado pelo script.
As evidências são determinísticas e não são adicionadas às métricas dos modelos.

## Identificação das fontes

Os caminhos abaixo são relativos à raiz do repositório. O SHA256 identifica os
bytes lidos, incluindo o script de simulação e o conjunto independente da Fase 2.

| Fonte | SHA256 |
|---|---|
{linhas_fontes}

> Projeto educacional com dados sintéticos. Nenhuma análise constitui diagnóstico,
> recomendação clínica ou comprovação de equidade em uma população real.
"""


def main() -> None:
    auditoria = auditar()
    processados = RAIZ / "data" / "processed"
    processados.mkdir(parents=True, exist_ok=True)
    (processados / "continuidade_fase1.json").write_text(
        json.dumps(auditoria, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    with (processados / "representacao_fase1.csv").open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=list(auditoria["subgrupos"][0]))
        escritor.writeheader()
        escritor.writerows(auditoria["subgrupos"])
    with (processados / "termos_fase1.csv").open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["fonte", "termo", "ocorrencias"])
        escritor.writeheader()
        for texto in auditoria["nlp"]["textos"]:
            escritor.writerows({"fonte": texto["fonte"]["caminho"], **item} for item in texto["frequencias"])
    (RAIZ / "docs" / "CONTINUIDADE_FASE1.md").write_text(
        gerar_documentacao(auditoria), encoding="utf-8"
    )
    print("Continuidade auditada: CSV da Fase 1, dois TXT, representação e análise lexical.")
    print("Classificador das 80 frases preservado como experimento independente.")


if __name__ == "__main__":
    main()
