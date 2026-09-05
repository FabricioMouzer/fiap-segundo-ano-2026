# CardioIA — Fase 2: Diagnóstico Automatizado

Protótipo acadêmico que extrai sintomas por mapa de conhecimento e classifica relatos sintéticos com TF-IDF e Machine Learning.

> Uso exclusivamente educacional. Não realiza diagnóstico médico nem deve orientar atendimento real.

## Estado revisado em 05/09/2026

**Núcleo técnico concluído e reproduzido: 19 testes aprovados.** O notebook está executado, com tabelas e gráficos salvos. A entrega ainda depende da publicação do vídeo como não listado, revisão do grupo e envio à FIAP.

**Prazo:** 07/10/2026. O enunciado recuperado não informa o horário final.

| Critério obrigatório | Peso | Evidência |
|---|---:|---|
| Relatos e mapa organizados | 2 | [10 relatos](data/raw/relatos_sintomas.txt) e [45 expressões](data/raw/mapa_conhecimento.csv) |
| Extração funcional | 2 | [código](src/extrator_sintomas.py), [achados CSV](data/processed/resultados_extrator.csv) |
| Dataset rotulado | 1 | [80 frases em 40 grupos](data/raw/dataset_risco.csv) |
| Classificador treinado e testado | 2 | [notebook executado](notebooks/classificador_risco_tfidf.ipynb), [métricas](data/processed/metricas_modelos.json) |
| Documentação e GitHub público | 1 | README, [revisão final](docs/REVISAO_FINAL_2026-09-05.md) e documentação |
| Vídeo ≤4 minutos, YouTube não listado e link | 2 | **publicação pendente** |

Os pesos identificam critérios com evidências, não pontuação atribuída pelo professor nem percentual de trabalho enviado.

## Entenda o projeto

- [O que foi feito e como chegamos](docs/VISAO_GERAL_FASES_1_E_2.md)
- [O que reaproveitamos da Fase 1](docs/CONTINUIDADE_FASE1.md)
- [Arquitetura e recursos](docs/RECURSOS_E_ARQUITETURA.md)
- [Dicionário de dados](data/DICIONARIO_DADOS.md)
- [Resultados](docs/RESULTADOS_VALIDACAO.md) e [quatro erros do modelo](docs/ANALISE_ERROS_MODELO.md)
- [Governança e limites](docs/GOVERNANCA_E_LIMITACOES.md)
- [Matriz do barema](docs/MATRIZ_BAREMA.md) e [checklist](docs/CHECKLIST_ENTREGA.md)

## Apresentação para a equipe

[Apresentação em PDF](docs/apresentacao/CardioIA_Fase2_Revisao_Equipe.pdf) · [PowerPoint editável](docs/apresentacao/CardioIA_Fase2_Revisao_Equipe.pptx)

São 13 slides com resultados, percurso, ferramentas, continuidade da Fase 1 e pendências de entrega.

## Reprodução

Clone o repositório completo, pois a auditoria de continuidade lê os arquivos da Fase 1:

```bash
git clone https://github.com/FabricioMouzer/fiap-segundo-ano-2026.git
cd fiap-segundo-ano-2026/fase-2/cardioia-diagnostico-automatizado
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-validado.txt
```

No Windows PowerShell, ative com `.venv\Scripts\Activate.ps1`. Use Python 3.12 para reproduzir o ambiente registrado. `requirements-validado.txt` contém as versões efetivamente executadas nesta revisão; `requirements.txt` preserva a configuração inicial, que não é a referência destas métricas.

Execute na ordem:

```bash
python src/gerar_dados.py
python src/auditar_continuidade_fase1.py
python -m unittest discover -s tests -v
python src/construir_notebook.py
python src/gerar_evidencias.py
```

O último comando executa e salva o notebook, as métricas e os gráficos. O executor local atende às células Python deste projeto; não implementa magics/widgets nem substitui um kernel Jupyter completo. O arquivo `.ipynb` também pode ser aberto no Jupyter ou visualizado no GitHub. Gerar novamente o notebook limpa suas saídas; execute sempre `gerar_evidencias.py` depois.

Não são necessárias credenciais, API de IA paga ou acesso ao Drive. [Manifesto de execução](data/processed/manifesto_execucao.json), [log dos testes](data/processed/execucao_testes.txt) e [reprodutibilidade](data/processed/reprodutibilidade.json) documentam esta validação.

## Resultados do experimento

| Modelo | Acurácia | Recall de alto risco | F1 de alto risco |
|---|---:|---:|---:|
| Regressão Logística | 80% | 80% | 80% |
| Árvore de Decisão | 30% | 20% | 22,2% |

São 60 amostras de treino e 20 de teste, com grupos separados. A Regressão Logística acertou 16/20, incluindo 8/10 relatos de alto risco; teve dois falsos negativos e dois falsos positivos. A comparação é exploratória numa divisão fixa, sem teste clínico externo. Os números não demonstram generalização para pacientes reais.

## Continuidade da Fase 1

A auditoria lê o CSV original de 150 registros/17 variáveis e os dois TXT contextuais. Gera representação por grupos, análise de rótulos e vocabulário com hashes das fontes. As 80 frases de treinamento foram criadas para a Fase 2 e permanecem separadas. Os 100 ECGs e PDFs da Fase 1 são preservados; não alimentam este classificador.

## Vídeo de demonstração

**YouTube não listado: publicação pendente.** O link definitivo será incluído após publicação e verificação sem login. Um arquivo local ou roteiro não encerra esse critério.

O vídeo técnico legendado está preparado e validado: **3min40, 1080p**, com 11 etapas de arquivos e saídas reais. Consulte [identificação e legendas](docs/video/README.md) e [roteiro](docs/ROTEIRO_VIDEO.md). A apresentação da equipe explica o percurso do projeto; o vídeo técnico demonstra o funcionamento exigido pela FIAP.

## Demonstração visual anterior

[Abrir demonstração CardioIA](https://cardioia-demo-fiap.fabriciomouzer2025.chatgpt.site)

Esta interface é um apoio independente, descrito em [DEMONSTRACAO_VISUAL.md](docs/DEMONSTRACAO_VISUAL.md). A auditoria atual valida os arquivos Python; não declara sincronizada a versão publicada do extrator nem conclui os opcionais “Ir Além”. O portal completo de pacientes/agendamentos e a MLP de ECG permanecem fora da entrega obrigatória.

## Equipe

| Integrante | RM |
|---|---|
| Fabrício Mouzer Brito | RM566777 |
| Enzo Nunes Castanheira Gloria da Silva | RM567599 |
| Larissa Nunes Moreira Reis | RM568280 |
| Gabriel Rapozo Guimarães Soares | RM568480 |
