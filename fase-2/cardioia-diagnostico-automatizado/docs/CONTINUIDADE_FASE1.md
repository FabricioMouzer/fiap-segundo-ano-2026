# Continuidade verificável entre a Fase 1 e a Fase 2

Esta auditoria executa leitura e análise de ativos da Fase 1. Antes desta ponte,
o pipeline da Fase 2 utilizava dados criados na própria Fase 2; a continuidade
era temática, organizacional e de governança. O classificador principal continua
usando seu conjunto independente de 80 frases sintéticas.

## O que foi efetivamente aproveitado

| Ativo da Fase 1 | Uso executado nesta Fase 2 | Limite |
|---|---|---|
| CSV de pacientes sintéticos | leitura dos 150 registros e 17 colunas; representação por sexo, idade e rótulo original | não treina o classificador das 80 frases |
| Dois TXT de contexto histórico | normalização, tokenização e frequência de termos na seção CONTEXTO | resumos autorais em português; não são relatos de pacientes ou obras integrais |
| Script gerador do CSV | identificação por hash e análise documentada das regras de simulação | nenhum dado é regenerado ou rótulo alterado |
| Governança e dicionário | continuidade da finalidade acadêmica, categorias documentadas e rastreabilidade | governança não demonstra validade clínica |
| Dois PDFs em assets/textos | permanecem disponíveis como referências do projeto | não são lidos por esta auditoria nem usados no treinamento |
| XLSX e 100 imagens sintéticas de ECG | preservados como entregáveis da Fase 1 e material para extensões | não entram no pipeline obrigatório textual da Fase 2 |

Os 10 relatos de sintomas, as 45 expressões do mapa e as 80 frases rotuladas
foram elaborados para a Fase 2. Não existe vínculo entre essas frases e os
identificadores `SYN-XXXX` do CSV da Fase 1. Os modelos de Regressão Logística e
Árvore de Decisão são treinados exclusivamente com `data/raw/dataset_risco.csv`.

## Representação e viés de simulação

A base da Fase 1 contém **143 rótulos `lower_simulated_risk` e
7 rótulos `higher_simulated_risk`**. São 150
identificadores sintéticos distintos, 0 células vazias e
idades entre 29 e 82 anos.

| Dimensão | Grupo | Registros | Higher | Lower | Proporção Higher |
|---|---|---:|---:|---:|---:|
| sex_at_birth | F | 70 | 1 | 69 | 1.4% |
| sex_at_birth | M | 80 | 6 | 74 | 7.5% |
| faixa_etaria | 45 a 59 | 65 | 1 | 64 | 1.5% |
| faixa_etaria | 60 ou mais | 60 | 6 | 54 | 10.0% |
| faixa_etaria | menos de 45 | 25 | 0 | 25 | 0.0% |

As faixas etárias são agrupamentos descritivos deste projeto, sem significado
clínico atribuído. As proporções descrevem **rótulos do gerador**, não prevalência
de doença. Não são métricas de desempenho ou de equidade de um modelo.

O script original adiciona `0.45` ao escore de simulação quando `sex_at_birth == "M"`;
idade e outras variáveis também integram a fórmula. A diferença observada entre
grupos foi, portanto, influenciada pelas decisões do gerador. Não é evidência
populacional. A baixa contagem de rótulos Higher, especialmente no grupo F,
impede conclusões robustas por subgrupo.

Prever sempre a classe majoritária acertaria **95.3%**
destas linhas, mas encontraria zero exemplos da classe minoritária. Esse cálculo
descritivo ilustra por que acurácia isolada pode enganar; não é um modelo treinado
nem um resultado de teste. Ele não deve ser comparado aos 80% do experimento textual,
que tem outra tarefa, outros rótulos e outra divisão de dados.

## NLP exploratório sobre os textos da Fase 1

Método: extrair somente a seção `CONTEXTO`; transformar em minúsculas; remover
acentos; separar tokens alfabéticos; excluir tokens com menos de três letras e
uma lista explícita de palavras funcionais, versionada no script e no JSON.
Cabeçalhos, URLs, perguntas propostas e a seção de limitações não entram na contagem.
Não há lematização, extração clínica, rotulagem ou treinamento neste passo.

| Texto | Tokens após filtro | Termos distintos | Cinco termos mais frequentes |
|---|---:|---:|---|
| texto_01_disturbances_of_the_heart_contexto.txt | 58 | 52 | arterial (2), coracao (2), historico (2), linguagem (2), pressao (2) |
| texto_02_lettsomian_lectures_contexto.txt | 54 | 46 | idade (4), arterias (2), coracao (2), doencas (2), sintomas (2) |

Os termos comuns e as frequências completas estão nos arquivos de evidência.
Os dois textos contextualizam obras históricas; as obras originais não foram
baixadas nem processadas nesta etapa. A amostra é pequena e não representa um
corpus clínico contemporâneo.

## Decisão metodológica

A continuidade tem evidências executáveis de exploração de dados, NLP e análise
do viés de geração a partir dos ativos da Fase 1. Na Parte 2, o enunciado detalhado
pede montar uma pequena base simulada em CSV com frases rotuladas; essa tarefa é
atendida pelo conjunto independente de 80 frases da Fase 2.

O CSV de 150 registros não treinou o modelo textual. Seus rótulos originais
descrevem um escore didático calculado pelo gerador a partir de atributos tabulares;
os rótulos das 80 frases foram definidos para o exercício de classificação de
relatos. Equiparar esses rótulos ou unir as bases confundiria tarefas distintas.
A decisão foi reutilizar os ativos originais para NLP exploratório e análise de
vieses e construir o corpus próprio de classificação solicitado, mantendo
rastreabilidade, avaliações e resultados separados.

## Reproduzir e localizar as evidências

Na pasta da Fase 2:

```bash
python src/auditar_continuidade_fase1.py
python -m unittest discover -s tests -p 'test_continuidade_fase1.py' -v
```

- `data/processed/continuidade_fase1.json`: auditoria, fontes, hashes e termos;
- `data/processed/representacao_fase1.csv`: contagens por sexo e faixa etária;
- `data/processed/termos_fase1.csv`: frequência completa por texto;
- `docs/CONTINUIDADE_FASE1.md`: este relatório, gerado pelo script.

Nenhum arquivo da Fase 1 nem as 80 frases da Fase 2 é modificado pelo script.
As evidências são determinísticas e não são adicionadas às métricas dos modelos.

## Identificação das fontes

Os caminhos abaixo são relativos à raiz do repositório. O SHA256 identifica os
bytes lidos, incluindo o script de simulação e o conjunto independente da Fase 2.

| Fonte | SHA256 |
|---|---|
| `fase-1/cardioia-batimentos-de-dados/data/numericos/cardioia_pacientes_sinteticos.csv` | `5c59928fde79d5c3f4b2bb94d5af0bf7a0ab61d61068cb787788665ba3debfc9` |
| `fase-1/cardioia-batimentos-de-dados/scripts/gerar_dataset_sintetico.py` | `d298d1117501020a7328251fb5a0cdb68f9e7c305a502dceb3cd14eb2bc1fac5` |
| `fase-1/cardioia-batimentos-de-dados/assets/textos/texto_01_disturbances_of_the_heart_contexto.txt` | `47605b368374ab7af71424304325cfbf3efc25121bd53c678bdbd80ee8e5618b` |
| `fase-1/cardioia-batimentos-de-dados/assets/textos/texto_02_lettsomian_lectures_contexto.txt` | `a5ddf28b4cfe4a1fc09516f47a0b144163b2b9a1239cfb3abc0d055c8ac3b333` |
| `fase-2/cardioia-diagnostico-automatizado/data/raw/dataset_risco.csv` | `c1f1c213c302e73fe01fd7af00794ea5267e191d4928f9571862c5e2f0b28721` |

> Projeto educacional com dados sintéticos. Nenhuma análise constitui diagnóstico,
> recomendação clínica ou comprovação de equidade em uma população real.
