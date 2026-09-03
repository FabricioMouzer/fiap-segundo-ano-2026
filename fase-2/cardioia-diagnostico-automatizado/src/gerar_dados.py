"""Gera dados sintéticos e reprodutíveis da Fase 2 do CardioIA."""

from __future__ import annotations

import csv
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"


MAPA_CONHECIMENTO = [
    ("dor no peito", "dor torácica", "síndrome coronariana / outras causas", "alto"),
    ("dor intensa no peito", "dor torácica", "síndrome coronariana / outras causas", "alto"),
    ("pressão no peito", "dor torácica", "angina / síndrome coronariana", "alto"),
    ("pressão forte no peito", "dor torácica", "angina / síndrome coronariana", "alto"),
    ("aperto no tórax", "dor torácica", "angina / síndrome coronariana", "alto"),
    ("peso no peito", "dor torácica", "angina / síndrome coronariana", "alto"),
    ("queimação no peito", "desconforto torácico", "causa cardíaca ou digestiva", "avaliar"),
    ("falta de ar", "dispneia", "insuficiência cardíaca / causa respiratória", "alto"),
    ("dificuldade para respirar", "dispneia", "insuficiência cardíaca / causa respiratória", "alto"),
    ("respiração curta", "dispneia", "insuficiência cardíaca / causa respiratória", "alto"),
    ("cansaço constante", "fadiga", "insuficiência cardíaca / outras causas", "avaliar"),
    ("fadiga", "fadiga", "insuficiência cardíaca / outras causas", "avaliar"),
    ("cansaço aos esforços", "intolerância ao esforço", "insuficiência cardíaca / isquemia", "avaliar"),
    ("coração acelerado", "palpitação", "taquicardia / arritmia", "avaliar"),
    ("coração fica acelerado", "palpitação", "taquicardia / arritmia", "avaliar"),
    ("palpitação", "palpitação", "arritmia", "avaliar"),
    ("batimento irregular", "ritmo irregular", "arritmia", "avaliar"),
    ("coração irregular", "ritmo irregular", "arritmia", "avaliar"),
    ("suor frio", "sudorese fria", "síndrome coronariana / outras causas", "alto"),
    ("náusea", "náusea", "síndrome coronariana / causa digestiva", "avaliar"),
    ("tontura", "tontura", "arritmia / hipotensão / outras causas", "avaliar"),
    ("quase desmaiei", "pré-síncope", "arritmia / hipotensão", "alto"),
    ("desmaio", "síncope", "arritmia / outras causas", "alto"),
    ("perda de consciência", "síncope", "arritmia / outras causas", "alto"),
    ("inchaço nos tornozelos", "edema periférico", "insuficiência cardíaca / outras causas", "avaliar"),
    ("pernas inchadas", "edema periférico", "insuficiência cardíaca / outras causas", "avaliar"),
    ("pés inchados", "edema periférico", "insuficiência cardíaca / outras causas", "avaliar"),
    ("tosse ao deitar", "ortopneia / tosse noturna", "insuficiência cardíaca / causa respiratória", "avaliar"),
    ("tosse seca ao deitar", "ortopneia / tosse noturna", "insuficiência cardíaca / causa respiratória", "avaliar"),
    ("usar mais travesseiros", "ortopneia", "insuficiência cardíaca / causa respiratória", "avaliar"),
    ("dor nas costas", "dor dorsal", "causa musculoesquelética / outras causas", "baixo"),
    ("dor leve nas costas", "dor dorsal", "causa musculoesquelética / outras causas", "baixo"),
    ("pontada no peito", "dor torácica atípica", "causa musculoesquelética / pleurítica", "avaliar"),
    ("pontada breve no peito", "dor torácica atípica", "causa musculoesquelética / pleurítica", "avaliar"),
    ("piora quando respiro fundo", "dor pleurítica", "causa pleural / musculoesquelética", "avaliar"),
    ("fraqueza súbita", "déficit neurológico súbito", "acidente vascular cerebral", "alto"),
    ("um lado do corpo", "déficit neurológico focal", "acidente vascular cerebral", "alto"),
    ("dificuldade para falar", "alteração da fala", "acidente vascular cerebral", "alto"),
    ("fala enrolada", "alteração da fala", "acidente vascular cerebral", "alto"),
    ("dor no braço esquerdo", "irradiação para braço", "síndrome coronariana", "alto"),
    ("dor no maxilar", "irradiação para mandíbula", "síndrome coronariana", "alto"),
    ("dor no ombro", "dor no ombro", "causa musculoesquelética / dor irradiada", "avaliar"),
    ("lábios arroxeados", "cianose", "baixa oxigenação / causa cardiopulmonar", "alto"),
    ("confusão mental", "alteração do estado mental", "baixa perfusão / outras causas", "alto"),
    ("dor após esforço", "sintoma relacionado ao esforço", "angina / causa musculoesquelética", "avaliar"),
]


ALTO_RISCO = [
    "Sinto forte dor no peito com falta de ar desde esta manhã.",
    "Uma pressão intensa no peito começou durante a caminhada e não melhorou com repouso.",
    "Estou com aperto no tórax, suor frio e náusea há vinte minutos.",
    "A dor no peito está irradiando para o braço esquerdo e para o maxilar.",
    "Meu coração está muito acelerado e quase desmaiei ao levantar.",
    "Tive um desmaio repentino depois de sentir o batimento irregular.",
    "Comecei a sentir fraqueza súbita em um lado do corpo e dificuldade para falar.",
    "Estou com falta de ar intensa mesmo parado e meus lábios parecem arroxeados.",
    "Acordei sem conseguir respirar e continuo com forte pressão no peito.",
    "Estou confuso, com suor frio e uma dor forte no tórax.",
    "Senti perda de consciência após uma sequência de palpitações.",
    "A falta de ar piorou rapidamente e agora não consigo completar uma frase.",
    "Tenho dor torácica intensa e sensação de desmaio desde alguns minutos atrás.",
    "Meu peito está apertado e a dor se espalha para o ombro e braço.",
    "A dor no peito começou durante o esforço e permanece mesmo sentado.",
    "Estou com respiração muito curta, tontura e suor frio.",
    "Uma dor súbita no peito veio acompanhada de náusea e fraqueza intensa.",
    "Meu coração está irregular e tive uma perda breve de consciência.",
    "Sinto forte peso no peito e dificuldade para respirar desde agora há pouco.",
    "Minha fala ficou enrolada e perdi força em um dos braços de forma súbita.",
]


BAIXO_RISCO = [
    "Senti leve dor nas costas depois de carregar caixas e ela melhora com repouso.",
    "Tenho uma pontada breve no peito apenas quando movimento o tronco.",
    "O ombro ficou dolorido após a academia, mas consigo fazer minhas atividades.",
    "Sinto leve desconforto muscular nas costas desde o treino de ontem.",
    "A pontada no lado do peito dura poucos segundos e aparece ao girar o corpo.",
    "Tenho cansaço leve depois de dormir pouco, sem falta de ar ou dor no peito.",
    "Senti tensão no ombro após trabalhar muitas horas sentado.",
    "A dor nas costas começou depois de uma postura ruim e melhora ao alongar.",
    "Tenho um incômodo leve no peito ao apertar o local com a mão.",
    "O desconforto no tórax apareceu após exercício de braço e melhora parado.",
    "Sinto dor muscular leve quando levanto o braço direito.",
    "Tive uma pontada curta no peito ao respirar fundo, mas ela já passou.",
    "Estou com leve cansaço após uma noite mal dormida e mantenho minha rotina.",
    "Sinto rigidez nas costas ao acordar, que melhora durante o dia.",
    "O peito ficou sensível depois do treino, principalmente ao tocar a região.",
    "Tenho dor leve no ombro desde que carreguei uma mochila pesada.",
    "Senti um pequeno incômodo nas costas durante o trabalho, sem outros sintomas.",
    "A dor aparece somente quando faço um movimento específico com o tronco.",
    "Estou com desconforto muscular após atividade física e ele vem melhorando.",
    "Sinto uma pontada superficial e rápida quando espirro ou me movimento.",
]


def escrever_csv(caminho: Path, cabecalho: list[str], linhas: list[tuple[str, ...]]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(cabecalho)
        escritor.writerows(linhas)


def expandir_frases(frases_base: list[str], rotulo: str, prefixo: str) -> list[tuple[str, str, str]]:
    tempos = ["Hoje,", "Desde ontem,", "Nesta manhã,", "Há dois dias,"]
    impactos = [
        " Isso alterou minha rotina.",
        " Percebi o sintoma durante minhas atividades.",
        " O episódio me deixou preocupado.",
        " Estou observando a evolução do sintoma.",
    ]
    linhas: list[tuple[str, str, str]] = []
    for indice, frase in enumerate(frases_base):
        base = frase[0].lower() + frase[1:]
        grupo_id = f"{prefixo}_{indice + 1:02d}"
        linhas.append((frase, rotulo, grupo_id))
        linhas.append((f"{tempos[indice % len(tempos)]} {base}{impactos[indice % len(impactos)]}", rotulo, grupo_id))
    return linhas


def main() -> None:
    escrever_csv(
        RAW / "mapa_conhecimento.csv",
        ["expressao", "sintoma_normalizado", "possivel_associacao", "nivel_alerta"],
        MAPA_CONHECIMENTO,
    )

    dataset = expandir_frases(ALTO_RISCO, "alto risco", "alto")
    dataset += expandir_frases(BAIXO_RISCO, "baixo risco", "baixo")
    dataset_ordenado = sorted(dataset, key=lambda item: (len(item[0]) % 11, item[0]))
    escrever_csv(RAW / "dataset_risco.csv", ["frase", "situacao", "grupo_id"], dataset_ordenado)

    print(f"Mapa de conhecimento: {len(MAPA_CONHECIMENTO)} associações")
    print(f"Dataset de risco: {len(dataset_ordenado)} frases")


if __name__ == "__main__":
    main()
