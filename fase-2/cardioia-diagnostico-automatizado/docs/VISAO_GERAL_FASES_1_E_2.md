# CardioIA — O que construímos nas Fases 1 e 2

Revisão da equipe em **05/09/2026**. Este documento substitui o plano inicial, que ainda descrevia no futuro etapas já implementadas.

## A evolução do trabalho

A Fase 1 organizou materiais para estudar IA em cardiologia. A Fase 2 acrescentou dois módulos executáveis: um extrator por expressões e um classificador de relatos com TF-IDF. Nesta revisão, a continuidade ganhou evidência computacional pela leitura dos arquivos originais da Fase 1.

## O que aproveitamos da Fase 1

| Material original | Uso real na Fase 2 | Limite |
|---|---|---|
| CSV com 150 registros e 17 variáveis | auditoria de representação, rótulos e subgrupos | não integra o treino das 80 frases; rótulo de perfil não equivale à triagem textual |
| Dois TXT contextuais de cardiologia | exploração de vocabulário com origem e hashes | são textos contextuais, não relatos de pacientes nem obras integrais |
| Dicionário e governança | definição dos campos, origem sintética, privacidade e análise crítica | a base não representa uma população clínica real |
| 100 ECGs sintéticos | preservados para próximas etapas | não usados pelo TF-IDF; não demonstram conclusão do opcional MLP |
| XLSX e PDFs de apoio | referências da primeira entrega | não são entradas do classificador obrigatório |
| Repositório, equipe e organização | continuidade do histórico, autores e rastreabilidade | nenhuma contribuição individual é presumida |

O classificador utiliza **80 frases novas**, produzidas para a Fase 2. Não afirmamos que foram extraídas dos 150 registros da Fase 1. Consulte a [continuidade auditável](CONTINUIDADE_FASE1.md).

## Como chegamos ao resultado

1. Conferimos o enunciado e separamos os seis critérios obrigatórios das extensões “Ir Além”.
2. Organizamos dez relatos completos e um mapa com 45 expressões.
3. Implementamos leitura, normalização, busca de expressões e tratamento limitado de negação.
4. Criamos 80 frases rotuladas, distribuídas em 40 grupos de variações linguísticas.
5. Separamos 60 amostras de treino e 20 de teste por grupo; o TF-IDF foi ajustado somente no treino.
6. Comparamos Regressão Logística e Árvore de Decisão, mantendo os erros visíveis.
7. Geramos CSVs, métricas, matrizes de confusão e notebook com resultados salvos.
8. Acrescentamos leitura verificável da base anterior e revisamos documentação, testes e apresentação.

## Dois módulos com funções diferentes

| Módulo | Entrada | Método | Saída |
|---|---|---|---|
| Extração | dez relatos + mapa | regras e expressões normalizadas | sintomas e associações educacionais |
| Classificação | corpus de 80 frases | TF-IDF + modelo supervisionado | classe textual de baixo ou alto risco |

O extrator não fornece as variáveis de entrada do classificador. Ambos processam texto, com métodos distintos. A auditoria da Fase 1 é uma terceira análise de continuidade e representação, independente da avaliação das 80 frases.

## O que os resultados significam

Na divisão fixa, a Regressão Logística acertou **16 de 20 frases** e reconheceu **8 de 10 relatos rotulados como alto risco**. Foram dois falsos positivos e dois falsos negativos. A Árvore de Decisão teve 30% de acurácia e 20% de recall de alto risco.

Esses números descrevem um experimento pequeno e sintético. O mesmo conjunto foi usado para comparar os modelos; não existe teste externo independente que confirme generalização após a escolha. A separação por grupo evita que as duas versões da mesma frase base fiquem nos dois conjuntos, mas não elimina toda semelhança linguística entre grupos.

## Recursos utilizados

- Python e pandas: criação, leitura e auditoria dos dados.
- scikit-learn: TF-IDF, pipelines, divisão por grupos, modelos e métricas.
- Jupyter/IPython: notebook com método e resultados preservados.
- matplotlib e seaborn: gráficos de avaliação.
- unittest: testes dos dados, extração e continuidade.
- GitHub: fonte oficial do código, documentação e histórico.

Não é necessária chave de API nem serviço de IA pago para executar o núcleo. A [demonstração visual anterior](DEMONSTRACAO_VISUAL.md) é apoio; não comprova todos os requisitos do opcional React.

## Situação da entrega

Os artefatos técnicos dos cinco primeiros critérios do barema estão implementados e revisados. O sexto critério exige **vídeo de até quatro minutos publicado no YouTube como não listado e link no README**. Arquivo local, roteiro ou apresentação da equipe não substituem essa publicação.

Prazo informado: **07/10/2026**, sem horário final no enunciado recuperado. A conferência do grupo e o envio no ambiente FIAP permanecem ações de encerramento. Não há comprovante de submissão neste repositório.

## Equipe

| Integrante | RM |
|---|---|
| Fabrício Mouzer Brito | RM566777 |
| Enzo Nunes Castanheira Gloria da Silva | RM567599 |
| Larissa Nunes Moreira Reis | RM568280 |
| Gabriel Rapozo Guimarães Soares | RM568480 |

Todos devem compreender os dados, explicar os erros e revisar a entrega. Divisões anteriores eram sugestões, não registro de autoria individual.

## Links para revisão

- [Fase 1](../../../fase-1/cardioia-batimentos-de-dados/)
- [Fase 2](../README.md)
- [Resultados executados](RESULTADOS_VALIDACAO.md)
- [Matriz do barema](MATRIZ_BAREMA.md)
- [Checklist](CHECKLIST_ENTREGA.md)

> Uso exclusivamente acadêmico. O projeto não realiza diagnóstico e não deve orientar atendimento real.
