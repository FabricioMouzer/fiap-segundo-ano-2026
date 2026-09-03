# Matriz de atendimento ao barema — CardioIA Fase 2

Esta matriz relaciona cada critério obrigatório do enunciado às evidências existentes no repositório. A pontuação indicada é uma estimativa de prontidão, não uma garantia de nota.

## Resumo executivo

| Situação | Pontos do barema |
|---|---:|
| Evidências técnicas implementadas | 8/10 |
| Pendente: vídeo e link público não listado | 2/10 |
| Potencial após concluir e validar o vídeo | 10/10 |

## Rastreabilidade dos critérios

| Critério | Pontos | Situação | Evidências | Verificação |
|---|---:|---|---|---|
| Relatos e mapa de conhecimento organizados | 2 | Concluído | `data/raw/relatos_sintomas.txt`, `data/raw/mapa_conhecimento.csv`, `data/DICIONARIO_DADOS.md` | 10 relatos; 45 expressões mapeadas |
| Código de extração funcional | 2 | Concluído | `src/extrator_sintomas.py`, `data/processed/resultados_extrator.json`, `data/processed/resultados_extrator.csv` | todos os relatos geram achados; testes automatizados aprovados |
| Dataset criado corretamente | 1 | Concluído | `data/raw/dataset_risco.csv`, `tests/test_dados.py` | 80 frases; 40 de baixo e 40 de alto risco; sem duplicatas |
| Classificador treinado e testado | 2 | Concluído | `notebooks/classificador_risco_tfidf.ipynb`, `data/processed/metricas_modelos.json`, `data/processed/erros_regressao_logistica.csv` | TF-IDF em pipeline; separação por grupo; métricas e erros registrados |
| Documentação e repositório público | 1 | Concluído | `README.md`, pasta `docs/` e repositório público | instalação, execução, limitações, integrantes e RMs documentados |
| Vídeo de até 4 minutos, não listado, com link no README | 2 | Pendente | `docs/ROTEIRO_VIDEO.md` e seção “Vídeo de demonstração” do `README.md` | gravar, publicar, inserir o link e testar em janela anônima |

## Evidências técnicas consolidadas

- 8 de 8 testes automatizados aprovados.
- Pipeline executado de ponta a ponta com 60 amostras de treino e 20 de teste.
- Separação por `grupo_id`, impedindo que variações da mesma frase apareçam em treino e teste.
- Regressão Logística: 80% de acurácia e 80% de recall de alto risco.
- Quatro erros registrados: dois falsos positivos e dois falsos negativos, concentrados em dois grupos linguísticos.
- Dados exclusivamente sintéticos e limitações explicitadas.

## Condição de encerramento

A entrega obrigatória estará pronta para submissão quando:

1. o vídeo tiver no máximo quatro minutos;
2. estiver publicado no YouTube como **não listado**;
3. o link estiver no `README.md`;
4. o link abrir em janela anônima;
5. o repositório for clonado e executado novamente em ambiente limpo;
6. a equipe conferir nomes, RMs e o arquivo final antes do envio à FIAP.

## Itens “Ir Além”

O portal React e a rede neural com ECG são extensões opcionais, com entregáveis próprios. Eles devem permanecer fora do caminho crítico até a conclusão do vídeo obrigatório e da auditoria final.

