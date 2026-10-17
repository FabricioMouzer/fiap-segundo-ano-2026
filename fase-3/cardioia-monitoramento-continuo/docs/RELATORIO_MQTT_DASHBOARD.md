# Relatório — MQTT, Fog/Cloud Computing e dashboard

## 1. Objetivo

A segunda parte conecta o ESP32 simulado a um broker MQTT e utiliza o Node-RED como camada de integração e visualização. O fluxo representa o percurso completo captura → processamento local → transmissão → visualização → alerta, sempre com dados sintéticos.

## 2. Comunicação MQTT

MQTT foi escolhido por ser um protocolo leve baseado em publicação e assinatura. O ESP32 não precisa conhecer o endereço do dashboard: publica mensagens em tópicos, enquanto o Node-RED assina os tópicos relevantes. Essa separação reduz o acoplamento entre o dispositivo e a interface.

O protótipo utiliza três tópicos. `telemetria` recebe todas as amostras; `alerta` recebe apenas ocorrências que violam uma regra; `status` registra conexão e tamanho da fila. O broker público HiveMQ é usado sem autenticação apenas para facilitar a simulação. O prefixo do projeto e o identificador do dispositivo reduzem colisões, mas não transformam o canal em privado.

Cada mensagem de telemetria contém identificador, sequência, tempo de execução, temperatura, umidade, BPM, código e rótulo de alerta, origem e situação do buffer. O formato JSON torna a inspeção simples e permite que o Node-RED converta o payload diretamente em objeto.

## 3. Processamento no Node-RED

O flow recebe a telemetria, converte o JSON e verifica a presença dos campos obrigatórios. Valores numéricos inválidos ou mensagens incompletas são descartados com aviso. Depois da validação, uma função produz quatro saídas independentes:

1. valor de BPM para o gráfico temporal;
2. temperatura para o gauge;
3. texto e cor para o indicador de alerta;
4. resumo da origem, fila, descartes e sequência.

Outro ramo recebe o tópico de status e apresenta o estado declarado pelo dispositivo. A separação torna mais fácil diagnosticar se a ausência de pontos no gráfico é causada por falha do dispositivo, do broker ou do tratamento da telemetria.

## 4. Dashboard e alertas

O gráfico apresenta a evolução dos batimentos simulados. O gauge usa faixa de 30 a 42 °C, com transição visual próxima do limite acadêmico de 38 °C. O indicador central fica verde para condição normal e vermelho para qualquer alerta. Também são exibidas informações operacionais da sincronização.

As regras são executadas no Edge, antes da publicação. Isso permite acender o LED mesmo quando a comunicação está indisponível. O Node-RED apenas representa o resultado recebido. Uma evolução possível seria repetir as regras na camada Fog e comparar os resultados para detectar inconsistências.

## 5. Segurança e privacidade

A porta 1883 não usa TLS e o broker é público. Portanto, somente valores sintéticos podem ser publicados. Um projeto real exigiria broker privado, TLS, autenticação individual por dispositivo, rotação de credenciais, autorização por tópico, logs de acesso e política de retenção. Identificadores de pacientes não devem integrar os tópicos nem os payloads.

## 6. Testes planejados

A validação funcional deve cobrir pelo menos:

- temperatura e BPM normais;
- BPM abaixo de 50;
- BPM acima de 120;
- temperatura acima de 38 °C;
- falha ou valor inválido do DHT22;
- desconexão forçada com crescimento do buffer;
- reconexão com mensagens marcadas como `buffered`;
- payload incompleto descartado pelo Node-RED;
- reinício do dashboard e nova assinatura do broker.

## 7. Limitações e conclusão

O histórico do dashboard não é banco de dados permanente. A demonstração usa QoS 0 e não confirma processamento fim a fim. Ainda assim, a arquitetura atende ao objetivo de demonstrar o fluxo entre Edge, nuvem e Fog. A conclusão acadêmica só será marcada após importar o flow, executar o Wokwi, observar mensagens reais e registrar capturas legíveis.

