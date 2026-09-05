# Governança, vieses e limitações

## Origem e separação

Os 150 perfis da Fase 1 e as 80 frases da Fase 2 são bases sintéticas distintas. A primeira usa rótulos didáticos de perfil; a segunda simula classes textuais de triagem. A análise de continuidade preserva essa diferença e registra as fontes por SHA-256. Não há prontuários reais.

Os dois TXT da Fase 1 são textos contextuais do projeto com referências históricas. Exploramos seu vocabulário sem transformá-los em orientação médica atual, relatos de pacientes ou treino supervisionado das 80 frases.

## Evidências observadas

- A base da Fase 1 contém 143 rótulos `lower_simulated_risk` e apenas 7 `higher_simulated_risk`. Um preditor majoritário acertaria 95,3% sem reconhecer nenhum exemplo minoritário. Isso mostra como acurácia isolada pode enganar; não é desempenho do classificador textual.
- O corpus Fase 2 é balanceado (40/40), mas segue padrões controlados. Balanceamento de classes não demonstra diversidade populacional.
- A divisão por `grupo_id` mantém variações da mesma frase base juntas. Reduz vazamento, sem garantir independência semântica entre grupos.
- Os dois falsos negativos e dois falsos positivos da Regressão Logística permanecem publicados, sem remover exemplos difíceis para elevar métricas.
- A comparação de modelos usa a mesma divisão fixa. A escolha não foi confirmada por teste externo independente.

## Limites de interpretação

Não é possível estimar justiça clínica por sexo, idade ou outros grupos com esta base. As distribuições da Fase 1 refletem a simulação, não prevalência real. O classificador textual não recebe sexo/idade como campos estruturados e não foi avaliado sobre população representativa.

O extrator reconhece expressões explícitas e algumas negações. Não compreende integralmente temporalidade, ironia, escopo de negação, intensidade ou linguagem indireta. TF-IDF também pode errar diante de palavras desconhecidas e contextos diferentes. Probabilidades do modelo não são probabilidades calibradas de doença.

## Publicação e responsabilidade

- publicar artefatos sintéticos e nomes/RMs já autorizados da equipe;
- não incluir e-mails, credenciais, prontuários, caminhos privados ou tokens;
- registrar fontes, método, versões e resultados reais;
- apresentar o vídeo e os slides como explicação acadêmica;
- não declarar opcionais concluídos sem seus entregáveis;
- preservar revisão humana e comprovante de envio à FIAP.

> Projeto educacional. As saídas não constituem diagnóstico, prescrição nem orientação para emergências.
