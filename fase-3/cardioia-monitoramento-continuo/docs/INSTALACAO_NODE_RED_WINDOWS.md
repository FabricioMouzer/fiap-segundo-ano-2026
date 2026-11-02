# Instalação do Node-RED no Windows

Este guia prepara o ambiente local usado pelo dashboard da Fase 3. A instalação deve ser realizada no computador que executará e registrará as evidências do projeto.

## Decisão de compatibilidade

O flow `node-red/cardioia-dashboard-flow.json` usa os nós do pacote clássico `node-red-dashboard`, o mesmo pacote apresentado no material da disciplina. Esse pacote foi descontinuado em 27 de junho de 2024 e não deve ser adotado em produção. Para esta entrega acadêmica, ele será usado apenas localmente, com dados sintéticos e sem exposição pública do painel.

O sucessor recomendado atualmente é o `@flowfuse/node-red-dashboard`. A migração foi registrada como melhoria posterior porque os tipos e a configuração dos nós diferem e uma troca agora exigiria recriação e nova validação do flow.

## 1. Instalar o Node.js

1. Baixe a versão LTS no site oficial: <https://nodejs.org/>.
2. Execute o instalador MSI e mantenha as opções padrão.
3. Feche e abra novamente o PowerShell.
4. Verifique:

```powershell
node --version
npm --version
```

Os dois comandos precisam retornar números de versão.

## 2. Instalar o Node-RED

No PowerShell, sem executar como administrador:

```powershell
npm install -g node-red
node-red
```

Mantenha a janela aberta. Quando o log informar que o servidor foi iniciado, abra:

<http://localhost:1880/>

## 3. Instalar o dashboard compatível

Na interface do Node-RED:

1. Abra o menu no canto superior direito.
2. Selecione **Manage palette** / **Gerenciar paleta**.
3. Abra a aba **Install** / **Instalar**.
4. Procure por `node-red-dashboard`.
5. Instale o pacote com esse nome exato.
6. Reinicie o Node-RED se a interface solicitar.

Alternativa pelo PowerShell, depois de interromper o Node-RED com `Ctrl+C`:

```powershell
cd $env:USERPROFILE\.node-red
npm install node-red-dashboard
node-red
```

## 4. Importar o flow do CardioIA

1. Abra <http://localhost:1880/>.
2. Menu → **Import** → **Clipboard**.
3. Copie todo o conteúdo de `node-red/cardioia-dashboard-flow.json`.
4. Importe e clique em **Deploy**.
5. Abra <http://localhost:1880/ui>.

## 5. Evidências obrigatórias

Preserve capturas legíveis de:

- editor do Node-RED com o flow completo;
- dashboard com gráfico de BPM;
- gauge de temperatura;
- alerta normal;
- alerta de BPM alto;
- alerta de BPM baixo;
- alerta de temperatura alta;
- recebimento dos dados MQTT;
- sincronização depois do período offline.

## Diagnóstico rápido

| Sintoma | Verificação |
|---|---|
| `node` não é reconhecido | Reabra o PowerShell; se persistir, reinstale o Node.js LTS. |
| `node-red` não é reconhecido | Reabra o PowerShell e repita `npm install -g node-red`. |
| Nós `ui_*` aparecem como desconhecidos | Instale `node-red-dashboard` e reinicie o Node-RED. |
| Dashboard não abre em `/ui` | Confirme o Deploy e procure erros na aba Debug. |
| MQTT não conecta | Verifique internet, broker, porta e tópico configurados. |

## Fontes oficiais consultadas

- Node-RED — instalação no Windows: <https://nodered.org/docs/getting-started/windows>
- Node-RED Flow Library — estado do pacote clássico: <https://flows.nodered.org/node/node-red-dashboard>
- FlowFuse Dashboard 2.0 — sucessor recomendado: <https://dashboard.flowfuse.com/getting-started.html>
