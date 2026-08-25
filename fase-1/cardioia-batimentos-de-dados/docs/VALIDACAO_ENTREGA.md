# Validação final — CardioIA Fase 1

**Data da auditoria:** 25/08/2026  
**Prazo exibido na plataforma FIAP:** 02/09/2026  
**Escopo:** requisitos do enunciado, integridade dos arquivos e consistência entre entregáveis.

## Resultado resumido

| Requisito | Evidência verificada | Resultado |
|---|---|---|
| Dataset numérico | CSV com 150 linhas e 17 colunas | Aprovado |
| Qualidade do dataset | 0 nulos, 0 duplicidades exatas e 0 IDs repetidos | Aprovado |
| Formato alternativo | XLSX com abas `Dados_Sinteticos`, `Dicionario` e `Governanca` | Aprovado |
| Consistência CSV/XLSX | Conteúdo da aba de dados idêntico ao CSV | Aprovado |
| Dados textuais | 2 arquivos `.txt`, legíveis, contextualizados e com fontes | Aprovado com observação |
| Dados visuais | ZIP íntegro com 100 arquivos PNG | Aprovado |
| Manifesto visual | 100 entradas únicas e nenhuma imagem ausente | Aprovado |
| README | Objetivo, fontes, justificativas, governança, equipe e links | Aprovado |
| Estrutura | Pastas `assets`, `data`, `docs`, `notebooks` e `scripts` | Aprovado |
| Acesso público | Cinco arquivos abertos em janela anônima, sem login | Aprovado |

## Perfil do dataset

- Unidade de análise: paciente cardiovascular sintético.
- Chave: `patient_id_synthetic`, única e no padrão `SYN-0001`.
- Faixa etária: 29 a 82 anos.
- Pressão sistólica: 95 a 170 mmHg.
- Pressão diastólica: 55 a 99 mmHg.
- Colesterol total: 130 a 313 mg/dL.
- Glicemia de jejum: 66 a 201 mg/dL.
- Frequência cardíaca em repouso: 48 a 107 bpm.
- Frequência cardíaca máxima: 126 a 195 bpm.
- IMC: 18,0 a 40,5 kg/m².
- Rótulos explicitamente sintéticos e sem finalidade diagnóstica.

## Observação sobre os textos

Os dois arquivos atuais são textos contextuais derivados de obras em domínio público do Project Gutenberg. Eles atendem à quantidade, ao formato, à temática, às fontes e à explicação de uso em NLP. Como o enunciado usa a expressão “faça o download de textos”, recomenda-se confirmar com o professor se são aceitos textos contextuais ou se devem ser incluídas as obras integrais em `.txt`.

## Verificação de acesso

Em 25/08/2026, o grupo confirmou a abertura dos cinco arquivos em janela anônima, sem login: CSV, XLSX, Texto 1, Texto 2 e ZIP com 100 ECGs. O requisito de acesso público está concluído.

## Equipe

| Integrante | RM |
|---|---|
| Fabrício Mouzer Brito | RM566777 |
| Enzo Nunes Castanheira Gloria da Silva | RM567599 |
| Larissa Nunes Moreira Reis | RM568280 |
| Gabriel Rapozo Guimarães Soares | RM568480 |
