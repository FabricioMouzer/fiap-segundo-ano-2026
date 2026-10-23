# Relatório — armazenamento e processamento local

## 1. Objetivo

A primeira parte do CardioIA Fase 3 simula um dispositivo vestível capaz de coletar continuamente sinais vitais, realizar verificações locais e manter temporariamente os dados quando a comunicação estiver indisponível. O foco é demonstrar Edge Computing: decisões e armazenamento próximos da origem dos dados, reduzindo a dependência de uma conexão permanente.

## 2. Componentes simulados

O circuito usa um ESP32, um DHT22, um potenciômetro, um botão e um LED. O DHT22 fornece temperatura e umidade. Embora produza duas grandezas, ele é considerado um único sensor, conforme o enunciado. O segundo sensor é representado pelo potenciômetro, cuja leitura analógica de 0 a 4095 é convertida para uma frequência cardíaca simulada entre 40 e 180 bpm.

O botão vermelho controla a falha de comunicação: pressionado, força o modo offline; liberado, permite nova tentativa de Wi-Fi e MQTT. O LED vermelho representa um alerta local e permanece aceso quando temperatura, BPM ou leitura do DHT22 ultrapassam as regras configuradas.

## 3. Fluxo de funcionamento

A cada cinco segundos o ESP32 lê os sensores, valida os valores e cria uma estrutura com sequência, tempo de execução, temperatura, umidade, BPM e código de alerta. A amostra entra primeiro no buffer local, independentemente do estado da conexão. Essa decisão evita dois caminhos diferentes de persistência e reduz o risco de uma leitura ser perdida entre a coleta e a tentativa de transmissão.

Quando Wi-Fi e MQTT estão disponíveis, o firmware retira as amostras da fila em ordem cronológica e as publica em JSON. A remoção ocorre somente depois que a biblioteca MQTT aceita a publicação. Em uma desconexão, a aquisição continua e o Monitor Serial registra a origem, os valores, o alerta, o tamanho da fila e a quantidade de amostras substituídas.

## 4. Estratégia de resiliência

O armazenamento é um buffer circular com 720 posições. No intervalo adotado, isso representa uma hora de dados offline. O limite impede crescimento indefinido e facilita estimar o consumo de memória. Caso a fila fique cheia, o registro mais antigo é substituído pelo mais recente e o contador `dropped_samples` aumenta. Para um protótipo de monitoramento, privilegiar a janela mais atual facilita a retomada do contexto quando a conectividade retorna.

A sincronização é limitada a 20 mensagens por ciclo do programa. O objetivo é evitar que uma fila extensa bloqueie por muito tempo a coleta de novas leituras. O firmware intercala a manutenção da conexão com lotes curtos de sincronização.

## 5. Relação com SPIFFS

O enunciado informa que o SPIFFS no ambiente simulado é volátil e que o item não integra a pontuação obrigatória. Por esse motivo, a versão Wokwi usa memória RAM e o Monitor Serial como evidência da resiliência durante a execução. Em hardware físico, uma evolução possível seria gravar uma fila persistente em LittleFS, SPIFFS ou cartão microSD e acrescentar verificação de integridade e desgaste da memória.

## 6. Limitações

O buffer em RAM não sobrevive ao encerramento da simulação. O valor `uptime_ms` também reinicia junto com o ESP32. A confirmação local da biblioteca MQTT não garante que a mensagem tenha sido persistida pelo broker, pois a publicação utiliza QoS 0. Essas limitações devem permanecer explícitas na demonstração e não invalidam o objetivo acadêmico de simular coleta offline e sincronização posterior.

## 7. Evidências a produzir

Para concluir esta parte, a equipe deverá registrar o link público do Wokwi, capturar o circuito, demonstrar no Monitor Serial o crescimento da fila com o botão pressionado e mostrar a sincronização após liberar a conexão. Nenhuma dessas evidências é declarada como concluída antes da execução real.

