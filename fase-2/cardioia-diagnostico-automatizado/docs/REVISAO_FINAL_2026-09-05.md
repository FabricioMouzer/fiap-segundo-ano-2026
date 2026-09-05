# Revisão final técnica — 05/09/2026

## Resultado

O núcleo obrigatório da Fase 2 está implementado e reproduzível. Os cinco critérios técnicos têm evidências verificáveis, correspondentes a 8 pontos de peso no barema. O sexto critério, de 2 pontos, só se encerra com vídeo de até quatro minutos no YouTube como não listado e link no README. A publicação, revisão coletiva e submissão à FIAP permanecem pendentes.

Fonte dos requisitos: enunciado da atividade da Fase 2 fornecido pela equipe, período 03/09 a 07/10/2026. Não foi usado o prazo nem o barema da Fase 1 para avaliar esta entrega.

## Estado encontrado

A branch principal no início desta revisão era `a9c78fa` (PR7). Já continha TXT10, mapa45, corpus80, extrator, notebook, métricas, análise de quatro erros, matriz e roteiro. Não havia PR aberto. Esses componentes foram preservados e revisados, sem refazer o corpus.

## Correções concluídas

| Achado real | Correção | Evidência |
|---|---|---|
| Executor descartava outputs do notebook | persistência de stdout, tabelas e figuras após execução completa | notebook com 10 células executadas, 9 com saídas e 2 figuras |
| Negação podia usar primeira ocorrência e atravessar contexto | verificação por ocorrência, oração e enumeração | novos testes de regressão no extrator |
| Continuidade Fase 1 apenas conceitual | leitura dos arquivos originais, análise de representação e vocabulário | CONTINUIDADE_FASE1.md, JSON, dois CSVs e hashes |
| Documentação ainda apresentava código pronto como trabalho futuro | revisão do README, visão geral, plano, matriz e checklist | documentos coerentes com o estado executado |
| Evidências não preservavam todas as previsões/ambiente | exportação das 20 previsões, gráficos, manifesto e versões executadas | data/processed e requirements-validado.txt |
| Fase 1 descrevia incorretamente tipos de arquivo e códigos | correções pontuais no README e dicionário | dois TXT contextuais + dois PDFs; valores reais dos rótulos |

Os dados, scripts geradores e arquivos de origem da Fase 1 foram preservados. As 80 frases da Fase 2 também permaneceram iguais. Não houve tuning para elevar resultados nem remoção de exemplos difíceis.

## Verificações executadas

- 19 testes aprovados: 15 do núcleo e 4 da continuidade.
- 80 frases únicas em 40 grupos; 40 de cada classe.
- 60 frases/30 grupos no treino e 20 frases/10 grupos no teste; grupos disjuntos.
- TF-IDF ajustado apenas no treino.
- Regressão Logística: acurácia, precisão, recall e F1 de alto risco de 80%.
- Árvore de Decisão: acurácia de 30%, recall de alto risco de 20%.
- Quatro erros da regressão: dois falsos negativos e dois falsos positivos.
- Duas execuções com notebook, CSVs, gráficos e manifesto idênticos; timestamp das métricas excluído da comparação.
- Arquivos do notebook sem erros gravados e gráficos legíveis.

A validação usou um clone novo e as bibliotecas já instaladas no ambiente, registradas no manifesto. Não foi alegada instalação integral em ambiente vazio. As versões executadas são as de requirements-validado.txt, não as do arquivo histórico requirements.txt.

## Continuidade acadêmica

A Parte 2 do enunciado pede montar uma base simulada de frases rotuladas. O corpus de 80 frases cumpre essa finalidade. Em paralelo, os dados da Fase 1 foram efetivamente reutilizados para NLP exploratório e análise de representação/vieses. Não transformamos o rótulo de perfil sintético dos 150 registros em rótulo de triagem aguda.

A base anterior contém 143 rótulos majoritários e 7 minoritários; suas diferenças por sexo/idade são consequências da simulação e não prevalências reais. A auditoria dos TXT usa resumos contextuais, não relatos de pacientes. ECGs, PDFs e XLSX não são entradas do modelo textual.

## Limites e pendências reais

O experimento é pequeno, sintético e utiliza uma divisão fixa para comparação de modelos; não há validação clínica ou teste externo independente após a escolha do modelo. O extrator ainda tem regras limitadas de linguagem. A demonstração web anterior não foi sincronizada nesta revisão e não comprova todos os requisitos opcionais do portal React.

Para encerrar a entrega: publicar o vídeo não listado, inserir/testar o link, revisar com o grupo e submeter à FIAP guardando comprovante. Os opcionais React completo e MLP/Keras não são declarados concluídos. Prazo: 07/10/2026; horário a conferir na plataforma.

## Materiais preparados para a equipe

Apresentação de 13 slides em PPTX editável e PDF com links. Vídeo técnico legendado de 3min40/1080p,11 etapas e saídas reais, com decodificação validada. A publicação no YouTube não listado segue pendente de aprovação.
