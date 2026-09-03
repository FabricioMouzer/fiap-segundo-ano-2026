# Dicionário de dados

Todos os registros desta fase são sintéticos e destinados exclusivamente ao aprendizado.

## relatos_sintomas.txt

Cada linha representa um relato independente. Os 10 relatos contêm sintoma, referência temporal e impacto na rotina.

## mapa_conhecimento.csv

| Coluna | Definição |
|---|---|
| `expressao` | termo ou expressão procurada no relato |
| `sintoma_normalizado` | conceito simplificado usado para organizar os achados |
| `possivel_associacao` | associação educacional, não diagnóstica |
| `nivel_alerta` | indicação interna: `baixo`, `avaliar` ou `alto` |

## dataset_risco.csv

| Coluna | Definição |
|---|---|
| `frase` | relato sintético usado pelo classificador |
| `situacao` | rótulo acadêmico: `baixo risco` ou `alto risco` |
| `grupo_id` | identifica frases derivadas da mesma base e impede vazamento entre treino e teste |

O `grupo_id` é usado apenas para a separação metodológica dos dados e não como variável preditora.
