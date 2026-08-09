# CardioIA — Fase 1: Batimentos de Dados

Projeto acadêmico do segundo ano do Tecnólogo em Inteligência Artificial da FIAP. Nesta fase, o grupo atua como uma equipe de ciência de dados hospitalar para levantar, organizar, documentar e avaliar dados que poderão alimentar os futuros módulos do ecossistema CardioIA.

> **Escopo acadêmico:** este repositório não oferece diagnóstico, tratamento ou recomendação médica. Os dados e traçados produzidos pelo grupo são sintéticos e servem apenas para aprendizagem e prototipação.

## Objetivo

Preparar três modalidades de dados cardiovasculares:

1. dados numéricos tabulares;
2. textos relacionados ao coração e à saúde cardiovascular;
3. imagens de traçados de ECG.

O trabalho prioriza rastreabilidade, privacidade, documentação, análise de vieses e reutilização nas próximas fases do PBL.

## Entregáveis e links públicos

| Parte | Conteúdo | Quantidade | Formato | Link público |
|---|---|---:|---|---|
| Dados numéricos | pacientes cardiovasculares sintéticos | 150 linhas | `.csv` e `.xlsx` | [CSV](https://drive.google.com/file/d/1HnlPUPEPy60gnaZxyj95yXEgWjuthC8N/view) · [XLSX](https://docs.google.com/spreadsheets/d/1AvjAxQ4cUDXAejiGdPOv3g8mYj4764ix/edit) |
| Dados textuais | textos contextuais sobre cardiologia | 2 arquivos | `.txt` | [Texto 1](https://drive.google.com/file/d/1BbNlI70gYCpd7FA4YDGQxs3lSDy-Mnms/view) · [Texto 2](https://drive.google.com/file/d/16unqNwFppNcaUbzc-Ml6ryS4eRYcXkC7/view) |
| Dados visuais | traçados de ECG sintéticos | 100 imagens | `.png` em `.zip` | [ZIP com 100 ECGs](https://drive.google.com/file/d/1m9SIyu2w9nHW3KeFlL0F1JUnqudw0m7n/view) |

Antes da entrega, os três links devem ser testados em janela anônima e permitir leitura ou download sem solicitação de login.

Pasta de apoio no Google Drive: [FIAP 2026 — CardioIA Fase 1 — Dados](https://drive.google.com/drive/folders/1RvTaKIOQbhe04TMe1KKybCqhSNXxvndg)

## Parte 1 — Dados numéricos

### Origem e natureza

O conjunto `cardioia_pacientes_sinteticos.csv` contém 150 registros totalmente simulados. Nenhuma linha representa uma pessoa real. A geração usa semente fixa (`20260809`), distribuições controladas e regras didáticas documentadas no script.

Também fornecemos uma versão `.xlsx` com três abas:

- `Dados_Sinteticos`: registros tabulares;
- `Dicionario`: definição, tipo, unidade e códigos;
- `Governanca`: finalidade, limites, privacidade, viés e rastreabilidade.

### Variáveis consideradas mais relevantes

- **Idade:** auxilia a estudar como risco e manifestações cardiovasculares variam ao longo da vida, mas não deve ser usada isoladamente.
- **Pressão arterial sistólica e diastólica:** representam medidas hemodinâmicas importantes para análises de risco e monitoramento.
- **Colesterol total:** permite estudar associações entre perfil lipídico e doença cardiovascular.
- **Glicemia e histórico de diabetes:** ajudam a representar comorbidades relevantes.
- **Frequência cardíaca em repouso e máxima:** úteis para padrões fisiológicos e resposta ao esforço.
- **Dor torácica e angina induzida por exercício:** simulam sinais e sintomas que podem apoiar tarefas futuras de classificação.
- **Tabagismo e histórico familiar:** representam fatores de risco e exigem interpretação crítica.
- **Sexo ao nascimento:** variável sensível que deve ser monitorada quanto a representação e desempenho desigual.

Essas variáveis são clinicamente plausíveis como temas de estudo, mas os valores simulados e o rótulo sintético **não podem ser usados para decisão clínica**.

### Uso futuro em IA

- análise exploratória e qualidade de dados;
- tratamento de variáveis numéricas e categóricas;
- classificação didática de risco;
- comparação de modelos;
- avaliação de desempenho por subgrupos;
- estudo de explicabilidade e viés.

## Parte 2 — Dados textuais

Foram preparados dois arquivos em `assets/textos/`, contextualizados a partir de obras de domínio público do Project Gutenberg:

1. *Disturbances of the Heart*, de Oliver T. Osborne;
2. *The Lettsomian Lectures on Diseases and Disorders of the Heart and Arteries in Middle and Advanced Life*, de J. Mitchell Bruce.

Os arquivos do repositório são textos contextuais produzidos para o projeto e registram a fonte original. As obras históricas não devem ser interpretadas como orientação médica atual.

### Possibilidades de NLP

- **extração de entidades e sintomas:** identificar termos referentes a dor, palpitações, pressão arterial, dispneia e tratamentos;
- **classificação de tópicos:** separar trechos por sintomas, fatores de risco, diagnóstico, tratamento ou anatomia;
- **frequência de termos e n-gramas:** observar vocabulário e relações recorrentes;
- **comparação temporal:** comparar linguagem médica histórica com terminologia contemporânea;
- **sumarização:** produzir resumos rastreáveis e avaliar perda de informação;
- **limpeza e normalização:** estudar tokenização, stopwords, lematização e variação terminológica.

Essas tarefas são relevantes porque grande parte da informação clínica está em linguagem natural. Porém, resultados automáticos exigem validação humana, contexto e governança.

## Parte 3 — Dados visuais

O arquivo `cardioia_100_ecgs_sinteticos.zip` reúne 100 imagens `.png` de traçados de ECG gerados matematicamente. As imagens imitam a aparência de papel milimetrado e incluem variações didáticas de frequência e morfologia.

### Possibilidades de Visão Computacional

- detecção de linhas e bordas;
- segmentação do traçado em relação ao fundo;
- normalização de escala e remoção de ruído;
- identificação de picos e intervalos visuais;
- classificação didática de padrões sintéticos;
- comparação entre imagem e série temporal.

### Limitação essencial

As imagens **não são exames reais**, não representam pacientes e não possuem validade diagnóstica. Um modelo treinado somente nesse conjunto não deve ser aplicado em ambiente clínico. Em fase futura, será necessário validar metodologia, licença, qualidade e representatividade antes de incorporar bases reais, como as disponibilizadas pela PhysioNet.

## Governança de dados e IA

- **Privacidade:** não há nomes, documentos, contatos, datas de nascimento nem identificadores reais.
- **Finalidade:** aprendizagem acadêmica e preparação de pipeline.
- **Minimização:** somente variáveis necessárias ao exercício foram incluídas.
- **Rastreabilidade:** scripts, sementes, dicionário e fontes estão versionados.
- **Viés:** dados sintéticos reproduzem decisões de modelagem e não a diversidade real da população.
- **Validação:** qualquer uso futuro exige análise de qualidade, métricas por subgrupo e revisão humana.
- **Segurança:** não versionar tokens, credenciais ou dados pessoais.
- **Responsabilidade:** resultados não devem ser apresentados como aconselhamento médico.

Veja [Governança e vieses](docs/GOVERNANCA_E_VIES.md).

## Estrutura

```text
cardioia-batimentos-de-dados/
├── README.md
├── assets/
│   ├── textos/
│   └── imagens/
├── data/
│   └── numericos/
├── docs/
├── notebooks/
└── scripts/
```

## Como reproduzir

1. Crie um ambiente virtual Python.
2. Instale as dependências registradas em `requirements.txt`.
3. Execute `python scripts/gerar_dataset_sintetico.py`.
4. Execute `python scripts/gerar_ecgs_sinteticos.py`.
5. Confira contagens, formatos, manifesto e avisos de governança.

## Fontes e referências

- UCI Machine Learning Repository — Heart Disease: https://archive.ics.uci.edu/dataset/45/heart+disease
- Project Gutenberg — *Disturbances of the Heart*: https://www.gutenberg.org/ebooks/3731
- Project Gutenberg — *The Lettsomian Lectures...*: https://www.gutenberg.org/ebooks/43780
- PhysioNet — MIT-BIH Supraventricular Arrhythmia Database: https://physionet.org/content/svdb/1.0.0/

## Autoria

- Fabrício Mouzer Brito — RM 566777
- Curso: Tecnólogo em Inteligência Artificial — FIAP

## Status da auditoria

🟡 **Em desenvolvimento.** Os dados e links foram preparados, mas a permissão “qualquer pessoa com o link” e o acesso em janela anônima ainda precisam ser confirmados antes da entrega.
