"""Executa as células de código sem depender de um kernel Jupyter externo."""

from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("MPLBACKEND", "Agg")
RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOK = RAIZ / "notebooks" / "classificador_risco_tfidf.ipynb"


def executar_notebook() -> dict[str, object]:
    """Executa o notebook e devolve seu namespace para auditoria automatizada."""
    documento = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert documento["nbformat"] == 4
    namespace = {"__name__": "__notebook_validation__"}
    diretorio_original = Path.cwd()
    os.chdir(RAIZ)
    try:
        for indice, celula in enumerate(documento["cells"], start=1):
            if celula["cell_type"] != "code":
                continue
            fonte = "".join(celula["source"])
            exec(compile(fonte, f"{NOTEBOOK.name}:cell-{indice}", "exec"), namespace)
    finally:
        os.chdir(diretorio_original)
    return namespace


def main() -> None:
    executar_notebook()
    print("Notebook validado: todas as células de código executaram sem erros.")


if __name__ == "__main__":
    main()
