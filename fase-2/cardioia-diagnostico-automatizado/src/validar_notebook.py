"""Executa este notebook Python e persiste saídas visíveis, sem kernel externo.

O executor atende células Python puras deste projeto. Não implementa magics,
widgets nem protocolos de kernel Jupyter. Erros interrompem a execução e não
sobrescrevem o notebook com uma execução parcial.
"""

from __future__ import annotations

import ast
import base64
import contextlib
import io
import json
import os
from pathlib import Path


os.environ.setdefault("MPLBACKEND", "Agg")
RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOK = RAIZ / "notebooks" / "classificador_risco_tfidf.ipynb"


def executar_notebook(caminho: Path = NOTEBOOK) -> dict[str, object]:
    """Executa e grava stdout, tabelas e figuras; devolve o namespace."""
    import matplotlib.pyplot as plt

    documento = json.loads(caminho.read_text(encoding="utf-8"))
    assert documento["nbformat"] == 4
    namespace = {"__name__": "__notebook_validation__"}
    diretorio_original = Path.cwd()
    show_original = plt.show
    plt.close("all")
    os.chdir(RAIZ)
    execucao = 0
    try:
        for indice, celula in enumerate(documento["cells"], start=1):
            if celula["cell_type"] != "code":
                continue
            execucao += 1
            outputs = []
            captura = io.StringIO()

            def capturar_figuras(*args, **kwargs):
                for numero in plt.get_fignums():
                    figura = plt.figure(numero)
                    buffer = io.BytesIO()
                    figura.savefig(buffer, format="png", dpi=120, bbox_inches="tight")
                    outputs.append({"output_type": "display_data", "metadata": {}, "data": {
                        "image/png": base64.b64encode(buffer.getvalue()).decode("ascii"),
                        "text/plain": [repr(figura)],
                    }})
                plt.close("all")

            plt.show = capturar_figuras
            fonte = "".join(celula["source"])
            filename = f"{caminho.name}:cell-{indice}"
            arvore = ast.parse(fonte, filename=filename)
            ultima = arvore.body.pop() if arvore.body and isinstance(arvore.body[-1], ast.Expr) else None
            with contextlib.redirect_stdout(captura), contextlib.redirect_stderr(captura):
                exec(compile(arvore, filename, "exec"), namespace)
                valor = eval(compile(ast.Expression(ultima.value), filename, "eval"), namespace) if ultima else None
            if captura.getvalue():
                outputs.insert(0, {"output_type": "stream", "name": "stdout", "text": captura.getvalue().splitlines(keepends=True)})
                print(captura.getvalue(), end="")
            if valor is not None:
                dados = {"text/plain": [repr(valor)]}
                if hasattr(valor, "_repr_html_"):
                    html = valor._repr_html_()
                    if html:
                        dados["text/html"] = [html]
                outputs.append({"output_type": "execute_result", "execution_count": execucao, "metadata": {}, "data": dados})
            celula["execution_count"] = execucao
            celula["outputs"] = outputs
    finally:
        plt.show = show_original
        plt.close("all")
        os.chdir(diretorio_original)
    caminho.write_text(json.dumps(documento, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return namespace


def main() -> None:
    executar_notebook()
    print("Notebook executado e salvo com saídas, tabelas e figuras.")


if __name__ == "__main__":
    main()
