# Plano de execução — CardioIA Fase 2

## Resultado esperado

Entregar uma solução executável, documentada e demonstrável que cumpra integralmente os 10 pontos do barema e apresente diferenciais técnicos sem confundir uma simulação acadêmica com diagnóstico médico.

## Estratégia recomendada

### Trilha obrigatória — prioridade máxima

1. Reaproveitar a identidade, princípios de governança e dados sintéticos da Fase 1.
2. Produzir 10 relatos variados com sintoma, início/duração e impacto na rotina.
3. Criar mapa de conhecimento robusto, preferencialmente com 30 ou mais associações.
4. Implementar extração com normalização de texto, busca de expressões e tratamento de múltiplos sintomas.
5. Criar base de risco balanceada e maior que os exemplos mínimos do enunciado.
6. Separar treino e teste de forma estratificada.
7. Comparar pelo menos Regressão Logística e Árvore de Decisão, escolhendo o modelo final por evidência.
8. Apresentar acurácia, precision, recall, F1-score e matriz de confusão.
9. Executar testes com frases inéditas e analisar erros e vieses.
10. Revisar repositório, gravar vídeo e entregar com antecedência.

### Diferenciais de excelência

- sementes aleatórias fixas para reprodutibilidade;
- prevenção de vazamento entre treino e teste;
- comparação de modelos e justificativa da escolha;
- análise por negação, intensidade, duração e ambiguidade;
- seção clara de limitações e uso responsável;
- testes automatizados da extração;
- notebook limpo, executado do início ao fim e sem erros;
- tabela no README ligando cada item do barema à sua evidência.

## Marcos

| Marco | Entregável | Critério de conclusão |
|---|---|---|
| M1 — Base textual | TXT e mapa de conhecimento | 10 relatos completos; mapa revisado e sem duplicidades problemáticas |
| M2 — Extração | módulo Python + testes | identifica sintomas, múltiplas ocorrências e casos sem correspondência |
| M3 — Classificação | dataset + notebook | pipeline TF-IDF/modelo treinado, avaliado e reprodutível |
| M4 — Responsabilidade | análise de vieses | limitações, erros críticos e riscos documentados |
| M5 — Apresentação | README + vídeo | execução demonstrada em até 4 minutos; link válido |
| M6 — Entrega | repositório público | checklist integral revisado antes de 07/10/2026 |

## Divisão sugerida do grupo

| Frente | Responsabilidades | Responsável sugerido |
|---|---|---|
| Coordenação e integração | cronograma, PRs, revisão final, README | Fabrício |
| Dados e mapa de conhecimento | relatos, associações, qualidade e fontes | Enzo |
| NLP e classificador | TF-IDF, modelos, métricas e notebook | Larissa |
| Testes e apresentação | testes, revisão, roteiro e vídeo | Gabriel |

Todos devem revisar os artefatos clínicos e o vídeo; a divisão é operacional, não individualiza a autoria acadêmica.

## Cronograma de referência

| Período | Foco |
|---|---|
| 03–09/09 | planejamento, repositório, critérios e divisão |
| 10–16/09 | relatos, mapa de conhecimento e dataset de risco |
| 17–23/09 | extração, TF-IDF, modelos e testes |
| 24–30/09 | métricas, vieses, documentação e melhorias |
| 01–04/10 | revisão cruzada e gravação do vídeo |
| 05–06/10 | auditoria do upload, links e entrega antecipada |
| 07/10 | margem de segurança, não data-alvo de trabalho |

## Decisões ainda necessárias

1. Confirmar a divisão de responsáveis com o grupo.
2. Escolher se os opcionais “Ir Além” serão executados após a trilha obrigatória estar estável.
3. Definir plataforma de gravação e narrador do vídeo.
4. Confirmar o horário exato de fechamento na FIAP.

## Recomendação sobre os opcionais

Prioridade: primeiro assegurar os 10 pontos obrigatórios. Depois, executar o portal React como principal diferencial visual. A MLP com ECG acrescenta maior risco de prazo e de interpretação dos dados; só deve entrar se a parte obrigatória estiver concluída e validada.

