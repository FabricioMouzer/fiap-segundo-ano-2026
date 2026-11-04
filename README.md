# FIAP — Segundo Ano — Inteligência Artificial

Repositório acadêmico central do ecossistema **CardioIA**, reunindo os estudos, projetos, códigos, bases sintéticas, testes e evidências desenvolvidos pela equipe ao longo do segundo ano do Tecnólogo em Inteligência Artificial da FIAP.

> **Aviso de governança e escopo acadêmico:** todos os projetos deste repositório têm finalidade exclusivamente educacional, utilizam dados sintéticos e não realizam diagnóstico, triagem real nem recomendação clínica. Não publicar credenciais, dados pessoais, prontuários, tokens ou materiais exclusivos da FIAP.

## Sumário Navegável

- [Propósito do Ecossistema CardioIA](#propósito-do-ecossistema-cardioia)
- [Equipe](#equipe)
- [Jornada CardioIA — Fases Concluídas](#jornada-cardioia--fases-concluídas)
  - [Fase 1 — Batimentos de Dados (`fase-1/cardioia-batimentos-de-dados`)](#fase-1--batimentos-de-dados)
  - [Fase 2 — Diagnóstico Automatizado (`fase-2/cardioia-diagnostico-automatizado`)](#fase-2--diagnóstico-automatizado)
  - [Fase 3 — Monitoramento Contínuo com IoT (`fase-3/CardioIA-Fase3-Monitoramento-IoT`)](#fase-3--monitoramento-contínuo-com-iot)
- [Organização do Repositório](#organização-do-repositório)
- [Padrão Acadêmico e Governança](#padrão-acadêmico-e-governança)

## Propósito do Ecossistema CardioIA

O **CardioIA** simula a evolução modular de uma plataforma inteligente voltada à cardiologia, conectando ciência e governança de dados, processamento de linguagem natural (NLP) com aprendizado de máquina supervisionado e monitoramento contínuo por Internet das Coisas (IoT) e Edge Computing. Cada fase reutiliza lições de governança, reprodutibilidade e validação automatizada para demonstrar como diferentes camadas tecnológicas se articulam em um ecossistema de saúde digital auditável.

## Equipe

| Integrante | RM |
|---|---|
| Fabrício Mouzer Brito | RM566777 |
| Enzo Nunes Castanheira Gloria da Silva | RM567599 |
| Larissa Nunes Moreira Reis | RM568280 |
| Gabriel Rapozo Guimarães Soares | RM568480 |

**Curso:** Tecnólogo em Inteligência Artificial — FIAP (2º Ano — 2026)

## Jornada CardioIA — Fases Concluídas

| Fase | Projeto | Diretório Principal | Estado |
|---|---|---|---|
| **Fase 1** | CardioIA — Batimentos de Dados | [`fase-1/cardioia-batimentos-de-dados/`](fase-1/cardioia-batimentos-de-dados/) | Concluída e validada |
| **Fase 2** | CardioIA — Diagnóstico Automatizado | [`fase-2/cardioia-diagnostico-automatizado/`](fase-2/cardioia-diagnostico-automatizado/) | Concluída e validada (19 testes aprovados) |
| **Fase 3** | CardioIA — Monitoramento Contínuo com IoT | [`fase-3/CardioIA-Fase3-Monitoramento-IoT/`](fase-3/CardioIA-Fase3-Monitoramento-IoT/) | Concluída e integrada ([repositório espelho com 41 commits](https://github.com/FabricioMouzer/CardioIA-Fase3-Monitoramento-IoT)) |

---

### Fase 1 — Batimentos de Dados

Preparação governada de três modalidades de dados cardiovasculares sintéticos e contextuais para fundar o ecossistema CardioIA:

- **Dados numéricos tabulares:** 150 registros sintéticos (`CSV` e `XLSX`) com 17 variáveis clínicas simuladas, dicionário de dados e análise de viés de geração.
- **Dados textuais (NLP):** textos contextuais baseados em obras históricas de domínio público (Project Gutenberg) e referências clínicas brasileiras sobre hipertensão.
- **Dados visuais (Visão Computacional):** 100 traçados sintéticos de ECG em alta resolução (`.png`) gerados matematicamente.
- **Acesso direto:** [`fase-1/cardioia-batimentos-de-dados/`](fase-1/cardioia-batimentos-de-dados/) (índice da fase em [`fase-1/README.md`](fase-1/README.md)).

### Fase 2 — Diagnóstico Automatizado

Extração estruturada de sintomas e classificação supervisionada de risco clínico a partir de relatos textuais sintéticos:

- **Extrator de sintomas por mapa de conhecimento:** identificação de achados em 10 relatos utilizando 45 expressões mapeadas, com tratamento de negação contextual e pontuação.
- **Classificação de risco com TF-IDF e Machine Learning:** avaliação comparativa entre Regressão Logística (80% de acurácia e recall de alto risco) e Árvore de Decisão em um corpus balanceado de 80 frases (40 grupos disjuntos com `StratifiedGroupKFold`).
- **Auditoria de continuidade e reprodutibilidade:** 19 testes automatizados (`unittest`), análise explícita dos 4 erros do modelo e vídeo técnico de demonstração publicado no YouTube.
- **Acesso direto:** [`fase-2/cardioia-diagnostico-automatizado/`](fase-2/cardioia-diagnostico-automatizado/).

### Fase 3 — Monitoramento Contínuo com IoT

Protótipo de dispositivo vestível cardiológico com computação de borda (Edge Computing), resiliência offline, telemetria MQTT e supervisão em tempo real:

- **Edge Computing e Resiliência Offline (Wokwi / ESP32):** leitura contínua de temperatura/umidade (`DHT22`) e batimentos cardíacos sintéticos (potenciômetro), classificação local de alertas e buffer circular FIFO em RAM para até `2.160` amostras durante quedas de conectividade.
- **Telemetria MQTT e Dashboard (HiveMQ + Node-RED):** publicação JSON versão 1 no broker HiveMQ com *Last Will and Testament (LWT)* e painel público em FlowFuse Dashboard 2.0 (hospedado no Render) com gráficos históricos, medidores e alertas visuais automáticos (`BPM ALTO`, `BPM BAIXO`, `TEMP ALTA` e `FALHA DO SENSOR`).
- **Acesso direto neste repositório:** [`fase-3/CardioIA-Fase3-Monitoramento-IoT/`](fase-3/CardioIA-Fase3-Monitoramento-IoT/).
- **Repositório espelho (histórico completo da equipe):** [`https://github.com/FabricioMouzer/CardioIA-Fase3-Monitoramento-IoT`](https://github.com/FabricioMouzer/CardioIA-Fase3-Monitoramento-IoT) — mantido como espelho e backup oficial onde constam os **41 commits detalhados** de desenvolvimento e auditoria de todas as etapas pela equipe.

---

## Organização do Repositório

- [`fase-1/`](fase-1/): Batimentos de Dados — construção da base multimodal sintética e governança em IA;
- [`fase-2/`](fase-2/cardioia-diagnostico-automatizado/): Diagnóstico Automatizado — extrator de sintomas, TF-IDF e classificadores supervisionados;
- [`fase-3/`](fase-3/CardioIA-Fase3-Monitoramento-IoT/): Monitoramento Contínuo com IoT — ESP32 no Wokwi, buffer offline FIFO, MQTT e dashboard Node-RED;
- `challenge/`: reservado para projetos Challenge;
- `global-solution/`: reservado para Global Solution e documentação relacionada.

## Padrão Acadêmico e Governança

Todo projeto do repositório é estruturado com:

1. **Objetivo e arquitetura** claramente delimitados ao contexto educacional;
2. **Fontes, dados sintéticos e contratos** rastreáveis por hashes e scripts determinísticos;
3. **Instruções completas de reprodução** e testes automatizados;
4. **Análise transparente de resultados, erros e limitações** (política de veracidade: nenhum item é dado como validado sem evidência correspondente versionada);
5. **Privacidade e segurança:** ausência total de dados clínicos reais, informações pessoais, senhas ou chaves de API.
