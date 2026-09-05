"""Regressões para perda de outputs e sobrescrita parcial do notebook."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from src.validar_notebook import executar_notebook


class TestExecucaoNotebook(unittest.TestCase):
    def documento(self, fontes):
        return {"nbformat": 4, "nbformat_minor": 5, "metadata": {}, "cells": [
            {"cell_type": "code", "id": f"teste-{i}", "metadata": {}, "execution_count": None,
             "outputs": [], "source": fonte}
            for i, fonte in enumerate(fontes)
        ]}

    def test_persiste_stdout_tabela_e_figura(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "teste.ipynb"
            caminho.write_text(json.dumps(self.documento([
                "import pandas as pd\nprint('evidência')\npd.DataFrame({'valor': [42]})",
                "import matplotlib.pyplot as plt\nplt.plot([1, 2], [3, 4])\nplt.show()",
            ])), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                executar_notebook(caminho)
            celulas = json.loads(caminho.read_text())["cells"]
            self.assertEqual([c["execution_count"] for c in celulas], [1, 2])
            self.assertIn("evidência", "".join(celulas[0]["outputs"][0]["text"]))
            self.assertIn("text/html", celulas[0]["outputs"][1]["data"])
            self.assertIn("image/png", celulas[1]["outputs"][0]["data"])

    def test_erro_preserva_arquivo_e_diretorio_original(self):
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "teste.ipynb"
            original = json.dumps(self.documento(["raise ValueError('falha simulada')"]))
            caminho.write_text(original, encoding="utf-8")
            cwd = Path.cwd()
            with self.assertRaises(ValueError):
                executar_notebook(caminho)
            self.assertEqual(Path.cwd(), cwd)
            self.assertEqual(caminho.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
