# Matriz de atendimento ao barema — CardioIA Fase 2

Revisão em 05/09/2026. Fonte: enunciado da atividade “Diagnóstico Automatizado — IA no Estetoscópio Digital”, período 03/09 a 07/10/2026, fornecido pela equipe. Pesos não representam nota garantida.

| Critério | Peso | Estado verificado | Evidência |
|---|---:|---|---|
| Relatos e mapa organizados | 2 | implementado | 10 relatos e 45 expressões em data/raw |
| Código de extração funcional | 2 | implementado e testado | src/extrator_sintomas.py; resultados_extrator.csv/json |
| Dataset correto | 1 | implementado e validado | 80 frases únicas, 40/40 classes, 40 grupos |
| Classificador treinado/testado | 2 | executado | notebook com 10 células executadas; métricas, 2 gráficos, 20 predições e 4 erros |
| Documentação e GitHub público | 1 | revisados | README, instruções, limites, autores e evidências |
| Vídeo até 4 min, YouTube não listado e link | 2 | publicação pendente | roteiro/arquivo não substituem link publicado |

## Evidências de qualidade

- 19 testes aprovados.
- 60 amostras/30 grupos de treino; 20 amostras/10 grupos de teste; zero grupos compartilhados.
- TF-IDF ajustado no treino; Regressão Logística 80% de acurácia e recall alto risco.
- Dois falsos negativos e dois falsos positivos mantidos na avaliação.
- Notebook, CSVs, gráficos e manifesto idênticos em duas execuções; timestamp das métricas não integra a comparação.
- Continuidade da Fase 1 executada com fontes/hashes, sem misturar seus rótulos com o corpus textual.

Os cinco critérios técnicos somam 8 pontos de peso no barema. Isso não é nota atribuída nem comprovação de submissão.

## Encerramento obrigatório

1. Verificar o vídeo técnico de até 4 min e publicar como não listado.
2. Inserir o link no README e abrir sem login.
3. Realizar revisão coletiva de método, nomes/RMs e limitações.
4. Confirmar horário final e enviar na FIAP até 07/10/2026, preservando comprovante.

## Opcionais

A demonstração de relatos não comprova login, pacientes, agendamentos e demais itens do portal “Ir Além 1”. Não foi entregue MLP/Keras com ECG público do “Ir Além 2”. Esses opcionais não integram os 10 pontos do barema obrigatório acima.
