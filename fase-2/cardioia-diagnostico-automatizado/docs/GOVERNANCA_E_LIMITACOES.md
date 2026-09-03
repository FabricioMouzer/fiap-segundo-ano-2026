# Governança, ética e limitações

## Natureza dos dados

- Utilizar exclusivamente relatos sintéticos ou dados públicos devidamente licenciados.
- Não incluir nomes, CPF, e-mail, telefone, prontuário ou qualquer identificador real.
- Documentar origem, método de geração, versão e limitações de cada base.

## Limitações esperadas

- associação por palavras-chave não compreende contexto clínico completo;
- TF-IDF não interpreta linguagem como um profissional de saúde;
- base pequena pode gerar métricas instáveis;
- frases parecidas podem provocar vazamento ou desempenho artificialmente alto;
- negações, ironia, erros de digitação e sintomas simultâneos podem causar falhas;
- classes e formas de escrita desbalanceadas podem favorecer determinados padrões.

## Testes responsáveis

- avaliar falsos negativos de alto risco separadamente;
- incluir variações linguísticas sem reforçar estereótipos;
- testar frases com negação e múltiplos sintomas;
- apresentar métricas além da acurácia;
- não publicar alegações de validade clínica.

## Aviso de uso

Este projeto é uma simulação educacional de apoio à decisão. Suas saídas são hipóteses produzidas por regras e modelos simples e não constituem diagnóstico, prescrição ou orientação de emergência.

