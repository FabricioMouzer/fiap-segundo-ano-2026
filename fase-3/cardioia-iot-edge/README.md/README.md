# CardioIA - Monitorização IoT de Sinais Vitais (Fase 3)

Projeto desenvolvido para a disciplina de IoT e Inteligência Artificial (FIAP), focado na simulação, recolha e visualização de dados clínicos através de arquitetura Edge e Fog/Cloud Computing.

## 🔗 Links e Entregáveis Principais
* **Simulação Interativa no Wokwi:** [https://wokwi.com/projects/479502357195128833]
* **Código C++ Comentado (ESP32):** [`/wokwi/sketch.ino`](./wokwi/sketch.ino)
* **Circuito Virtual (JSON):** [`/wokwi/diagram.json`](./wokwi/diagram.json)
* **Export do Fluxo Node-RED:** [`/node-red/flow.json`](./node-red/flow.json)
* **Relatório 1 (Fluxo e Resiliência Edge):** [`/docs/Relatorio_1_Edge_Resiliencia.pdf`](./docs/Relatorio_1_Edge_Resiliencia.pdf)
* **Relatório 2 (Comunicação MQTT e Dashboard):** [`/docs/Relatorio_2_MQTT_Dashboard.pdf`](./docs/Relatorio_2_MQTT_Dashboard.pdf)

## 📌 Arquitetura do Sistema
1. **Edge Computing (ESP32):** Recolha contínua de Temperatura (DHT22 no pino 15) e Batimentos Cardíacos (Pushbutton com interrupção de hardware no pino 4). Possui trava biológica (máximo de 220 BPM) e resiliência offline com buffer em memória RAM para até 20 leituras em caso de queda de Wi-Fi.
2. **Protocolo MQTT:** Transmissão em formato JSON pelo tópico `cardioia/sinais` através do broker público `broker.hivemq.com` (porta TCP 1883).
3. **Fog/Cloud Computing (Node-RED):** Processamento em tempo real e exibição em dashboard clínico (`http://localhost:1880/ui`), com disparo automático de alertas críticos quando a temperatura ultrapassa 38 °C ou a frequência cardíaca supera 120 BPM.

## 🚀 Como Testar
1. Abra o link do Wokwi acima e dê **Play**. Ajuste a temperatura clicando sobre o sensor DHT22 e simule taquicardia clicando repetidamente no botão vermelho. Para testar a resiliência offline, digite `0` no Monitor Serial (derruba o Wi-Fi simulado) e depois `1` (restaura a rede e descarrega o buffer).
2. No terminal local, execute `node-red`, acesse `http://localhost:1880`, instale a paleta `node-red-dashboard`, importe o arquivo `node-red/flow.json` e clique em **Deploy**.
3. Visualize os sinais em tempo real em `http://localhost:1880/ui`.