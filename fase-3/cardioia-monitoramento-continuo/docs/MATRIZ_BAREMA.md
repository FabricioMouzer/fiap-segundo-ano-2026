# Matriz de atendimento ao barema — Fase 3

Estado inicial. As colunas distinguem implementação no repositório de evidência produzida por execução.

| Critério | Peso | Estado atual | Evidência necessária para encerrar |
|---|---:|---|---|
| Leitura de sensores | 2 | Código e circuito preparados | Wokwi executado com DHT22 e BPM variando |
| Resiliência offline | 2 | Buffer circular e botão implementados | Log mostrando fila crescer e sincronizar |
| MQTT e broker | 2 | Tópicos e cliente configurados | Mensagens reais recebidas pelo broker/Node-RED |
| Dashboard e alertas | 2 | Flow JSON preparado | Importação, deploy, gráfico, gauge e alerta visíveis |
| Documentação | 2 | Documentação inicial produzida | Revisão da equipe, links e capturas finais |

## Condições de conclusão

Um item somente muda para **verificado** quando a evidência indicada estiver disponível e acessível. Código presente não comprova execução. Captura isolada não substitui link ou export quando o enunciado exigir ambos.

## Fora do núcleo obrigatório

- SPIFFS em hardware físico: “Ir Além”, sem peso obrigatório no simulador.
- REST e e-mail: Ir Além 1.
- Regressão Logística versus rede neuromórfica: Ir Além 2.
- Vídeo de até quatro minutos: obrigatório somente no Ir Além 2, conforme o enunciado fornecido.

