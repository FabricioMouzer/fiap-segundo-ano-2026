import csv
import unittest
from collections import Counter
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"


class TestDados(unittest.TestCase):
    def test_mapa_possui_estrutura_e_volume(self):
        with (RAW / "mapa_conhecimento.csv").open(encoding="utf-8", newline="") as arquivo:
            linhas = list(csv.DictReader(arquivo))
        self.assertGreaterEqual(len(linhas), 30)
        self.assertEqual(set(linhas[0]), {"expressao", "sintoma_normalizado", "possivel_associacao", "nivel_alerta"})
        self.assertEqual(len({linha["expressao"] for linha in linhas}), len(linhas))

    def test_dataset_esta_balanceado_e_sem_duplicidades(self):
        with (RAW / "dataset_risco.csv").open(encoding="utf-8", newline="") as arquivo:
            linhas = list(csv.DictReader(arquivo))
        contagem = Counter(linha["situacao"] for linha in linhas)
        self.assertEqual(contagem["alto risco"], contagem["baixo risco"])
        self.assertEqual(len({linha["frase"] for linha in linhas}), len(linhas))
        self.assertTrue(all(linha["grupo_id"] for linha in linhas))


if __name__ == "__main__":
    unittest.main()
