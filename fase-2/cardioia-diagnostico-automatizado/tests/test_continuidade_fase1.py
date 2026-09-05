"""Verifica rastreabilidade e conservação dos dados na ponte entre as fases."""

import csv
import hashlib
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from src.auditar_continuidade_fase1 import (
    CSV_FASE1, RAIZ, REPOSITORIO, TEXTOS, analisar_texto, auditar,
)


class TestContinuidadeFase1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidencia = auditar()
        with CSV_FASE1.open(encoding="utf-8", newline="") as arquivo:
            cls.originais = list(csv.DictReader(arquivo))

    def test_fontes_identificadas_e_preservadas(self):
        fontes = [self.evidencia["fonte_tabular"], self.evidencia["fonte_regra_simulacao"]]
        fontes += [t["fonte"] for t in self.evidencia["nlp"]["textos"]]
        fontes.append(self.evidencia["experimento_classificacao_fase2"]["fonte"])
        antes = {f["caminho"]: (REPOSITORIO / f["caminho"]).read_bytes() for f in fontes}
        auditar()
        for fonte in fontes:
            with self.subTest(fonte=fonte["caminho"]):
                self.assertFalse(Path(fonte["caminho"]).is_absolute())
                self.assertEqual(fonte["sha256"], hashlib.sha256(antes[fonte["caminho"]]).hexdigest())
                self.assertEqual(antes[fonte["caminho"]], (REPOSITORIO / fonte["caminho"]).read_bytes())

    def test_conserva_dataset_e_rotulos_originais(self):
        tabela = self.evidencia["tabela"]
        self.assertEqual(tabela["registros"], 150)
        self.assertEqual(len(tabela["colunas"]), 17)
        self.assertEqual(tabela["identificadores_unicos"], tabela["registros"])
        self.assertEqual(tabela["rotulos_originais"], dict(Counter(
            r["cardio_risk_label_synthetic"] for r in self.originais
        )))
        self.assertNotIn("situacao", tabela["colunas"])
        with (RAIZ / "data" / "raw" / "dataset_risco.csv").open(encoding="utf-8", newline="") as arquivo:
            frases = list(csv.DictReader(arquivo))
        self.assertEqual(len(frases), 80)
        self.assertTrue(set(tabela["rotulos_originais"]).isdisjoint(r["situacao"] for r in frases))

    def test_subgrupos_preservam_totais_sem_contar_registro_duas_vezes(self):
        subgrupos = self.evidencia["subgrupos"]
        for dimensao in {s["dimensao"] for s in subgrupos}:
            grupos = [s for s in subgrupos if s["dimensao"] == dimensao]
            with self.subTest(dimensao=dimensao):
                self.assertEqual(sum(s["registros"] for s in grupos), len(self.originais))
                for rotulo, total in self.evidencia["tabela"]["rotulos_originais"].items():
                    self.assertEqual(sum(s[rotulo] for s in grupos), total)
        for grupo in (s for s in subgrupos if s["dimensao"] == "sex_at_birth"):
            self.assertEqual(grupo["registros"], sum(r["sex_at_birth"] == grupo["grupo"] for r in self.originais))

    def test_nlp_usa_conteudo_e_exclui_metadados_e_perguntas(self):
        # Uma fonte externa mínima detecta contaminação por URL/cabeçalho/perguntas.
        texto = "CABECALHO\nhttps://exemplo.invalid\nCONTEXTO\nCoração, CORAÇÃO e artérias.\nPERGUNTAS DE NLP\nQual diagnóstico?"
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "contexto.txt"
            caminho.write_text(texto, encoding="utf-8")
            with patch("src.auditar_continuidade_fase1.REPOSITORIO", Path(diretorio)):
                resultado = analisar_texto(caminho)
        frequencias = {item["termo"]: item["ocorrencias"] for item in resultado["frequencias"]}
        self.assertEqual(frequencias, {"coracao": 2, "arterias": 1})
        self.assertEqual(len(self.evidencia["nlp"]["textos"]), len(TEXTOS))
        self.assertTrue(all(t["tokens_apos_filtragem"] > 0 for t in self.evidencia["nlp"]["textos"]))


if __name__ == "__main__":
    unittest.main()
