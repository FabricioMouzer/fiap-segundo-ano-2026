"""Extrator explicável de sintomas para a simulação acadêmica CardioIA."""

from __future__ import annotations

import csv
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Achado:
    expressao: str
    sintoma: str
    possivel_associacao: str
    nivel_alerta: str


NEGACOES = {"nao", "sem", "nega", "nego", "nunca"}


def normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(char for char in texto if not unicodedata.combining(char))
    texto = re.sub(r"[^a-z0-9\s]", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def carregar_mapa(caminho: str | Path) -> list[dict[str, str]]:
    with Path(caminho).open(encoding="utf-8", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def esta_negada(texto_normalizado: str, expressao_normalizada: str) -> bool:
    """Avalia todas as ocorrências em uma oração já normalizada.

    A negação abrange a enumeração na mesma oração. Uma ocorrência afirmada
    basta para conservar o achado. É uma heurística, sem interpretação clínica.
    """
    ocorrencias = list(re.finditer(rf"(?<!\w){re.escape(expressao_normalizada)}(?!\w)", texto_normalizado))
    if not ocorrencias:
        return False
    negadas = []
    for ocorrencia in ocorrencias:
        contexto = texto_normalizado[:ocorrencia.start()]
        contexto = re.sub(r"\bnao (?:so|somente|apenas)\b", "", contexto)
        negadas.append(any(token in NEGACOES for token in contexto.split()))
    return all(negadas)


def segmentar_oracoes(relato: str) -> list[str]:
    """Preserva fronteiras de negação antes de remover a pontuação."""
    sem_acentos = unicodedata.normalize("NFKD", relato.lower())
    sem_acentos = "".join(char for char in sem_acentos if not unicodedata.combining(char))
    fronteiras = (
        r"[.!?;\n]+|\b(?:mas|porem|contudo|entretanto|no entanto)\b"
        r"|,(?=\s*(?:sinto|tenho|apresento|relato|estou com)\b)"
    )
    return [normalizar(parte) for parte in re.split(fronteiras, sem_acentos) if parte.strip()]


def extrair_sintomas(relato: str, mapa: list[dict[str, str]]) -> list[Achado]:
    oracoes = segmentar_oracoes(relato)
    achados: list[Achado] = []
    vistos: set[tuple[str, str]] = set()

    for linha in mapa:
        expressao_normalizada = normalizar(linha["expressao"])
        padrao = rf"(?<!\w){re.escape(expressao_normalizada)}(?!\w)"
        if any(re.search(padrao, texto) and not esta_negada(texto, expressao_normalizada) for texto in oracoes):
            chave = (linha["expressao"], linha["possivel_associacao"])
            if chave not in vistos:
                vistos.add(chave)
                achados.append(
                    Achado(
                        expressao=linha["expressao"],
                        sintoma=linha["sintoma_normalizado"],
                        possivel_associacao=linha["possivel_associacao"],
                        nivel_alerta=linha["nivel_alerta"],
                    )
                )
    return achados


def analisar_arquivo(relatos_path: str | Path, mapa_path: str | Path) -> list[dict[str, object]]:
    mapa = carregar_mapa(mapa_path)
    relatos = [linha.strip() for linha in Path(relatos_path).read_text(encoding="utf-8").splitlines() if linha.strip()]
    return [
        {"relato": relato, "achados": [asdict(achado) for achado in extrair_sintomas(relato, mapa)]}
        for relato in relatos
    ]


def main() -> None:
    raiz = Path(__file__).resolve().parents[1]
    resultados = analisar_arquivo(
        raiz / "data" / "raw" / "relatos_sintomas.txt",
        raiz / "data" / "raw" / "mapa_conhecimento.csv",
    )
    for indice, resultado in enumerate(resultados, start=1):
        print(f"\nRelato {indice}: {resultado['relato']}")
        achados = resultado["achados"]
        if not achados:
            print("  Nenhuma associação encontrada.")
        for achado in achados:
            print(
                f"  - {achado['expressao']} → {achado['sintoma']} → "
                f"{achado['possivel_associacao']} [{achado['nivel_alerta']}]"
            )
    print("\nAVISO: resultado educacional; não constitui diagnóstico médico.")


if __name__ == "__main__":
    main()
