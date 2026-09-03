# Roteiro final do vídeo — CardioIA Fase 2

## Configuração

- **Duração-alvo:** 3 minutos e 35 segundos a 3 minutos e 50 segundos.
- **Formato:** horizontal, 16:9, mínimo de 1080p.
- **Publicação:** YouTube como **não listado**.
- **Apresentação:** gravação de tela com narração ou legenda.
- **Fonte oficial:** repositório público e arquivos executados localmente.
- **Regra:** não utilizar dados reais de pacientes.

## Preparação antes de gravar

1. Fechar notificações, e-mails e arquivos pessoais.
2. Aumentar o zoom do navegador e do editor para facilitar a leitura.
3. Deixar abertas somente estas páginas:
   - README do projeto;
   - `data/raw/relatos_sintomas.txt`;
   - `data/raw/mapa_conhecimento.csv`;
   - `data/processed/resultados_extrator.csv`;
   - notebook `classificador_risco_tfidf.ipynb`;
   - `docs/ANALISE_ERROS_MODELO.md`;
   - portal demonstrativo.
4. Preparar o terminal na pasta `fase-2/cardioia-diagnostico-automatizado`.
5. Fazer um teste de áudio de 10 segundos.

## Roteiro cronometrado

### 0:00–0:20 — Abertura

**Mostrar:** título do projeto e README.

**Narração:**

> Olá. Somos a equipe responsável pelo CardioIA. Nesta segunda fase, desenvolvemos um módulo acadêmico para interpretar relatos sintéticos de sintomas, extrair informações por meio de um mapa de conhecimento e classificar textos como baixo ou alto risco. A solução é educacional e não realiza diagnóstico médico.

### 0:20–0:55 — Dados da Parte 1

**Mostrar:** `relatos_sintomas.txt` e `mapa_conhecimento.csv`.

**Narração:**

> A primeira parte começa com dez relatos completos e variados. Cada relato informa o sintoma, quando ele começou e como afetou a rotina simulada do paciente. O mapa de conhecimento possui quarenta e cinco expressões associadas a sintomas, possíveis condições e níveis de alerta. Todos os dados foram produzidos de forma sintética, preservando privacidade e rastreabilidade.

### 0:55–1:25 — Extração de sintomas

**Mostrar:** terminal e depois `resultados_extrator.csv`.

**Executar:**

```bash
python src/extrator_sintomas.py
```

**Narração:**

> O código normaliza os textos, procura expressões completas e considera negações simples. Ao encontrar uma correspondência, apresenta o sintoma, uma associação educacional e o nível de alerta. Todos os dez relatos geraram pelo menos um achado. Os resultados também foram exportados para CSV, facilitando a leitura e a auditoria.

### 1:25–2:10 — Classificador com TF-IDF

**Mostrar:** dataset e células principais do notebook.

**Narração:**

> Na segunda parte, criamos uma base com oitenta frases: quarenta de baixo risco e quarenta de alto risco. O TF-IDF transforma os textos em vetores numéricos dentro do pipeline de treinamento. A divisão entre treino e teste utiliza grupos, impedindo que variações da mesma frase apareçam nos dois conjuntos. Foram comparadas Regressão Logística e Árvore de Decisão.

### 2:10–2:50 — Resultados e análise de erros

**Mostrar:** métricas, matriz de confusão e `ANALISE_ERROS_MODELO.md`.

**Narração:**

> A Regressão Logística apresentou o melhor resultado: oitenta por cento de acurácia e oitenta por cento de recall para alto risco. A Árvore de Decisão foi mantida como comparação técnica. Registramos de forma transparente quatro previsões incorretas: dois falsos positivos e dois falsos negativos, concentrados em dois grupos linguísticos. Esses erros mostram a limitação do TF-IDF para compreender contexto e reforçam que o protótipo não possui validade clínica.

### 2:50–3:15 — Testes e reprodução

**Mostrar:** terminal.

**Executar:**

```bash
python -m unittest discover -s tests -v
python src/gerar_evidencias.py
```

**Narração:**

> O projeto possui oito testes automatizados. Eles verificam a estrutura e o equilíbrio dos dados, a ausência de duplicidades, a normalização, o tratamento de negação e a extração dos dez relatos. O pipeline pode ser reproduzido usando apenas as instruções do README.

### 3:15–3:38 — Demonstração e governança

**Mostrar:** portal demonstrativo e aviso educacional.

**Narração:**

> O portal permite visualizar o fluxo usando relatos sintéticos e os parâmetros exportados do modelo validado. A interface não substitui os arquivos obrigatórios. Como limitações, reconhecemos o tamanho reduzido da base, os padrões linguísticos controlados e a ausência de validação clínica externa.

### 3:38–3:50 — Encerramento

**Mostrar:** README, equipe e endereço do repositório.

**Narração:**

> O código, os dados, os resultados e a documentação estão disponíveis no repositório público. Este foi o CardioIA Fase 2: uma entrega reproduzível, explicável e desenvolvida com responsabilidade. Obrigado.

## Título e descrição para o YouTube

**Título:**

`CardioIA — Fase 2 | Diagnóstico Automatizado com NLP e Machine Learning`

**Descrição:**

```text
Demonstração acadêmica da Fase 2 do projeto CardioIA, desenvolvida pela equipe da FIAP.

O protótipo utiliza dados sintéticos, mapa de conhecimento, TF-IDF e modelos de classificação para simular apoio à triagem textual.

Repositório:
https://github.com/FabricioMouzer/fiap-segundo-ano-2026/tree/main/fase-2/cardioia-diagnostico-automatizado

Aviso: projeto exclusivamente educacional. Não realiza diagnóstico médico e não deve ser utilizado em atendimento clínico.
```

## Validação após publicar

- [ ] duração máxima de 4 minutos;
- [ ] resolução e áudio compreensíveis;
- [ ] visibilidade definida como **não listado**;
- [ ] link aberto com sucesso em janela anônima;
- [ ] link inserido na seção “Vídeo de demonstração” do README;
- [ ] nomes e RMs conferidos;
- [ ] nenhuma informação pessoal ou credencial aparece na gravação.
