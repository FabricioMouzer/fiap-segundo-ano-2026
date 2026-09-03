# Análise dos erros — Regressão Logística

## Resultado executivo

A avaliação encontrou **4 erros em 20 amostras de teste**: **2 falsos negativos** e **2 falsos positivos**, concentrados em **2 grupos linguísticos**. Os falsos negativos são o risco metodológico mais importante, pois textos rotulados como alto risco foram classificados como baixo risco.

## Casos divergentes

| Tipo | Classe real | Previsão | Prob. alto risco | Grupo | Frase |
|---|---|---|---:|---|---|
| falso positivo | baixo risco | alto risco | 57.1% | baixo_12 | Há dois dias, tive uma pontada curta no peito ao respirar fundo, mas ela já passou. Estou observando a evolução do sintoma. |
| falso positivo | baixo risco | alto risco | 54.9% | baixo_12 | Tive uma pontada curta no peito ao respirar fundo, mas ela já passou. |
| falso negativo | alto risco | baixo risco | 38.2% | alto_11 | Senti perda de consciência após uma sequência de palpitações. |
| falso negativo | alto risco | baixo risco | 39.6% | alto_11 | Nesta manhã, senti perda de consciência após uma sequência de palpitações. O episódio me deixou preocupado. |

## Interpretação

- O conjunto é pequeno e sintético; quatro erros não permitem conclusões clínicas.
- A probabilidade próxima ao limiar de decisão indica incerteza lexical do modelo, não confiança médica.
- TF-IDF aprende padrões de palavras, mas tem compreensão limitada de negação, contexto, intensidade e temporalidade.
- As duas variações de cada grupo receberam a mesma classificação incorreta; portanto, o problema está associado ao padrão linguístico, não a uma frase isolada.
- Os casos devem permanecer registrados como evidência transparente, sem remoção seletiva para elevar a métrica.

## Próxima melhoria recomendada

Ampliar a diversidade linguística mantendo o agrupamento por `grupo_id`, repetir a validação e comparar as novas métricas com esta linha de base. Qualquer melhoria deve ser medida em um conjunto de teste separado.

> Resultado educacional; não constitui diagnóstico ou recomendação médica.
