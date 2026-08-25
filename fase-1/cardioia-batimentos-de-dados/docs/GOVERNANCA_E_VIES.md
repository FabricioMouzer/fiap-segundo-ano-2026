# Governança de dados, ética e vieses

## Classificação dos ativos

| Ativo | Natureza | Dados pessoais | Risco principal |
|---|---|---:|---|
| dataset tabular | sintético | não | simplificação e viés de simulação |
| textos | contextuais, com fontes em domínio público | não | linguagem histórica desatualizada |
| ECGs | imagens sintéticas | não | aparência realista gerar interpretação indevida |

## Decisões de governança

1. Não coletar identificadores ou prontuários reais.
2. Usar identificadores artificiais `SYN-XXXX`.
3. Documentar semente, unidades, categorias e regras de geração.
4. Proibir uso para diagnóstico, tratamento ou triagem clínica real.
5. Separar dados brutos, documentação e scripts.
6. Manter fontes e licenças registradas.
7. Testar desempenho futuro por idade, sexo e outros subgrupos relevantes.
8. Revisar termos históricos antes de utilizá-los como verdade médica atual.

## Vieses e limitações

- As distribuições não representam prevalência real.
- Relações entre fatores e rótulos foram definidas para fins didáticos.
- Categorias binárias podem reduzir diversidade e não capturam todas as realidades clínicas e sociais.
- As imagens possuem poucos tipos de variação e podem facilitar aprendizado artificial de padrões do gerador.
- Os textos históricos refletem linguagem, conhecimentos e valores de outras épocas.
- Ausência de indivíduos reais elimina risco de reidentificação, mas não elimina risco de conclusões incorretas.

## Controles futuros

- comparar com bases públicas documentadas;
- avaliar valores ausentes, duplicatas, distribuição e outliers;
- usar divisão treino/validação/teste sem vazamento;
- medir desempenho por subgrupo;
- registrar versões, transformações e responsáveis;
- submeter decisões clínicas e de produto à revisão especializada;
- monitorar drift e uso fora da finalidade.
