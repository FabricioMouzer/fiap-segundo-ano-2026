# CardioIA — Fase 2: Diagnóstico Automatizado

Módulo acadêmico de apoio à triagem cardiológica que combina extração de sintomas por mapa de conhecimento e classificação de risco textual com TF-IDF e Machine Learning.

> Projeto educacional. A solução não realiza diagnóstico médico, não substitui profissionais de saúde e não deve ser utilizada em atendimento clínico real.

## Status

🟢 Pipeline validado: dados, extrator, testes, notebook TF-IDF e evidências reproduzíveis implementados.

## Guia de orientação da equipe

Para entender a evolução do CardioIA, o que foi realizado na Fase 1 e todo o plano da Fase 2, consulte:

- [Visão geral das Fases 1 e 2](docs/VISAO_GERAL_FASES_1_E_2.md)
- [Recursos, plugins, interfaces e arquitetura](docs/RECURSOS_E_ARQUITETURA.md)
- [Dicionário de dados](data/DICIONARIO_DADOS.md)
- [Resultados e evidências de validação](docs/RESULTADOS_VALIDACAO.md)
- [Análise das previsões incorretas](docs/ANALISE_ERROS_MODELO.md)
- [Matriz de atendimento ao barema](docs/MATRIZ_BAREMA.md)

## Objetivos

1. Ler relatos sintéticos de pacientes e identificar sintomas por expressões conhecidas.
2. Relacionar os sintomas a hipóteses educacionais por meio de um mapa de conhecimento.
3. Classificar relatos como `baixo risco` ou `alto risco` usando TF-IDF e um classificador supervisionado.
4. Avaliar desempenho, erros, limitações e possíveis vieses.
5. Documentar e demonstrar a solução de forma reprodutível.

## Entregáveis obrigatórios

- `relatos_sintomas.txt` com 10 relatos completos e variados;
- `mapa_conhecimento.csv` com sintomas, sinônimos e doenças associadas;
- código de extração de sintomas e sugestão de hipótese;
- `dataset_risco.csv` com frases rotuladas;
- notebook com TF-IDF, treinamento, teste e avaliação;
- README completo e repositório público;
- vídeo de até 4 minutos no YouTube como não listado, com link neste README.

## Estrutura planejada

```text
cardioia-fase2-diagnostico-automatizado/
├── data/
│   ├── raw/
│   ├── processed/
│   └── README.md
├── docs/
│   ├── GOVERNANCA_E_LIMITACOES.md
│   ├── PLANO_EXECUCAO.md
│   ├── ROTEIRO_VIDEO.md
│   └── CHECKLIST_ENTREGA.md
├── notebooks/
├── src/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Equipe

| Integrante | RM |
|---|---:|
| Fabrício Mouzer Brito | RM566777 |
| Enzo Nunes Castanheira Gloria da Silva | RM567599 |
| Larissa Nunes Moreira Reis | RM568280 |
| Gabriel Rapozo Guimarães Soares | RM568480 |

## Tecnologias previstas

- Python 3.11+
- pandas
- scikit-learn
- Jupyter Notebook
- matplotlib e seaborn
- pytest

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No Windows PowerShell, ative o ambiente com:

```powershell
.venv\Scripts\Activate.ps1
```

## Execução

```bash
python src/gerar_dados.py
python src/extrator_sintomas.py
python -m unittest discover -s tests -v
python src/gerar_evidencias.py
jupyter notebook notebooks/classificador_risco_tfidf.ipynb
```

## Vídeo de demonstração

Link: `A INSERIR APÓS PUBLICAÇÃO COMO NÃO LISTADO`

## Demonstração visual interativa

[Abrir o portal CardioIA](https://cardioia-demo-fiap.fabriciomouzer2025.chatgpt.site)

O portal permite testar relatos sintéticos, consultar os sintomas identificados pelo mapa de conhecimento e visualizar a classificação produzida pelos parâmetros exportados da Regressão Logística validada no notebook. Consulte a [documentação da demonstração](docs/DEMONSTRACAO_VISUAL.md).

## Continuidade do projeto

Esta fase dá continuidade ao CardioIA iniciado na Fase 1, preservando o uso de dados sintéticos, a rastreabilidade dos artefatos e o compromisso com privacidade e IA responsável.
