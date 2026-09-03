# Demonstração visual interativa

## Acesso

[Abrir o portal CardioIA](https://cardioia-demo-fiap.fabriciomouzer2025.chatgpt.site)

## Finalidade

A interface demonstra, com relatos sintéticos, os dois componentes centrais da Fase 2:

1. extração explicável de sintomas por mapa de conhecimento;
2. classificação textual de risco por TF-IDF e Regressão Logística.

## Coerência com o notebook

O portal utiliza os parâmetros exportados do classificador validado: vocabulário, valores IDF, coeficientes e intercepto. A inferência no navegador aplica a mesma tokenização por unigramas e bigramas e a mesma normalização L2 do pipeline acadêmico.

O painel informa a confiança estimada para a classe prevista, mas essa probabilidade não deve ser interpretada como risco clínico real.

## Fluxo demonstrado

```mermaid
flowchart LR
    A[Relato sintético] --> B[Normalização]
    B --> C[Mapa de conhecimento]
    B --> D[TF-IDF]
    C --> E[Sintomas e associações]
    D --> F[Regressão Logística]
    F --> G[Classe e confiança]
```

## Verificações realizadas

- compilação de produção concluída;
- cenário musculoesquelético classificado como baixo risco;
- cenário com alteração da fala e perda de força classificado como alto risco;
- visualização dos achados do mapa de conhecimento;
- layout adaptável para computador e celular;
- aviso de uso exclusivamente acadêmico visível na interface.

## Limitações

A demonstração utiliza dados sintéticos e um modelo pequeno. Não realiza diagnóstico, não orienta conduta médica e não substitui avaliação profissional.
