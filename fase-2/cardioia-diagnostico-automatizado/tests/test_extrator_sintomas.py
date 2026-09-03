import unittest
from pathlib import Path

from src.extrator_sintomas import analisar_arquivo, carregar_mapa, extrair_sintomas, normalizar


RAIZ = Path(__file__).resolve().parents[1]
MAPA = carregar_mapa(RAIZ / "data" / "raw" / "mapa_conhecimento.csv")


class TestExtratorSintomas(unittest.TestCase):
    def test_normaliza_acentos_e_pontuacao(self):
        self.assertEqual(normalizar("Coração acelerado!"), "coracao acelerado")

    def test_identifica_multiplos_sintomas(self):
        achados = extrair_sintomas("Sinto pressão no peito, falta de ar e suor frio.", MAPA)
        expressoes = {achado.expressao for achado in achados}
        self.assertTrue({"pressão no peito", "falta de ar", "suor frio"} <= expressoes)

    def test_ignora_negacao_simples(self):
        achados = extrair_sintomas("Não sinto dor no peito, apenas tensão muscular.", MAPA)
        self.assertNotIn("dor no peito", {achado.expressao for achado in achados})

    def test_retorna_lista_vazia_sem_correspondencia(self):
        self.assertEqual(extrair_sintomas("Estou me sentindo bem e mantive minha rotina.", MAPA), [])

    def test_nao_confunde_parte_de_outra_palavra(self):
        self.assertEqual(extrair_sintomas("O texto menciona uma palpitaçãozinha inventada.", MAPA), [])

    def test_todos_os_dez_relatos_possuem_achado(self):
        resultados = analisar_arquivo(
            RAIZ / "data" / "raw" / "relatos_sintomas.txt",
            RAIZ / "data" / "raw" / "mapa_conhecimento.csv",
        )
        self.assertEqual(len(resultados), 10)
        self.assertTrue(all(resultado["achados"] for resultado in resultados))


if __name__ == "__main__":
    unittest.main()
