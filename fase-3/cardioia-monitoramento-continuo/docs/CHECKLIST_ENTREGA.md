# Checklist de entrega — Fase 3

## Informações administrativas

- [x] confirmar os integrantes e RMs desta fase
- [ ] registrar prazo e horário exatos exibidos no Portal FIAP
- [ ] confirmar formato exigido no ambiente FIAP
- [ ] registrar divisão de responsabilidades

## Parte 1 — Edge Computing

- [x] circuito-base ESP32 criado
- [x] DHT22 incluído
- [x] segundo sensor simulado por potenciômetro/BPM incluído
- [x] código comentado criado
- [x] buffer circular limitado implementado
- [x] contador de descarte implementado
- [x] botão para forçar modo offline implementado
- [x] reconexão e sincronização implementadas no código
- [ ] projeto importado e executado no Wokwi
- [ ] diagrama visualmente conferido no Wokwi
- [ ] leituras do DHT22 validadas
- [ ] faixa de BPM validada
- [ ] log do período offline capturado
- [ ] log da sincronização capturado
- [ ] link público do Wokwi testado sem login
- [x] relatório inicial de Edge Computing redigido
- [ ] relatório revisado após os testes reais

## Parte 2 — MQTT e dashboard

- [x] cliente MQTT implementado
- [x] tópicos e contrato JSON documentados
- [x] flow inicial do Node-RED criado
- [x] gráfico de BPM configurado
- [x] gauge de temperatura configurado
- [x] alerta visual configurado
- [x] estado do buffer e conexão incluído
- [ ] publicação real no broker validada
- [ ] flow importado sem erro
- [ ] Node-RED instalado e inicializado no Windows
- [ ] pacote `node-red-dashboard` instalado para compatibilidade com o flow acadêmico
- [ ] dashboard executado
- [ ] condições normal, BPM alto, BPM baixo e temperatura alta testadas
- [ ] prints legíveis capturados
- [ ] export final do Node-RED conferido
- [x] relatório inicial de MQTT/dashboard redigido
- [ ] relatório revisado após os testes reais

## Qualidade e entrega

- [x] nenhuma credencial real versionada
- [x] dados declarados como sintéticos
- [x] limitações de QoS, tempo e persistência registradas
- [ ] código compilado no ambiente-alvo
- [ ] arquivos estáticos validados novamente
- [ ] README atualizado com evidências reais
- [ ] matriz do barema atualizada sem contradições
- [ ] revisão coletiva concluída
- [ ] todos os links testados sem login
- [ ] versão final/tag criada
- [ ] entrega realizada na FIAP
- [ ] comprovante preservado

## Regra de consistência

Antes do envio, pesquisar no repositório por `pendente`, `aguardando`, `[ ]` e `TODO`. Cada ocorrência deve permanecer como limitação consciente ou ser resolvida. README, matriz e checklist devem declarar o mesmo estado.

