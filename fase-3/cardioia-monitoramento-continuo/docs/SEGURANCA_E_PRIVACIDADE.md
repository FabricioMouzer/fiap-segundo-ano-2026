# Segurança, privacidade e responsabilidade

## Escopo acadêmico

Todos os valores do projeto são sintéticos. O sistema não possui cadastro de pacientes, não recebe prontuários e não deve ser usado para orientar conduta médica.

## Riscos identificados

| Risco | Consequência | Controle adotado ou recomendado |
|---|---|---|
| Broker público sem TLS | Leitura ou injeção de mensagens por terceiros | Somente dados sintéticos; tópico com prefixo específico |
| Regras fixas de alerta | Interpretação clínica indevida | Aviso educacional e limites declarados como demonstração |
| Buffer limitado | Perda das amostras mais antigas | Contador de descartes e capacidade documentada |
| QoS 0 | Mensagem pode não chegar ao broker | Amostra só sai após aceite local; limitação explícita |
| Identificador previsível | Colisão com outro experimento | Prefixo CardioIA e dispositivo; testar tópico antes da apresentação |
| Dashboard sem autenticação local | Acesso indevido na rede | Executar em ambiente controlado; não expor publicamente |
| Dados inválidos | Gráficos e alertas incorretos | Validação no ESP32 e no flow Node-RED |

## Requisitos para uma solução real

Uma aplicação médica real exigiria, no mínimo, TLS, autenticação mútua ou credenciais por dispositivo, autorização por tópico, firmware assinado, armazenamento criptografado, sincronização temporal confiável, trilha de auditoria, gestão de consentimento e avaliação clínica. Também seriam necessárias análise de risco, conformidade regulatória e validação de hardware e software.

## Dados que não podem ser publicados

- nome, CPF, e-mail ou telefone;
- número de prontuário;
- localização;
- dados clínicos reais;
- credenciais do broker;
- tokens, senhas ou chaves privadas.

