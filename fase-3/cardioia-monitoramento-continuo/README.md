# CardioIA — Fase 3: Monitoramento Contínuo com IoT

Protótipo acadêmico de monitoramento contínuo de sinais vitais simulados, integrando Edge Computing, MQTT e visualização em Node-RED.

> Uso exclusivamente educacional. O protótipo não realiza diagnóstico, não substitui avaliação profissional e utiliza somente dados sintéticos.

## Estado do projeto

**Base técnica inicial implementada em branch de desenvolvimento.** O código, o circuito e o fluxo do dashboard ainda precisam ser executados no Wokwi e no Node-RED antes de serem considerados entregues.

**Prazo:** aguardando registro da data e do horário exatos exibidos no Portal FIAP. O texto do enunciado arquivado no projeto não contém essa informação.

## Escopo obrigatório

| Critério | Peso | Implementação preparada | Evidência ainda necessária |
|---|---:|---|---|
| Leitura de sensores | 2 | DHT22 + potenciômetro simulando BPM | Link e captura do Wokwi em execução |
| Resiliência offline | 2 | Buffer circular limitado, reconexão e sincronização | Demonstração offline/online no Monitor Serial |
| MQTT e broker | 2 | Publicação JSON em três tópicos | Log real do broker e recebimento no Node-RED |
| Dashboard e alertas | 2 | Flow importável com gráfico, gauge e alerta | Capturas do dashboard funcionando |
| Documentação | 2 | README, relatórios, arquitetura, barema e checklist | Revisão coletiva e PDF final, se exigido |

Os pesos representam o barema informado, não uma nota garantida.

## Arquitetura

```text
DHT22 + potenciômetro (BPM)
            │
            ▼
       ESP32 / Wokwi
       ├─ regras de alerta
       ├─ buffer circular offline
       └─ sincronização após reconexão
            │ MQTT / JSON
            ▼
       Broker HiveMQ público
            │
            ▼
          Node-RED
       ├─ gráfico de BPM
       ├─ gauge de temperatura
       ├─ indicador de alerta
       └─ estado do buffer/conexão
```

Consulte [a arquitetura detalhada](docs/ARQUITETURA.md).

## Sensores e controles

- **DHT22:** temperatura e umidade; conta como um sensor segundo o enunciado.
- **Potenciômetro:** representa um sensor cardíaco, mapeando a leitura analógica para 40–180 bpm.
- **Botão OFFLINE:** enquanto pressionado, força a interrupção da conectividade para demonstrar a resiliência.
- **LED vermelho:** acende quando uma regra de alerta é ativada.

## Estratégia de resiliência

Uma amostra é coletada a cada 5 segundos e inserida em um buffer circular de 720 posições, equivalente a até uma hora de dados. Quando a conectividade volta, o firmware envia as amostras mais antigas primeiro. Uma amostra só é removida da fila quando a função de publicação confirma que o payload foi aceito pelo cliente MQTT.

Se o limite for atingido, a amostra mais antiga é substituída e o contador `dropped_samples` é incrementado. Essa decisão mantém o consumo de memória previsível e privilegia os dados mais recentes.

## Tópicos MQTT

```text
cardioia/fase3/rm566777/cardioia-esp32-01/telemetria
cardioia/fase3/rm566777/cardioia-esp32-01/alerta
cardioia/fase3/rm566777/cardioia-esp32-01/status
```

Exemplo de telemetria:

```json
{
  "device_id": "cardioia-esp32-01",
  "sequence": 42,
  "uptime_ms": 210000,
  "temperature_c": 36.7,
  "humidity_pct": 58.2,
  "bpm": 82,
  "alert_code": 0,
  "source": "live"
}
```

## Limites acadêmicos configurados

- BPM abaixo de 50: frequência reduzida.
- BPM acima de 120: frequência elevada.
- Temperatura acima de 38 °C: temperatura elevada.
- Falha do DHT22: alerta técnico.

Os limites são parâmetros de demonstração e não devem ser interpretados como protocolo clínico.

## Como executar no Wokwi

1. Crie um projeto ESP32 no Wokwi.
2. Copie os arquivos da pasta [`wokwi`](wokwi/).
3. Confirme as bibliotecas de [`libraries.txt`](wokwi/libraries.txt).
4. Inicie a simulação e abra o Monitor Serial em 115200 baud.
5. Varie o potenciômetro e os valores do DHT22.
6. Pressione o botão vermelho para forçar o modo offline.
7. Solte o botão e observe a sincronização das amostras acumuladas.

O broker público é adequado somente a dados sintéticos. Não publique informações pessoais ou clínicas reais.

## Como executar o dashboard

1. Siga o guia [`docs/INSTALACAO_NODE_RED_WINDOWS.md`](docs/INSTALACAO_NODE_RED_WINDOWS.md).
2. Importe [`node-red/cardioia-dashboard-flow.json`](node-red/cardioia-dashboard-flow.json).
3. Faça o deploy.
4. Abra `/ui` no endereço do Node-RED.
5. Confirme o recebimento do tópico `cardioia/fase3/rm566777/cardioia-esp32-01/#`.

## Documentação

- [Relatório — Edge Computing](docs/RELATORIO_EDGE_COMPUTING.md)
- [Relatório — MQTT e dashboard](docs/RELATORIO_MQTT_DASHBOARD.md)
- [Arquitetura](docs/ARQUITETURA.md)
- [Segurança e privacidade](docs/SEGURANCA_E_PRIVACIDADE.md)
- [Matriz do barema](docs/MATRIZ_BAREMA.md)
- [Checklist de entrega](docs/CHECKLIST_ENTREGA.md)

## Continuidade do CardioIA

- **Fase 1:** base cardiovascular sintética, governança e rastreabilidade.
- **Fase 2:** extração textual de sintomas, classificação de risco, testes e análise de erros.
- **Fase 3:** captura contínua simulada, processamento local, comunicação MQTT, visualização e alertas.

A Fase 3 reutiliza os princípios de privacidade, transparência, rastreabilidade e validação das fases anteriores. Os modelos da Fase 2 não são usados para tomar decisões clínicas neste firmware.

## Equipe confirmada

| Integrante | RM |
|---|---|
| Fabrício Mouzer Brito | RM566777 |
| Enzo Nunes Castanheira Gloria da Silva | RM567599 |
| Larissa Nunes Moreira Reis | RM568280 |
| Gabriel Rapozo Guimarães Soares | RM568480 |

