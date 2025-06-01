
# 🔒 Sistema de Segurança Automático para Discord

Um bot de segurança avançado que protege automaticamente seu servidor Discord contra ações maliciosas!

## 🚀 Características Principais

### 🔥 Detecção de Exclusão de Canais
- Monitora automaticamente quando canais são deletados
- Identifica o responsável através do audit log
- Remove todos os cargos do usuário como punição
- Salva informações para possível restauração

### 🎭 Detecção de Exclusão de Cargos
- Detecta exclusões de cargos em tempo real
- Punição configurável: remover cargos ou banir usuário
- Sistema de logs detalhado
- Proteção contra ataques de spam de exclusões

### 🤖 Proteção Contra Bots
- Bane automaticamente bots que tentam entrar
- Configurável (pode ser desativado)
- Log de todas as ações de segurança

### 🔐 Sistema de Whitelist
- Usuários autorizados não sofrem punições
- Fácil gerenciamento via comandos
- Ideal para admins e moderadores confiáveis

### 🔄 Sistema de Restauração
- Restaura cargos removidos pelo sistema
- Histórico completo de ações
- Reverter punições quando necessário

## 📦 Instalação

### 1. **Configure o Token do Bot**

No Replit, vá em **Secrets** e adicione:
```
SECURITY_BOT_TOKEN = seu_token_aqui
```

### 2. **Personalize as Configurações**

Edite o arquivo `security_config.py`:

```python
# Adicione IDs de usuários autorizados
WHITELIST_IDS = [
    123456789012345678,  # Seu ID
    987654321098765432,  # ID de admin confiável
]

# Configure punições
DEFAULT_CONFIG = {
    'auto_ban_bots': True,  # Banir bots automaticamente
    'role_delete_punishment': 'remove_roles',  # ou 'ban'
    'logs_channel_name': 'security-logs',  # Nome do canal de logs
}
```

### 3. **Execute o Bot**

```bash
python security_bot.py
```

## 🛡️ Permissões Necessárias

O bot precisa dessas permissões:

- ✅ **View Audit Log** - Para identificar responsáveis
- ✅ **Manage Roles** - Para remover cargos
- ✅ **Ban Members** - Para banir usuários
- ✅ **Manage Channels** - Para criar canal de logs
- ✅ **Send Messages** - Para enviar logs
- ✅ **Embed Links** - Para embeds formatados

## 📋 Comandos Disponíveis

### 👑 Comandos Administrativos

```bash
!sec_status          # Mostra status do sistema
!sec_config          # Visualiza/altera configurações
!sec_restore <ID>    # Restaura cargos de um usuário
!sec_whitelist       # Gerencia usuários autorizados
!sec_help           # Central de ajuda
```

### ⚙️ Exemplos de Configuração

```bash
# Ativar/desativar banimento automático de bots
!sec_config auto_ban_bots true
!sec_config auto_ban_bots false

# Alterar punição por deletar cargos
!sec_config role_delete_punishment ban
!sec_config role_delete_punishment remove_roles

# Alterar nome do canal de logs
!sec_config logs_channel_name security-alerts
```

### 🔐 Gerenciar Whitelist

```bash
# Ver usuários autorizados
!sec_whitelist

# Adicionar usuário à whitelist
!sec_whitelist add 123456789012345678

# Remover usuário da whitelist
!sec_whitelist remove 123456789012345678
```

## 🎯 Como Funciona

### 1. **Detecção Automática**
O bot monitora constantemente:
- Exclusões de canais (`on_guild_channel_delete`)
- Exclusões de cargos (`on_guild_role_delete`) 
- Entrada de bots (`on_member_join`)

### 2. **Verificação de Audit Log**
- Aguarda 2 segundos para o audit log atualizar
- Identifica exatamente quem executou a ação
- Verifica se o usuário está na whitelist

### 3. **Aplicação de Punições**
- **Usuários autorizados**: Apenas log, sem punição
- **Usuários suspeitos**: Punição conforme configuração
- **Logs detalhados**: Todas as ações são registradas

### 4. **Sistema de Restauração**
- Salva todos os cargos antes de remover
- Permite reverter punições via comando
- Histórico completo para auditoria

## 📊 Logs e Monitoramento

O sistema cria automaticamente embeds detalhados com:

- 👤 **Responsável pela ação**
- 🎯 **O que foi deletado**
- ⚡ **Punição aplicada**
- 🔄 **Opções de restauração**
- 📅 **Timestamp completo**

## 🔧 Configurações Avançadas

### Personalizar Mensagens

Edite o arquivo `security_config.py`:

```python
MESSAGES = {
    'channel_deleted': "🚨 CANAL DELETADO - AÇÃO SUSPEITA",
    'role_deleted': "🚨 CARGO DELETADO - AÇÃO SUSPEITA",
    'bot_banned': "🤖 Bot Invasor Eliminado",
}
```

### Personalizar Cores

```python
COLORS = {
    'danger': 0xff0000,   # Vermelho para perigos
    'warning': 0xff9900,  # Laranja para avisos  
    'success': 0x00ff00,  # Verde para sucessos
    'info': 0x0099ff,     # Azul para informações
}
```

## 🚨 Cenários de Uso

### ✅ **Cenário 1: Admin Autorizado**
1. Admin na whitelist deleta um canal
2. Sistema detecta e registra no log
3. **Nenhuma punição aplicada**
4. Log marca como "Usuário Autorizado"

### ❌ **Cenário 2: Usuário Suspeito**
1. Usuário normal deleta canal importante
2. Sistema detecta via audit log
3. **Remove todos os cargos imediatamente**
4. Salva cargos para possível restauração
5. Envia log detalhado no canal

### 🤖 **Cenário 3: Bot Invasor**
1. Bot suspeito tenta entrar no servidor
2. Sistema detecta automaticamente
3. **Bane o bot imediatamente**
4. Registra ação no log de segurança

## 🔄 Restauração de Cargos

Se uma punição foi aplicada incorretamente:

```bash
# Listar usuários que podem ser restaurados
!sec_status

# Restaurar cargos de um usuário específico
!sec_restore 123456789012345678
```

O sistema irá:
- ✅ Verificar se há cargos para restaurar
- ✅ Adicionar de volta os cargos originais
- ✅ Remover da lista de restauração
- ✅ Registrar a restauração no log

## 📈 Monitoramento e Estatísticas

Use `!sec_status` para ver:

- 🟢 **Status do sistema** (Online/Offline)
- 📊 **Número de logs salvos**
- 🔄 **Restaurações pendentes**
- ⚙️ **Configurações ativas**
- 🛡️ **Proteções habilitadas**

## ⚠️ Troubleshooting

### Bot não está detectando exclusões?
1. ✅ Verifique se tem permissão "View Audit Log"
2. ✅ Confirme que o bot está online
3. ✅ Teste com `!sec_status`

### Não consegue remover cargos?
1. ✅ Verifique permissão "Manage Roles"
2. ✅ Cargo do bot deve estar acima dos outros
3. ✅ Não pode remover cargos superiores

### Canal de logs não criado?
1. ✅ Permissão "Manage Channels" necessária
2. ✅ Use `!sec_config logs_channel_name nome`
3. ✅ Crie manualmente se necessário

## 🔐 Segurança e Boas Práticas

### ✅ **Recomendações**
- Mantenha a whitelist atualizada
- Monitore logs regularmente  
- Teste configurações em servidor de teste
- Faça backup das configurações

### ⚠️ **Cuidados**
- Não adicione usuários não confiáveis na whitelist
- Configure punições adequadas ao seu servidor
- Mantenha o bot atualizado
- Monitore uso de recursos

## 💡 Dicas Extras

1. **Canal de logs dedicado**: Crie um canal específico para logs de segurança
2. **Whitelist mínima**: Apenas admins essenciais na whitelist
3. **Testes regulares**: Teste o sistema periodicamente
4. **Backup de configuração**: Salve suas configurações personalizadas
5. **Monitoramento ativo**: Verifique logs regularmente

---

**🔒 Sistema desenvolvido para máxima segurança do seu servidor Discord!**

Para suporte ou dúvidas, consulte os logs do sistema ou use `!sec_help`.
