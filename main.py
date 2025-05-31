
import discord
from discord.ext import commands
import json
import random
import asyncio
import aiofiles
import os

# Configuração do bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)

# Sistema de ganho automático
import time
from datetime import datetime, timedelta

# Dados dos jogadores disponíveis no olheiro
JOGADORES_OLHEIRO = [
    {"nome": "Oliver Santos", "posicao": "Goleiro", "over": 80, "habilidade": 82, "valor_mercado": 50000},
    {"nome": "Zargão", "posicao": "Zagueiro", "over": 80, "habilidade": 82, "valor_mercado": 45000},
    {"nome": "Bruno", "posicao": "Zagueiro", "over": 84, "habilidade": 86, "valor_mercado": 60000},
    {"nome": "Anthony", "posicao": "Meia", "over": 85, "habilidade": 87, "valor_mercado": 65000},
    {"nome": "Lewis Ferguson", "posicao": "Atacante", "over": 79, "habilidade": 78, "valor_mercado": 40000},
    {"nome": "Saulo Bezerra", "posicao": "Atacante", "over": 88, "habilidade": 89, "valor_mercado": 80000},
    {"nome": "Pedro Caldas", "posicao": "Atacante", "over": 85, "habilidade": 87, "valor_mercado": 65000},
    {"nome": "Brunno Santos", "posicao": "Meio Campo", "over": 80, "habilidade": 82, "valor_mercado": 45000},
    {"nome": "Zau", "posicao": "Goleiro", "over": 88, "habilidade": 89, "valor_mercado": 75000},
    {"nome": "Hiroshi", "posicao": "Goleiro", "over": 84, "habilidade": 86, "valor_mercado": 55000},
    {"nome": "Sassa", "posicao": "Goleiro", "over": 76, "habilidade": 75, "valor_mercado": 35000},
    {"nome": "Oliver Wayne", "posicao": "Zagueiro", "over": 91, "habilidade": 93, "valor_mercado": 100000},
    {"nome": "Corvino", "posicao": "Ponta", "over": 86, "habilidade": 88, "valor_mercado": 70000},
    {"nome": "Pdrz", "posicao": "Atacante", "over": 86, "habilidade": 88, "valor_mercado": 70000},
    {"nome": "Nott", "posicao": "Meio", "over": 83, "habilidade": 85, "valor_mercado": 55000},
    {"nome": "Keven", "posicao": "Atacante", "over": 86, "habilidade": 88, "valor_mercado": 70000},
    {"nome": "Ronaldinho Cruzeiro", "posicao": "Ponta", "over": 84, "habilidade": 86, "valor_mercado": 60000},
    {"nome": "Carlos Cruzeiro", "posicao": "Meio", "over": 85, "habilidade": 87, "valor_mercado": 65000},
    {"nome": "Gustavo Soares", "posicao": "Meia-Central", "over": 82, "habilidade": 83, "valor_mercado": 50000},
    {"nome": "Crazy", "posicao": "Ponta", "over": 88, "habilidade": 89, "valor_mercado": 80000},
    {"nome": "Pietro", "posicao": "Volante", "over": 80, "habilidade": 82, "valor_mercado": 45000},
    {"nome": "Matheus Taylor", "posicao": "Ponta Esq.", "over": 96, "habilidade": 98, "valor_mercado": 150000},
    {"nome": "Juliano Henrique", "posicao": "Atacante", "over": 99, "habilidade": 100, "valor_mercado": 200000},
    {"nome": "Michael Owen", "posicao": "Goleiro", "over": 99, "habilidade": 100, "valor_mercado": 200000},
    {"nome": "Phillipe Guedes", "posicao": "Atacante", "over": 88, "habilidade": 89, "valor_mercado": 80000},
    {"nome": "Prince", "posicao": "Ponta Direita", "over": 91, "habilidade": 93, "valor_mercado": 100000},
    {"nome": "Hiroshi", "posicao": "Zagueiro", "over": 90, "habilidade": 92, "valor_mercado": 95000},
    {"nome": "Felipe Botelho", "posicao": "Meio Campo", "over": 87, "habilidade": 88, "valor_mercado": 75000},
    {"nome": "M. De Light", "posicao": "Zagueiro", "over": 90, "habilidade": 92, "valor_mercado": 95000},
    {"nome": "Kai Guedes", "posicao": "Ponta Dir.", "over": 90, "habilidade": 92, "valor_mercado": 95000},
    {"nome": "Macaé", "posicao": "Atacante", "over": 89, "habilidade": 90, "valor_mercado": 85000},
    {"nome": "Lucas Bask", "posicao": "Zagueiro", "over": 79, "habilidade": 78, "valor_mercado": 40000},
    {"nome": "Sam Ker", "posicao": "Atacante", "over": 75, "habilidade": 74, "valor_mercado": 30000},
    {"nome": "Jake Willy", "posicao": "Atacante", "over": 69, "habilidade": 68, "valor_mercado": 25000},
    {"nome": "Zake Zau", "posicao": "Volante", "over": 80, "habilidade": 82, "valor_mercado": 45000},
    {"nome": "Helena Silva", "posicao": "Zagueira", "over": 70, "habilidade": 70, "valor_mercado": 28000},
    {"nome": "Luan Alves", "posicao": "Goleiro", "over": 69, "habilidade": 68, "valor_mercado": 25000},
    {"nome": "Fernando M.", "posicao": "Atacante", "over": 71, "habilidade": 71, "valor_mercado": 30000},
    {"nome": "Coutinho S.", "posicao": "Meio Campo", "over": 69, "habilidade": 68, "valor_mercado": 25000},
    {"nome": "Kaio Becker", "posicao": "Zagueiro", "over": 67, "habilidade": 66, "valor_mercado": 22000},
    {"nome": "Caio Miguel", "posicao": "Goleiro", "over": 69, "habilidade": 68, "valor_mercado": 25000},
    {"nome": "Alex", "posicao": "Volante", "over": 75, "habilidade": 74, "valor_mercado": 32000},
    {"nome": "Matheus Mtzx", "posicao": "Ponta Dir.", "over": 70, "habilidade": 70, "valor_mercado": 28000}
]

# Arquivo para salvar dados
DATA_FILE = "vados_bot_data.json"

# ID do owner (coloque seu ID aqui)
OWNER_ID = 983196900910039090  # Substitua pelo seu ID

class VadosBot:
    def __init__(self):
        self.users_data = {}
        self.ligas = {}
        self.confrontos = {}
        self.emprestimos = {}
        
    async def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                async with aiofiles.open(DATA_FILE, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    data = json.loads(content)
                    self.users_data = data.get('users_data', {})
                    self.ligas = data.get('ligas', {})
                    self.confrontos = data.get('confrontos', {})
                    self.emprestimos = data.get('emprestimos', {})
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
    
    async def save_data(self):
        try:
            data = {
                'users_data': self.users_data,
                'ligas': self.ligas,
                'confrontos': self.confrontos,
                'emprestimos': self.emprestimos
            }
            async with aiofiles.open(DATA_FILE, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def get_user_data(self, user_id):
        if str(user_id) not in self.users_data:
            self.users_data[str(user_id)] = {
                'dinheiro': 100000,
                'jogadores': [],
                'escalacao': {
                    'goleiro': None,
                    'zagueiro1': None,
                    'zagueiro2': None,
                    'lateral_esq': None,
                    'lateral_dir': None,
                    'volante': None,
                    'meia': None,
                    'ponta_esq': None,
                    'ponta_dir': None,
                    'atacante1': None,
                    'atacante2': None
                },
                'vitorias': 0,
                'derrotas': 0,
                'empates': 0,
                'jogadores_criados': 0,
                'ultimo_ganho_automatico': None
            }
        return self.users_data[str(user_id)]
    
    def verificar_ganho_automatico(self, user_id):
        user_data = self.get_user_data(user_id)
        agora = datetime.now()
        
        if user_data['ultimo_ganho_automatico'] is None:
            user_data['ultimo_ganho_automatico'] = agora.isoformat()
            return False
        
        ultimo_ganho = datetime.fromisoformat(user_data['ultimo_ganho_automatico'])
        if agora - ultimo_ganho >= timedelta(hours=24):
            user_data['dinheiro'] += 50000
            user_data['ultimo_ganho_automatico'] = agora.isoformat()
            return True
        
        return False

vados = VadosBot()

@bot.event
async def on_ready():
    await vados.load_data()
    print(f'🚀 MXP Football Manager está online e pronto para gerenciar o futebol!')
    print('=' * 50)

# Comando ganho automático
@bot.command(name='ganho_automatico')
async def ganho_automatico(ctx):
    """Coleta seu ganho automático de 50.000 reais (a cada 24h)"""
    user_data = vados.get_user_data(ctx.author.id)
    
    if vados.verificar_ganho_automatico(ctx.author.id):
        embed = discord.Embed(
            title="💰 Ganho Automático Coletado!",
            description="Você coletou seu ganho automático de **R$ 50.000**!",
            color=0x00ff00
        )
        embed.add_field(name="💵 Valor Recebido", value="R$ 50.000", inline=True)
        embed.add_field(name="💰 Saldo Atual", value=f"R$ {user_data['dinheiro']:,}", inline=True)
        embed.add_field(name="⏰ Próximo Ganho", value="Em 24 horas", inline=True)
        embed.set_footer(text="🎉 MXP Football Manager - Ganho automático coletado!")
        await vados.save_data()
    else:
        # Calcula tempo restante
        if user_data['ultimo_ganho_automatico']:
            ultimo_ganho = datetime.fromisoformat(user_data['ultimo_ganho_automatico'])
            proximo_ganho = ultimo_ganho + timedelta(hours=24)
            tempo_restante = proximo_ganho - datetime.now()
            
            if tempo_restante.total_seconds() > 0:
                horas = int(tempo_restante.total_seconds() // 3600)
                minutos = int((tempo_restante.total_seconds() % 3600) // 60)
                
                embed = discord.Embed(
                    title="⏰ Ganho Automático Não Disponível",
                    description=f"Você já coletou seu ganho automático hoje!\n\n⏱️ **Tempo restante:** {horas}h {minutos}min",
                    color=0xff9900
                )
                embed.add_field(name="💰 Saldo Atual", value=f"R$ {user_data['dinheiro']:,}", inline=True)
                embed.add_field(name="💵 Próximo Valor", value="R$ 50.000", inline=True)
            else:
                embed = discord.Embed(
                    title="🔄 Processando...",
                    description="Aguarde um momento e tente novamente.",
                    color=0x0099ff
                )
        else:
            embed = discord.Embed(
                title="🎉 Primeira Coleta!",
                description="Aguarde um momento para processar sua primeira coleta.",
                color=0x0099ff
            )
    
    await ctx.send(embed=embed)

# Event para comandos inválidos
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Comando Não Encontrado",
            description=f"O comando `{ctx.message.content}` não existe!\nUse `-ajuda` para ver todos os comandos disponíveis.",
            color=0xff0000
        )
        embed.set_footer(text="💡 Dica: Verifique se digitou corretamente!")
        await ctx.send(embed=embed)

# Comando para ver o time
@bot.command(name='time')
async def ver_time(ctx, usuario: discord.Member = None):
    """Visualiza o time escalado de um jogador"""
    if usuario is None:
        usuario = ctx.author
    
    user_data = vados.get_user_data(usuario.id)
    escalacao = user_data['escalacao']
    
    embed = discord.Embed(
        title=f"⚽ Time de {usuario.display_name}",
        color=0x00ff00
    )
    
    # Verifica se tem escalação
    jogadores_escalados = [j for j in escalacao.values() if j is not None]
    
    if not jogadores_escalados:
        embed.description = "❌ Nenhum jogador escalado ainda!\nUse `-escalar` para montar seu time."
        embed.color = 0xff9900
    else:
        # Formação visual melhorada
        formacao = f"""
```
                {escalacao['goleiro']['nome'][:12] if escalacao['goleiro'] else '-----'}
                        ({escalacao['goleiro']['habilidade']}%)

    {escalacao['zagueiro1']['nome'][:8] if escalacao['zagueiro1'] else '-----'}        {escalacao['zagueiro2']['nome'][:8] if escalacao['zagueiro2'] else '-----'}
    ({escalacao['zagueiro1']['habilidade']}%)      ({escalacao['zagueiro2']['habilidade']}%)

{escalacao['lateral_esq']['nome'][:8] if escalacao['lateral_esq'] else '-----'}                            {escalacao['lateral_dir']['nome'][:8] if escalacao['lateral_dir'] else '-----'}
({escalacao['lateral_esq']['habilidade']}%)                          ({escalacao['lateral_dir']['habilidade']}%)

         {escalacao['volante']['nome'][:8] if escalacao['volante'] else '-----'}    {escalacao['meia']['nome'][:8] if escalacao['meia'] else '-----'}
         ({escalacao['volante']['habilidade']}%)  ({escalacao['meia']['habilidade']}%)

    {escalacao['ponta_esq']['nome'][:8] if escalacao['ponta_esq'] else '-----'}                    {escalacao['ponta_dir']['nome'][:8] if escalacao['ponta_dir'] else '-----'}
    ({escalacao['ponta_esq']['habilidade']}%)                  ({escalacao['ponta_dir']['habilidade']}%)

         {escalacao['atacante1']['nome'][:8] if escalacao['atacante1'] else '-----'}    {escalacao['atacante2']['nome'][:8] if escalacao['atacante2'] else '-----'}
         ({escalacao['atacante1']['habilidade']}%)  ({escalacao['atacante2']['habilidade']}%)
```
        """
        
        embed.add_field(name="🏟️ Formação Tática", value=formacao, inline=False)
        
        # Calcula força do time
        forca_total = sum(j['habilidade'] for j in jogadores_escalados) / len(jogadores_escalados)
        embed.add_field(name="💪 Força do Time", value=f"{forca_total:.1f}%", inline=True)
        embed.add_field(name="👥 Jogadores Escalados", value=f"{len(jogadores_escalados)}/11", inline=True)
        
        # Status da escalação
        if len(jogadores_escalados) == 11:
            embed.add_field(name="✅ Status", value="Time Completo!", inline=True)
        else:
            embed.add_field(name="⚠️ Status", value="Time Incompleto", inline=True)
    
    # Estatísticas do jogador
    embed.add_field(
        name="📊 Estatísticas", 
        value=f"🏆 {user_data['vitorias']}V | ❌ {user_data['derrotas']}D | 🤝 {user_data['empates']}E",
        inline=False
    )
    
    embed.set_thumbnail(url=usuario.avatar.url if usuario.avatar else None)
    embed.set_footer(text=f"💰 Dinheiro: ${user_data['dinheiro']:,}")
    
    await ctx.send(embed=embed)

# Comando criar jogador melhorado com confirmação
@bot.command(name='criar_jogador')
async def criar_jogador(ctx, nome: str, posicao: str):
    """Cria um jogador personalizado (apenas 1 por pessoa)"""
    user_data = vados.get_user_data(ctx.author.id)
    
    if user_data['jogadores_criados'] >= 1:
        embed = discord.Embed(
            title="❌ Limite Atingido",
            description="Você já criou seu jogador personalizado!\nCada jogador pode criar apenas 1 jogador.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    # Interface de confirmação
    embed = discord.Embed(
        title="⚠️ Confirmação de Criação de Jogador",
        description=f"Você está prestes a criar o jogador **{nome}** na posição **{posicao}**",
        color=0xffff00
    )
    
    embed.add_field(name="📋 Informações Importantes:", value="""
🔸 **Você só pode criar 1 jogador por conta**
🔸 **O jogador não pode ser deletado sem autorização de admin**
🔸 **A habilidade será definida aleatoriamente**
🔸 **O jogador começará com over 50 e evoluirá**
🔸 **Esta ação é irreversível**
    """, inline=False)
    
    embed.add_field(name="⚽ Jogador a Criar:", value=f"**Nome:** {nome}\n**Posição:** {posicao}", inline=True)
    embed.set_footer(text="⚠️ Pense bem antes de confirmar! Esta decisão é permanente.")
    
    view = ConfirmarCriacaoView(nome, posicao, user_data, vados, ctx.author)
    await ctx.send(embed=embed, view=view)

class ConfirmarCriacaoView(discord.ui.View):
    def __init__(self, nome, posicao, user_data, vados_instance, author):
        super().__init__(timeout=120)
        self.nome = nome
        self.posicao = posicao
        self.user_data = user_data
        self.vados = vados_instance
        self.author = author
    
    @discord.ui.button(label="✏️ Editar Jogador", style=discord.ButtonStyle.secondary, emoji="✏️")
    async def editar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Apenas quem criou pode editar!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="💡 Como Editar seu Jogador",
            description="Para editar, use o comando novamente com os dados corretos:",
            color=0x0099ff
        )
        
        embed.add_field(
            name="📝 Comando:",
            value=f"`-criar_jogador <novo_nome> <nova_posição>`",
            inline=False
        )
        
        embed.add_field(
            name="📋 Exemplo:",
            value="`-criar_jogador \"Cristiano Silva\" Atacante`",
            inline=False
        )
        
        embed.set_footer(text="💡 Use aspas se o nome tiver espaços!")
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="✅ Tenho Certeza", style=discord.ButtonStyle.success, emoji="✅")
    async def confirmar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Apenas quem criou pode confirmar!", ephemeral=True)
            return
        
        # Habilidade aleatória baseada no over inicial
        over_inicial = 50
        habilidade_inicial = over_inicial + random.randint(-5, 10)  # Varia entre 45-60
        
        jogador = {
            'nome': self.nome,
            'posicao': self.posicao,
            'habilidade': habilidade_inicial,
            'over': over_inicial,
            'tipo': 'criado',
            'evolucoes': 0
        }
        
        self.user_data['jogadores'].append(jogador)
        self.user_data['jogadores_criados'] += 1
        await self.vados.save_data()
        
        embed = discord.Embed(
            title="🎉 Jogador Criado com Sucesso!",
            description=f"✨ **{self.nome}** foi adicionado ao seu elenco com sucesso!",
            color=0x00ff00
        )
        
        embed.add_field(name="⚽ Nome", value=self.nome, inline=True)
        embed.add_field(name="📍 Posição", value=self.posicao, inline=True)
        embed.add_field(name="📈 Over Inicial", value=over_inicial, inline=True)
        embed.add_field(name="🎯 Habilidade", value=f"{habilidade_inicial}%", inline=True)
        embed.add_field(name="🌟 Tipo", value="Jogador Único", inline=True)
        embed.add_field(name="🔄 Evoluções", value="0", inline=True)
        
        embed.add_field(
            name="💡 Informações:",
            value="• Seu jogador evoluirá conforme joga\n• Habilidade foi definida aleatoriamente\n• Este é seu único jogador criado",
            inline=False
        )
        
        embed.set_footer(text="🌟 Jogador personalizado criado! Use -elenco para visualizar.")
        
        await interaction.response.edit_message(embed=embed, view=None)

# Comando olheiro melhorado - apenas 1 jogador
@bot.command(name='olheiro')
async def olheiro(ctx):
    """Descubra UM jogador disponível no mercado"""
    user_data = vados.get_user_data(ctx.author.id)
    
    # Seleciona UM jogador aleatório baseado na raridade
    chances = []
    for jogador in JOGADORES_OLHEIRO:
        # Quanto maior a habilidade, menor a chance
        chance = max(5, 105 - jogador['habilidade'])
        chances.extend([jogador] * chance)
    
    jogador_encontrado = random.choice(chances)
    
    # Determina raridade baseada na habilidade
    if jogador_encontrado['habilidade'] >= 95:
        raridade = "🌟 LENDÁRIO"
        cor = 0xffd700
    elif jogador_encontrado['habilidade'] >= 90:
        raridade = "💎 ÉPICO"
        cor = 0x9932cc
    elif jogador_encontrado['habilidade'] >= 80:
        raridade = "🔵 RARO"
        cor = 0x0099ff
    else:
        raridade = "⚪ COMUM"
        cor = 0x808080
    
    embed = discord.Embed(
        title="🔍 Relatório do Olheiro",
        description=f"**{raridade}** jogador foi encontrado no mercado!",
        color=cor
    )
    
    embed.add_field(name="👤 Nome", value=f"**{jogador_encontrado['nome']}**", inline=True)
    embed.add_field(name="⚽ Posição", value=jogador_encontrado['posicao'], inline=True)
    embed.add_field(name="📊 Over", value=jogador_encontrado['over'], inline=True)
    embed.add_field(name="🎯 Habilidade", value=f"{jogador_encontrado['habilidade']}%", inline=True)
    embed.add_field(name="💰 Valor de Mercado", value=f"${jogador_encontrado['valor_mercado']:,}", inline=True)
    embed.add_field(name="💳 Seu Dinheiro", value=f"${user_data['dinheiro']:,}", inline=True)
    
    # Adiciona informações extras baseadas na habilidade
    if jogador_encontrado['habilidade'] >= 90:
        embed.add_field(name="📝 Análise", value="⭐ Jogador de elite! Investimento garantido.", inline=False)
    elif jogador_encontrado['habilidade'] >= 80:
        embed.add_field(name="📝 Análise", value="🎯 Bom jogador, pode fazer a diferença no time.", inline=False)
    else:
        embed.add_field(name="📝 Análise", value="💪 Jogador promissor para começar.", inline=False)
    
    embed.set_footer(text="💡 Use os botões abaixo para negociar este jogador!")
    
    view = OlheiroView(jogador_encontrado, user_data, vados, ctx.author)
    await ctx.send(embed=embed, view=view)

class OlheiroView(discord.ui.View):
    def __init__(self, jogador, user_data, vados_instance, author):
        super().__init__(timeout=300)
        self.jogador = jogador
        self.user_data = user_data
        self.vados = vados_instance
        self.author = author
    
    @discord.ui.button(label="💰 Comprar Jogador", style=discord.ButtonStyle.success, emoji="💰")
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Apenas quem usou o comando pode negociar!", ephemeral=True)
            return
            
        if self.user_data['dinheiro'] >= self.jogador['valor_mercado']:
            self.user_data['dinheiro'] -= self.jogador['valor_mercado']
            novo_jogador = {
                'nome': self.jogador['nome'],
                'posicao': self.jogador['posicao'],
                'habilidade': self.jogador['habilidade'],
                'over': self.jogador['over'],
                'tipo': 'comprado'
            }
            self.user_data['jogadores'].append(novo_jogador)
            await self.vados.save_data()
            
            embed = discord.Embed(
                title="🎉 Transferência Concluída!",
                description=f"✅ **{self.jogador['nome']}** foi contratado com sucesso!",
                color=0x00ff00
            )
            embed.add_field(name="⚽ Jogador", value=self.jogador['nome'], inline=True)
            embed.add_field(name="📍 Posição", value=self.jogador['posicao'], inline=True)
            embed.add_field(name="🎯 Habilidade", value=f"{self.jogador['habilidade']}%", inline=True)
            embed.add_field(name="💸 Valor Pago", value=f"${self.jogador['valor_mercado']:,}", inline=True)
            embed.add_field(name="💰 Dinheiro Restante", value=f"${self.user_data['dinheiro']:,}", inline=True)
            embed.add_field(name="📋 Status", value="Adicionado ao Elenco", inline=True)
            embed.set_footer(text="🌟 Jogador permanente adicionado ao seu elenco!")
            
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="💸 Fundos Insuficientes",
                description=f"❌ Você precisa de **${self.jogador['valor_mercado']:,}**\n💰 Você possui: **${self.user_data['dinheiro']:,}**\n💡 Faltam: **${self.jogador['valor_mercado'] - self.user_data['dinheiro']:,}**",
                color=0xff0000
            )
            embed.add_field(name="💡 Dicas para Ganhar Dinheiro:", value="• Participe de confrontos (vitória = $5,000)\n• Empates também dão $2,000\n• Use `-confronto @usuário` para desafiar", inline=False)
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🤝 Empréstimo (1 jogo)", style=discord.ButtonStyle.secondary, emoji="🤝")
    async def emprestar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Apenas quem usou o comando pode negociar!", ephemeral=True)
            return
            
        preco_emprestimo = self.jogador['valor_mercado'] // 4
        
        if self.user_data['dinheiro'] >= preco_emprestimo:
            self.user_data['dinheiro'] -= preco_emprestimo
            
            user_id = str(interaction.user.id)
            if user_id not in self.vados.emprestimos:
                self.vados.emprestimos[user_id] = []
            
            emprestimo = {
                'nome': self.jogador['nome'],
                'posicao': self.jogador['posicao'],
                'habilidade': self.jogador['habilidade'],
                'over': self.jogador['over'],
                'partidas_restantes': 1
            }
            
            self.vados.emprestimos[user_id].append(emprestimo)
            await self.vados.save_data()
            
            embed = discord.Embed(
                title="🤝 Empréstimo Acordado!",
                description=f"✅ **{self.jogador['nome']}** foi emprestado por 1 partida!",
                color=0x00ff00
            )
            embed.add_field(name="⚽ Jogador", value=self.jogador['nome'], inline=True)
            embed.add_field(name="📍 Posição", value=self.jogador['posicao'], inline=True)
            embed.add_field(name="🎯 Habilidade", value=f"{self.jogador['habilidade']}%", inline=True)
            embed.add_field(name="💸 Valor do Empréstimo", value=f"${preco_emprestimo:,}", inline=True)
            embed.add_field(name="💰 Dinheiro Restante", value=f"${self.user_data['dinheiro']:,}", inline=True)
            embed.add_field(name="⏰ Duração", value="1 Partida", inline=True)
            embed.add_field(name="⚠️ Importante:", value="O jogador retornará automaticamente após 1 confronto!", inline=False)
            embed.set_footer(text="🤝 Jogador temporário adicionado! Use -elenco para ver.")
            
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="💸 Fundos Insuficientes para Empréstimo",
                description=f"❌ Você precisa de **${preco_emprestimo:,}** para o empréstimo\n💰 Você possui: **${self.user_data['dinheiro']:,}**\n💡 Faltam: **${preco_emprestimo - self.user_data['dinheiro']:,}**",
                color=0xff0000
            )
            embed.add_field(name="💰 Empréstimo vs Compra:", value=f"• **Empréstimo:** ${preco_emprestimo:,} (1 jogo)\n• **Compra:** ${self.jogador['valor_mercado']:,} (permanente)", inline=False)
            await interaction.response.edit_message(embed=embed, view=self)

# Comando elenco melhorado
@bot.command(name='elenco')
async def elenco(ctx, usuario: discord.Member = None):
    """Visualiza o elenco completo de um jogador"""
    if usuario is None:
        usuario = ctx.author
    
    user_data = vados.get_user_data(usuario.id)
    
    embed = discord.Embed(
        title=f"📋 Elenco de {usuario.display_name}",
        color=0x0099ff
    )
    
    if not user_data['jogadores']:
        embed.description = "❌ Elenco vazio!\n💡 Use `-olheiro` para contratar jogadores ou `-criar_jogador` para criar um."
        embed.color = 0xff9900
        await ctx.send(embed=embed)
        return
    
    # Agrupa por posição
    posicoes = {}
    for jogador in user_data['jogadores']:
        pos = jogador['posicao']
        if pos not in posicoes:
            posicoes[pos] = []
        posicoes[pos].append(jogador)
    
    # Adiciona jogadores por posição
    for posicao, jogadores in posicoes.items():
        jogadores_texto = []
        for jogador in jogadores:
            emoji = "⭐" if jogador['tipo'] == 'criado' else "💰"
            jogadores_texto.append(f"{emoji} **{jogador['nome']}** - {jogador['habilidade']}% (Over: {jogador['over']})")
        
        embed.add_field(
            name=f"⚽ {posicao} ({len(jogadores)})",
            value="\n".join(jogadores_texto),
            inline=False
        )
    
    # Jogadores emprestados
    user_id = str(usuario.id)
    if user_id in vados.emprestimos and vados.emprestimos[user_id]:
        emprestados_texto = []
        for emp in vados.emprestimos[user_id]:
            emprestados_texto.append(f"🤝 **{emp['nome']}** - {emp['habilidade']}% ({emp['partidas_restantes']} jogo restante)")
        
        embed.add_field(
            name="🤝 Emprestados",
            value="\n".join(emprestados_texto),
            inline=False
        )
    
    # Estatísticas do elenco
    total_jogadores = len(user_data['jogadores'])
    media_habilidade = sum(j['habilidade'] for j in user_data['jogadores']) / total_jogadores
    
    embed.add_field(name="👥 Total de Jogadores", value=total_jogadores, inline=True)
    embed.add_field(name="📊 Média de Habilidade", value=f"{media_habilidade:.1f}%", inline=True)
    embed.add_field(name="💰 Patrimônio", value=f"${user_data['dinheiro']:,}", inline=True)
    
    embed.set_thumbnail(url=usuario.avatar.url if usuario.avatar else None)
    embed.set_footer(text="⭐ = Criado | 💰 = Comprado | 🤝 = Emprestado")
    
    await ctx.send(embed=embed)

# Comando escalar com Select Menu
@bot.command(name='escalar')
async def escalar(ctx):
    """Interface moderna para escalar seu time"""
    user_data = vados.get_user_data(ctx.author.id)
    
    if not user_data['jogadores']:
        embed = discord.Embed(
            title="❌ Elenco Vazio",
            description="Você precisa ter jogadores para escalar!\n💡 Use `-olheiro` ou `-criar_jogador` primeiro.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="⚽ Central de Escalação",
        description="Escolha uma posição para escalar um jogador:",
        color=0x0099ff
    )
    
    # Mostra escalação atual
    escalacao_atual = ""
    for pos, jogador in user_data['escalacao'].items():
        if jogador:
            escalacao_atual += f"✅ **{pos.replace('_', ' ').title()}**: {jogador['nome']} ({jogador['habilidade']}%)\n"
        else:
            escalacao_atual += f"❌ **{pos.replace('_', ' ').title()}**: *Vago*\n"
    
    embed.add_field(name="📋 Escalação Atual", value=escalacao_atual, inline=False)
    
    view = EscalacaoSelectView(user_data, vados, ctx.author)
    await ctx.send(embed=embed, view=view)

class EscalacaoSelectView(discord.ui.View):
    def __init__(self, user_data, vados_instance, author):
        super().__init__(timeout=300)
        self.user_data = user_data
        self.vados = vados_instance
        self.author = author
        
        # Select para posições
        self.add_item(PosicaoSelect(user_data, vados_instance, author))

class PosicaoSelect(discord.ui.Select):
    def __init__(self, user_data, vados_instance, author):
        self.user_data = user_data
        self.vados = vados_instance
        self.author = author
        
        options = [
            discord.SelectOption(label="🥅 Goleiro", value="goleiro", emoji="🥅"),
            discord.SelectOption(label="🛡️ Zagueiro 1", value="zagueiro1", emoji="🛡️"),
            discord.SelectOption(label="🛡️ Zagueiro 2", value="zagueiro2", emoji="🛡️"),
            discord.SelectOption(label="◀️ Lateral Esquerdo", value="lateral_esq", emoji="◀️"),
            discord.SelectOption(label="▶️ Lateral Direito", value="lateral_dir", emoji="▶️"),
            discord.SelectOption(label="⚙️ Volante", value="volante", emoji="⚙️"),
            discord.SelectOption(label="🎯 Meia", value="meia", emoji="🎯"),
            discord.SelectOption(label="◀️ Ponta Esquerda", value="ponta_esq", emoji="◀️"),
            discord.SelectOption(label="▶️ Ponta Direita", value="ponta_dir", emoji="▶️"),
            discord.SelectOption(label="⚽ Atacante 1", value="atacante1", emoji="⚽"),
            discord.SelectOption(label="⚽ Atacante 2", value="atacante2", emoji="⚽"),
        ]
        
        super().__init__(placeholder="Escolha uma posição para escalar...", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Apenas quem usou o comando pode escalar!", ephemeral=True)
            return
            
        posicao = self.values[0]
        
        # Cria select para jogadores
        view = JogadorSelectView(self.user_data, self.vados, posicao, self.author)
        
        embed = discord.Embed(
            title=f"⚽ Escalando {posicao.replace('_', ' ').title()}",
            description="Escolha um jogador do seu elenco:",
            color=0x0099ff
        )
        
        await interaction.response.edit_message(embed=embed, view=view)

class JogadorSelectView(discord.ui.View):
    def __init__(self, user_data, vados_instance, posicao, author):
        super().__init__(timeout=300)
        self.user_data = user_data
        self.vados = vados_instance
        self.posicao = posicao
        self.author = author
        
        # Select para jogadores
        self.add_item(JogadorSelect(user_data, vados_instance, posicao, author))
        
        # Botão voltar
        voltar_btn = discord.ui.Button(label="← Voltar", style=discord.ButtonStyle.secondary)
        voltar_btn.callback = self.voltar
        self.add_item(voltar_btn)
    
    async def voltar(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Apenas quem usou o comando pode navegar!", ephemeral=True)
            return
            
        embed = discord.Embed(
            title="⚽ Central de Escalação",
            description="Escolha uma posição para escalar um jogador:",
            color=0x0099ff
        )
        
        view = EscalacaoSelectView(self.user_data, self.vados, self.author)
        await interaction.response.edit_message(embed=embed, view=view)

class JogadorSelect(discord.ui.Select):
    def __init__(self, user_data, vados_instance, posicao, author):
        self.user_data = user_data
        self.vados = vados_instance
        self.posicao = posicao
        self.author = author
        
        options = []
        
        # Lista de jogadores já escalados
        jogadores_escalados = []
        for pos, jogador in user_data['escalacao'].items():
            if jogador and pos != posicao:  # Permite reescalar a mesma posição
                jogadores_escalados.append(jogador['nome'])
        
        # Adiciona jogadores próprios (apenas os não escalados)
        for jogador in user_data['jogadores'][:20]:  # Máximo 20
            if jogador['nome'] not in jogadores_escalados:
                tipo = jogador.get('tipo', 'comprado')
                emoji = "⭐" if tipo == 'criado' else "💰"
                options.append(discord.SelectOption(
                    label=f"{jogador['nome']} - {jogador['habilidade']}%",
                    value=f"proprio_{jogador['nome']}",
                    emoji=emoji,
                    description=f"{jogador['posicao']} | Over: {jogador['over']}"
                ))
        
        # Adiciona jogadores emprestados (apenas os não escalados)
        user_id = str(author.id)
        if hasattr(vados_instance, 'emprestimos') and user_id in vados_instance.emprestimos:
            for jogador in vados_instance.emprestimos[user_id]:
                if jogador['nome'] not in jogadores_escalados:
                    options.append(discord.SelectOption(
                        label=f"{jogador['nome']} (EMP) - {jogador['habilidade']}%",
                        value=f"emprestado_{jogador['nome']}",
                        emoji="🤝",
                        description=f"{jogador['posicao']} | {jogador['partidas_restantes']} jogo restante"
                    ))
        
        if not options:
            options.append(discord.SelectOption(label="Nenhum jogador disponível", value="vazio"))
        
        super().__init__(placeholder="Escolha um jogador...", options=options[:25])  # Discord limit
    
    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            await interaction.response.send_message("❌ Apenas quem usou o comando pode escalar!", ephemeral=True)
            return
            
        if self.values[0] == "vazio":
            await interaction.response.send_message("❌ Nenhum jogador disponível!", ephemeral=True)
            return
        
        tipo, nome = self.values[0].split("_", 1)
        
        # Encontra o jogador
        jogador_escalado = None
        if tipo == "proprio":
            for jogador in self.user_data['jogadores']:
                if jogador['nome'] == nome:
                    jogador_escalado = jogador
                    break
        elif tipo == "emprestado":
            user_id = str(interaction.user.id)
            if user_id in self.vados.emprestimos:
                for jogador in self.vados.emprestimos[user_id]:
                    if jogador['nome'] == nome:
                        jogador_escalado = jogador
                        break
        
        if jogador_escalado:
            self.user_data['escalacao'][self.posicao] = jogador_escalado
            await self.vados.save_data()
            
            embed = discord.Embed(
                title="✅ Jogador Escalado!",
                description=f"**{jogador_escalado['nome']}** foi escalado para **{self.posicao.replace('_', ' ').title()}**!",
                color=0x00ff00
            )
            embed.add_field(name="⚽ Jogador", value=jogador_escalado['nome'], inline=True)
            embed.add_field(name="📍 Posição no Time", value=self.posicao.replace('_', ' ').title(), inline=True)
            embed.add_field(name="🎯 Habilidade", value=f"{jogador_escalado['habilidade']}%", inline=True)
            embed.add_field(name="📋 Posição Original", value=jogador_escalado['posicao'], inline=True)
            embed.add_field(name="📊 Over", value=jogador_escalado['over'], inline=True)
            tipo = jogador_escalado.get('tipo', 'comprado')
            embed.add_field(name="🌟 Tipo", value="Criado" if tipo == 'criado' else "Comprado", inline=True)
            
            embed.set_footer(text="✅ Escalação atualizada! Use -time para ver a formação completa.")
            
            await interaction.response.edit_message(embed=embed, view=None)

# Comando criar liga (apenas owner)
@bot.command(name='criar_liga')
async def criar_liga(ctx, *, nome_liga):
    """Cria uma nova liga (apenas owner)"""
    if ctx.author.id != OWNER_ID:
        embed = discord.Embed(
            title="🚫 Acesso Negado",
            description="Apenas o owner do bot pode criar ligas!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    liga_id = len(vados.ligas) + 1
    vados.ligas[liga_id] = {
        'nome': nome_liga,
        'criador': ctx.author.id,
        'participantes': [ctx.author.id],
        'partidas': [],
        'tabela': {}
    }
    
    await vados.save_data()
    
    embed = discord.Embed(
        title="🏆 Liga Criada!",
        description=f"Liga **{nome_liga}** foi criada com sucesso!",
        color=0x00ff00
    )
    embed.add_field(name="🆔 ID da Liga", value=liga_id, inline=True)
    embed.add_field(name="👑 Criador", value=ctx.author.mention, inline=True)
    embed.set_footer(text="💡 Outros jogadores podem usar -entrar_liga para participar!")
    
    await ctx.send(embed=embed)

# Comando entrar liga
@bot.command(name='entrar_liga')
async def entrar_liga(ctx, liga_id: int):
    """Entra em uma liga existente"""
    if liga_id not in vados.ligas:
        embed = discord.Embed(
            title="❌ Liga Não Encontrada",
            description=f"Não existe liga com ID **{liga_id}**!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    if ctx.author.id in vados.ligas[liga_id]['participantes']:
        embed = discord.Embed(
            title="⚠️ Já Participando",
            description="Você já está nesta liga!",
            color=0xff9900
        )
        await ctx.send(embed=embed)
        return
    
    vados.ligas[liga_id]['participantes'].append(ctx.author.id)
    await vados.save_data()
    
    embed = discord.Embed(
        title="✅ Entrada Confirmada!",
        description=f"Você entrou na liga **{vados.ligas[liga_id]['nome']}**!",
        color=0x00ff00
    )
    embed.add_field(name="🏆 Liga", value=vados.ligas[liga_id]['nome'], inline=True)
    embed.add_field(name="👥 Participantes", value=len(vados.ligas[liga_id]['participantes']), inline=True)
    
    await ctx.send(embed=embed)

# Comando x1 (confronto individual)
@bot.command(name='x1')
async def x1(ctx, oponente: discord.Member):
    """Desafio x1 - apenas 1 jogador de cada lado"""
    if oponente.id == ctx.author.id:
        embed = discord.Embed(
            title="❌ Autodesafio Impossível",
            description="Você não pode desafiar a si mesmo!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    user_data = vados.get_user_data(ctx.author.id)
    oponente_data = vados.get_user_data(oponente.id)
    
    if not user_data['jogadores']:
        embed = discord.Embed(
            title="❌ Sem Jogadores",
            description="Você precisa ter pelo menos 1 jogador!\n💡 Use `-olheiro` para contratar jogadores.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    if not oponente_data['jogadores']:
        embed = discord.Embed(
            title="❌ Oponente Sem Jogadores",
            description=f"{oponente.mention} precisa ter pelo menos 1 jogador!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="⚡ Desafio X1",
        description=f"🔥 **{ctx.author.display_name}** desafiou **{oponente.display_name}** para um X1!",
        color=0xff9900
    )
    
    # Mostra melhor jogador de cada um
    melhor_desafiante = max(user_data['jogadores'], key=lambda x: x['habilidade'])
    melhor_oponente = max(oponente_data['jogadores'], key=lambda x: x['habilidade'])
    
    embed.add_field(name=f"⚡ {ctx.author.display_name}", value=f"**{melhor_desafiante['nome']}**\n{melhor_desafiante['habilidade']}% | {melhor_desafiante['posicao']}", inline=True)
    embed.add_field(name="🆚", value="**VS**", inline=True)
    embed.add_field(name=f"⚡ {oponente.display_name}", value=f"**{melhor_oponente['nome']}**\n{melhor_oponente['habilidade']}% | {melhor_oponente['posicao']}", inline=True)
    
    embed.set_footer(text="⏰ Oponente tem 5 minutos para responder!")
    
    view = X1View(ctx.author, oponente, user_data, oponente_data, vados)
    await ctx.send(embed=embed, view=view)

# Comando confronto melhorado
@bot.command(name='confronto')
async def confronto(ctx, oponente: discord.Member):
    """Desafie outro usuário para um confronto épico"""
    if oponente.id == ctx.author.id:
        embed = discord.Embed(
            title="❌ Autodesafio Impossível",
            description="Você não pode desafiar a si mesmo!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    user_data = vados.get_user_data(ctx.author.id)
    oponente_data = vados.get_user_data(oponente.id)
    
    # Verifica escalações
    escalacao_completa = all(pos for pos in user_data['escalacao'].values())
    oponente_escalacao_completa = all(pos for pos in oponente_data['escalacao'].values())
    
    if not escalacao_completa:
        embed = discord.Embed(
            title="❌ Escalação Incompleta",
            description="Você precisa ter uma escalação completa!\n💡 Use `-escalar` para montar seu time.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    if not oponente_escalacao_completa:
        embed = discord.Embed(
            title="❌ Oponente Sem Escalação",
            description=f"{oponente.mention} precisa ter uma escalação completa!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="⚔️ Desafio de Confronto",
        description=f"🔥 **{ctx.author.display_name}** desafiou **{oponente.display_name}** para um confronto épico!",
        color=0xff9900
    )
    
    # Calcula força dos times
    forca_desafiante = sum(j['habilidade'] for j in user_data['escalacao'].values()) / 11
    forca_oponente = sum(j['habilidade'] for j in oponente_data['escalacao'].values()) / 11
    
    embed.add_field(name=f"💪 {ctx.author.display_name}", value=f"Força: {forca_desafiante:.1f}%", inline=True)
    embed.add_field(name="🆚", value="**VS**", inline=True)
    embed.add_field(name=f"💪 {oponente.display_name}", value=f"Força: {forca_oponente:.1f}%", inline=True)
    
    embed.set_footer(text="⏰ Oponente tem 5 minutos para responder!")
    
    view = ConfrontoView(ctx.author, oponente, user_data, oponente_data, vados)
    await ctx.send(embed=embed, view=view)

class X1View(discord.ui.View):
    def __init__(self, desafiante, oponente, desafiante_data, oponente_data, vados_instance):
        super().__init__(timeout=300)
        self.desafiante = desafiante
        self.oponente = oponente
        self.desafiante_data = desafiante_data
        self.oponente_data = oponente_data
        self.vados = vados_instance
    
    @discord.ui.button(label="✅ Aceitar X1", style=discord.ButtonStyle.success, emoji="⚡")
    async def aceitar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.oponente.id:
            await interaction.response.send_message("❌ Apenas o desafiado pode aceitar!", ephemeral=True)
            return
        
        # Seleciona automaticamente os melhores jogadores
        melhor_desafiante = max(self.desafiante_data['jogadores'], key=lambda x: x['habilidade'])
        melhor_oponente = max(self.oponente_data['jogadores'], key=lambda x: x['habilidade'])
        
        # Simula o X1 com eventos em tempo real
        embed_inicial = discord.Embed(
            title="⚡ X1 EM ANDAMENTO",
            description="🔥 A partida está começando...",
            color=0xffff00
        )
        embed_inicial.add_field(name=f"⚡ {self.desafiante.display_name}", value=f"{melhor_desafiante['nome']}", inline=True)
        embed_inicial.add_field(name="🆚", value="**VS**", inline=True)
        embed_inicial.add_field(name=f"⚡ {self.oponente.display_name}", value=f"{melhor_oponente['nome']}", inline=True)
        
        await interaction.response.edit_message(embed=embed_inicial, view=None)
        
        # Simula eventos
        await self.simular_x1_eventos(interaction, melhor_desafiante, melhor_oponente)
    
    @discord.ui.button(label="❌ Recusar", style=discord.ButtonStyle.danger, emoji="🚫")
    async def recusar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.oponente.id:
            await interaction.response.send_message("❌ Apenas o desafiado pode recusar!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="❌ X1 Recusado",
            description=f"**{self.oponente.display_name}** recusou o X1 de **{self.desafiante.display_name}**.",
            color=0xff0000
        )
        embed.set_footer(text="🐔 Que pena! Talvez na próxima...")
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    async def simular_x1_eventos(self, interaction, jogador1, jogador2):
        eventos = []
        gols_jogador1 = 0
        gols_jogador2 = 0
        
        # Define se é goleiro
        is_goleiro1 = jogador1['posicao'].lower() == 'goleiro'
        is_goleiro2 = jogador2['posicao'].lower() == 'goleiro'
        
        # Simula eventos durante 5 minutos (representando tempo de jogo)
        for minuto in range(1, 6):
            await asyncio.sleep(2)  # Pausa entre eventos
            
            # Determina quem tem a ação baseado na habilidade
            if random.randint(1, 100) <= (jogador1['habilidade'] * 0.7):
                acao_jogador = jogador1
                defensor = jogador2
                atacante_num = 1
            else:
                acao_jogador = jogador2
                defensor = jogador1
                atacante_num = 2
            
            # Tipos de eventos baseados na posição
            evento_tipo = self.determinar_evento(acao_jogador, defensor)
            
            if evento_tipo == "gol":
                if atacante_num == 1:
                    gols_jogador1 += 1
                    if not is_goleiro1:
                        eventos.append(f"⚽ **GOL!** {acao_jogador['nome']} marca um golaço!")
                    else:
                        eventos.append(f"⚽ **GOL!** O goleiro {acao_jogador['nome']} surpreende e marca!")
                else:
                    gols_jogador2 += 1
                    if not is_goleiro2:
                        eventos.append(f"⚽ **GOL!** {acao_jogador['nome']} marca um golaço!")
                    else:
                        eventos.append(f"⚽ **GOL!** O goleiro {acao_jogador['nome']} surpreende e marca!")
            
            elif evento_tipo == "defesa":
                eventos.append(f"🛡️ {defensor['nome']} faz uma defesa espetacular!")
            
            elif evento_tipo == "bloqueio":
                eventos.append(f"🚫 {defensor['nome']} bloqueia o chute de {acao_jogador['nome']}!")
            
            elif evento_tipo == "contra_ataque":
                eventos.append(f"⚡ {acao_jogador['nome']} inicia um contra-ataque perigoso!")
            
            elif evento_tipo == "chute_fora":
                eventos.append(f"📤 {acao_jogador['nome']} chuta para fora por pouco!")
            
            # Atualiza o embed com os eventos
            embed_evento = discord.Embed(
                title=f"⚡ X1 - Minuto {minuto}",
                description=f"**Placar:** {gols_jogador1} x {gols_jogador2}",
                color=0x00ff00 if minuto == 5 else 0xffff00
            )
            
            embed_evento.add_field(
                name="📝 Último Evento",
                value=eventos[-1] if eventos else "Início da partida...",
                inline=False
            )
            
            if len(eventos) > 1:
                embed_evento.add_field(
                    name="📜 Eventos Anteriores",
                    value="\n".join(eventos[-3:-1]) if len(eventos) > 3 else "\n".join(eventos[:-1]),
                    inline=False
                )
            
            await interaction.edit_original_response(embed=embed_evento)
        
        # Resultado final
        await asyncio.sleep(2)
        resultado_embed = self.criar_embed_resultado_x1(gols_jogador1, gols_jogador2, jogador1, jogador2, eventos)
        
        # Atualiza dados dos jogadores
        if gols_jogador1 > gols_jogador2:
            self.desafiante_data['vitorias'] += 1
            self.oponente_data['derrotas'] += 1
            self.desafiante_data['dinheiro'] += 3000  # Prêmio menor para X1
        elif gols_jogador2 > gols_jogador1:
            self.oponente_data['vitorias'] += 1
            self.desafiante_data['derrotas'] += 1
            self.oponente_data['dinheiro'] += 3000
        else:
            self.desafiante_data['empates'] += 1
            self.oponente_data['empates'] += 1
            self.desafiante_data['dinheiro'] += 1500
            self.oponente_data['dinheiro'] += 1500
        
        await self.vados.save_data()
        await interaction.edit_original_response(embed=resultado_embed)
    
    def determinar_evento(self, atacante, defensor):
        # Probabilidades baseadas na diferença de habilidade
        diff_habilidade = atacante['habilidade'] - defensor['habilidade']
        
        # Ajusta probabilidades baseado na posição
        prob_gol = 30
        if atacante['posicao'].lower() in ['atacante', 'ponta']:
            prob_gol += 15
        elif atacante['posicao'].lower() == 'goleiro':
            prob_gol -= 20
        
        if defensor['posicao'].lower() in ['zagueiro', 'goleiro']:
            prob_gol -= 10
        
        # Ajusta pela diferença de habilidade
        prob_gol += diff_habilidade // 5
        prob_gol = max(5, min(prob_gol, 70))  # Entre 5% e 70%
        
        rand = random.randint(1, 100)
        
        if rand <= prob_gol:
            return "gol"
        elif rand <= prob_gol + 20:
            return "defesa"
        elif rand <= prob_gol + 35:
            return "bloqueio"
        elif rand <= prob_gol + 50:
            return "contra_ataque"
        else:
            return "chute_fora"
    
    def criar_embed_resultado_x1(self, gols1, gols2, jogador1, jogador2, eventos):
        embed = discord.Embed(
            title="🏁 X1 FINALIZADO!",
            color=0x00ff00
        )
        
        placar = f"**{self.desafiante.display_name}** {gols1} ⚽ {gols2} **{self.oponente.display_name}**"
        embed.add_field(name="📊 Placar Final", value=placar, inline=False)
        
        if gols1 > gols2:
            embed.add_field(name="🏆 Vencedor", value=f"{self.desafiante.mention} 🎉", inline=True)
            embed.add_field(name="💰 Prêmio", value="R$ 3.000", inline=True)
            embed.color = 0x00ff00
        elif gols2 > gols1:
            embed.add_field(name="🏆 Vencedor", value=f"{self.oponente.mention} 🎉", inline=True)
            embed.add_field(name="💰 Prêmio", value="R$ 3.000", inline=True)
            embed.color = 0x00ff00
        else:
            embed.add_field(name="🤝 Resultado", value="Empate! Ambos recebem R$ 1.500", inline=False)
            embed.color = 0xffff00
        
        # Mostra eventos mais importantes
        eventos_importantes = [e for e in eventos if "GOL" in e]
        if eventos_importantes:
            embed.add_field(
                name="⚽ Gols da Partida",
                value="\n".join(eventos_importantes[-5:]),  # Últimos 5 gols
                inline=False
            )
        
        embed.set_footer(text="⚡ X1 finalizado! Use -stats para ver suas estatísticas.")
        
        return embed

class ConfrontoView(discord.ui.View):
    def __init__(self, desafiante, oponente, desafiante_data, oponente_data, vados_instance):
        super().__init__(timeout=300)
        self.desafiante = desafiante
        self.oponente = oponente
        self.desafiante_data = desafiante_data
        self.oponente_data = oponente_data
        self.vados = vados_instance
    
    @discord.ui.button(label="✅ Aceitar Desafio", style=discord.ButtonStyle.success, emoji="⚔️")
    async def aceitar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.oponente.id:
            await interaction.response.send_message("❌ Apenas o desafiado pode aceitar!", ephemeral=True)
            return
        
        # Inicia a partida com eventos em tempo real
        embed_inicial = discord.Embed(
            title="🏟️ PARTIDA EM ANDAMENTO",
            description="⚽ A partida está começando...",
            color=0xffff00
        )
        embed_inicial.add_field(name=f"🔥 {self.desafiante.display_name}", value="Preparando time...", inline=True)
        embed_inicial.add_field(name="🆚", value="**VS**", inline=True)
        embed_inicial.add_field(name=f"🔥 {self.oponente.display_name}", value="Preparando time...", inline=True)
        
        await interaction.response.edit_message(embed=embed_inicial, view=None)
        
        # Simula eventos em tempo real
        await self.simular_confronto_eventos(interaction)
        
        # Remove jogadores emprestados
        self.remover_emprestados(str(self.desafiante.id))
        self.remover_emprestados(str(self.oponente.id))
        
        await self.vados.save_data()
    
    @discord.ui.button(label="❌ Recusar", style=discord.ButtonStyle.danger, emoji="🚫")
    async def recusar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.oponente.id:
            await interaction.response.send_message("❌ Apenas o desafiado pode recusar!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="❌ Confronto Recusado",
            description=f"**{self.oponente.display_name}** recusou o desafio de **{self.desafiante.display_name}**.",
            color=0xff0000
        )
        embed.set_footer(text="🐔 Que pena! Talvez na próxima...")
        
        await interaction.response.edit_message(embed=embed, view=None)
    
    def calcular_forca_time(self, escalacao):
        return sum(j['habilidade'] for j in escalacao.values()) / 11
    
    def simular_partida(self):
        forca_desafiante = self.calcular_forca_time(self.desafiante_data['escalacao'])
        forca_oponente = self.calcular_forca_time(self.oponente_data['escalacao'])
        
        # Adiciona fator sorte
        forca_desafiante += random.randint(-15, 15)
        forca_oponente += random.randint(-15, 15)
        
        # Simula gols
        gols_desafiante = max(0, int((forca_desafiante / 100) * random.randint(0, 5)))
        gols_oponente = max(0, int((forca_oponente / 100) * random.randint(0, 5)))
        
        vencedor = 'empate'
        if gols_desafiante > gols_oponente:
            vencedor = 'desafiante'
        elif gols_oponente > gols_desafiante:
            vencedor = 'oponente'
        
        # Pênaltis em caso de empate
        penaltis = None
        if vencedor == 'empate':
            penaltis_desafiante = random.randint(0, 5)
            penaltis_oponente = random.randint(0, 5)
            
            while penaltis_desafiante == penaltis_oponente:
                penaltis_desafiante = random.randint(0, 5)
                penaltis_oponente = random.randint(0, 5)
            
            if penaltis_desafiante > penaltis_oponente:
                vencedor = 'desafiante'
            else:
                vencedor = 'oponente'
            
            penaltis = (penaltis_desafiante, penaltis_oponente)
        
        return {
            'gols': (gols_desafiante, gols_oponente),
            'vencedor': vencedor,
            'penaltis': penaltis,
            'forca': (forca_desafiante, forca_oponente)
        }
    
    def criar_embed_resultado(self, resultado):
        embed = discord.Embed(
            title="🏟️ Resultado da Partida",
            color=0x00ff00
        )
        
        gols_desafiante, gols_oponente = resultado['gols']
        
        placar = f"**{self.desafiante.display_name}** {gols_desafiante} ⚽ {gols_oponente} **{self.oponente.display_name}**"
        embed.add_field(name="📊 Placar Final", value=placar, inline=False)
        
        if resultado['penaltis']:
            pen_desafiante, pen_oponente = resultado['penaltis']
            penaltis = f"**{self.desafiante.display_name}** {pen_desafiante} 🥅 {pen_oponente} **{self.oponente.display_name}**"
            embed.add_field(name="🎯 Disputa de Pênaltis", value=penaltis, inline=False)
        
        if resultado['vencedor'] == 'desafiante':
            embed.add_field(name="🏆 Vencedor", value=f"{self.desafiante.mention} 🎉", inline=False)
            embed.add_field(name="💰 Prêmio", value="$5,000", inline=True)
            embed.color = 0x00ff00
        elif resultado['vencedor'] == 'oponente':
            embed.add_field(name="🏆 Vencedor", value=f"{self.oponente.mention} 🎉", inline=False)
            embed.add_field(name="💰 Prêmio", value="$5,000", inline=True)
            embed.color = 0x00ff00
        else:
            embed.add_field(name="🤝 Resultado", value="Empate! Ambos recebem $2,000", inline=False)
            embed.color = 0xffff00
        
        embed.set_footer(text="⚽ Boa partida! Use -stats para ver suas estatísticas.")
        
        return embed
    
    async def simular_confronto_eventos(self, interaction):
        eventos = []
        gols_desafiante = 0
        gols_oponente = 0
        
        escalacao_desafiante = self.desafiante_data['escalacao']
        escalacao_oponente = self.oponente_data['escalacao']
        
        # Simula 9 minutos de jogo com eventos
        for minuto in range(1, 10):
            await asyncio.sleep(3)  # Pausa entre eventos
            
            # Determina qual time tem a posse
            forca_desafiante = self.calcular_forca_time(escalacao_desafiante)
            forca_oponente = self.calcular_forca_time(escalacao_oponente)
            
            if random.randint(1, 100) <= (forca_desafiante / (forca_desafiante + forca_oponente)) * 100:
                time_atacante = "desafiante"
                escalacao_atacante = escalacao_desafiante
                escalacao_defensor = escalacao_oponente
                nome_time_atacante = self.desafiante.display_name
                nome_time_defensor = self.oponente.display_name
            else:
                time_atacante = "oponente"
                escalacao_atacante = escalacao_oponente
                escalacao_defensor = escalacao_desafiante
                nome_time_atacante = self.oponente.display_name
                nome_time_defensor = self.desafiante.display_name
            
            # Gera evento baseado nas posições dos jogadores
            evento = self.gerar_evento_confronto(escalacao_atacante, escalacao_defensor, nome_time_atacante, nome_time_defensor)
            eventos.append(f"⏱️ {minuto}' - {evento['texto']}")
            
            # Verifica se foi gol
            if evento['tipo'] == 'gol':
                if time_atacante == "desafiante":
                    gols_desafiante += 1
                else:
                    gols_oponente += 1
            
            # Atualiza embed com o evento
            embed_minuto = discord.Embed(
                title=f"🏟️ TEMPO REAL - {minuto}º Minuto",
                description=f"**Placar:** {self.desafiante.display_name} {gols_desafiante} x {gols_oponente} {self.oponente.display_name}",
                color=0x00ff00 if evento['tipo'] == 'gol' else 0xffff00
            )
            
            embed_minuto.add_field(
                name="🔥 Último Lance",
                value=evento['texto'],
                inline=False
            )
            
            if len(eventos) > 1:
                eventos_recentes = eventos[-3:] if len(eventos) > 3 else eventos[:-1]
                embed_minuto.add_field(
                    name="📜 Lances Anteriores",
                    value="\n".join(eventos_recentes),
                    inline=False
                )
            
            await interaction.edit_original_response(embed=embed_minuto)
        
        # Resultado final
        await asyncio.sleep(2)
        embed_final = self.criar_embed_resultado_eventos(gols_desafiante, gols_oponente, eventos)
        
        # Atualiza estatísticas e dinheiro
        if gols_desafiante > gols_oponente:
            self.desafiante_data['vitorias'] += 1
            self.oponente_data['derrotas'] += 1
            self.desafiante_data['dinheiro'] += 5000
        elif gols_oponente > gols_desafiante:
            self.oponente_data['vitorias'] += 1
            self.desafiante_data['derrotas'] += 1
            self.oponente_data['dinheiro'] += 5000
        else:
            self.desafiante_data['empates'] += 1
            self.oponente_data['empates'] += 1
            self.desafiante_data['dinheiro'] += 2000
            self.oponente_data['dinheiro'] += 2000
        
        await interaction.edit_original_response(embed=embed_final)
    
    def gerar_evento_confronto(self, escalacao_atacante, escalacao_defensor, nome_atacante, nome_defensor):
        # Seleciona jogadores baseado na probabilidade da posição
        posicoes_ataque = ['atacante1', 'atacante2', 'ponta_esq', 'ponta_dir', 'meia']
        posicoes_meio = ['volante', 'meia']
        posicoes_defesa = ['zagueiro1', 'zagueiro2', 'lateral_esq', 'lateral_dir', 'goleiro']
        
        # Jogador que inicia a jogada
        if random.randint(1, 100) <= 60:  # 60% chance de atacante
            posicoes_iniciais = posicoes_ataque
        else:  # 40% chance de meio-campo
            posicoes_iniciais = posicoes_meio
        
        jogador_atacante = None
        for pos in posicoes_iniciais:
            if escalacao_atacante.get(pos):
                jogador_atacante = escalacao_atacante[pos]
                break
        
        if not jogador_atacante:
            # Fallback para qualquer jogador
            jogador_atacante = next(iter(escalacao_atacante.values()))
        
        # Determina tipo de evento baseado na habilidade
        rand = random.randint(1, 100)
        habilidade_atacante = jogador_atacante['habilidade']
        
        if rand <= 25 + (habilidade_atacante - 75):  # Gol
            return {
                'tipo': 'gol',
                'texto': f"⚽ **GOL DE {jogador_atacante['nome'].upper()}!** Que jogada espetacular do {nome_atacante}!"
            }
        elif rand <= 45:  # Defesa
            # Seleciona defensor
            defensor = self.selecionar_defensor(escalacao_defensor, jogador_atacante)
            if defensor['posicao'].lower() == 'goleiro':
                return {
                    'tipo': 'defesa',
                    'texto': f"🥅 **DEFESA!** {defensor['nome']} faz uma defesa espetacular! {jogador_atacante['nome']} quase marcou!"
                }
            else:
                return {
                    'tipo': 'bloqueio',
                    'texto': f"🛡️ **BLOQUEIO!** {defensor['nome']} bloqueia o chute perigoso de {jogador_atacante['nome']}!"
                }
        elif rand <= 65:  # Contra-ataque
            meio_campista = escalacao_defensor.get('meia') or escalacao_defensor.get('volante')
            if meio_campista:
                return {
                    'tipo': 'contra_ataque',
                    'texto': f"⚡ **CONTRA-ATAQUE!** {meio_campista['nome']} rouba a bola e inicia jogada rápida para o {nome_defensor}!"
                }
            else:
                return {
                    'tipo': 'recuperacao',
                    'texto': f"🔄 **RECUPERAÇÃO!** {nome_defensor} recupera a posse de bola no meio-campo!"
                }
        elif rand <= 80:  # Chute defendido
            return {
                'tipo': 'chute_defendido',
                'texto': f"📤 **PARA FORA!** {jogador_atacante['nome']} chuta forte, mas a bola passa raspando a trave!"
            }
        else:  # Falta ou lateral
            return {
                'tipo': 'falta',
                'texto': f"⚠️ **FALTA!** Jogada dura sobre {jogador_atacante['nome']}, o árbitro marca falta para o {nome_atacante}!"
            }
    
    def selecionar_defensor(self, escalacao_defensor, jogador_atacante):
        pos_atacante = jogador_atacante['posicao'].lower()
        
        # Lógica de quem defende baseado na posição do atacante
        if 'atacante' in pos_atacante or 'ponta' in pos_atacante:
            # Atacantes normalmente enfrentam zagueiros
            defensores_possiveis = ['zagueiro1', 'zagueiro2', 'goleiro']
        elif 'meia' in pos_atacante or 'meio' in pos_atacante:
            # Meias enfrentam volantes ou zagueiros
            defensores_possiveis = ['volante', 'zagueiro1', 'zagueiro2']
        else:
            # Outros enfrentam laterais ou zagueiros
            defensores_possiveis = ['lateral_esq', 'lateral_dir', 'zagueiro1', 'zagueiro2']
        
        # Seleciona defensor disponível
        for pos in defensores_possiveis:
            if escalacao_defensor.get(pos):
                return escalacao_defensor[pos]
        
        # Fallback para goleiro
        return escalacao_defensor.get('goleiro', next(iter(escalacao_defensor.values())))
    
    def criar_embed_resultado_eventos(self, gols_desafiante, gols_oponente, eventos):
        embed = discord.Embed(
            title="🏁 PARTIDA FINALIZADA!",
            color=0x00ff00
        )
        
        placar = f"**{self.desafiante.display_name}** {gols_desafiante} ⚽ {gols_oponente} **{self.oponente.display_name}**"
        embed.add_field(name="📊 Placar Final", value=placar, inline=False)
        
        if gols_desafiante > gols_oponente:
            embed.add_field(name="🏆 Vencedor", value=f"{self.desafiante.mention} 🎉", inline=True)
            embed.add_field(name="💰 Prêmio", value="R$ 5.000", inline=True)
            embed.color = 0x00ff00
        elif gols_oponente > gols_desafiante:
            embed.add_field(name="🏆 Vencedor", value=f"{self.oponente.mention} 🎉", inline=True)
            embed.add_field(name="💰 Prêmio", value="R$ 5.000", inline=True)
            embed.color = 0x00ff00
        else:
            embed.add_field(name="🤝 Resultado", value="Empate! Ambos recebem R$ 2.000", inline=False)
            embed.color = 0xffff00
        
        # Mostra gols da partida
        gols_eventos = [e for e in eventos if "GOL" in e.upper()]
        if gols_eventos:
            embed.add_field(
                name="⚽ Gols da Partida",
                value="\n".join(gols_eventos),
                inline=False
            )
        
        # Mostra lances importantes
        lances_importantes = [e for e in eventos if any(palavra in e.upper() for palavra in ["DEFESA", "BLOQUEIO", "CONTRA-ATAQUE"])]
        if lances_importantes:
            embed.add_field(
                name="🔥 Lances de Destaque",
                value="\n".join(lances_importantes[-3:]),  # Últimos 3 lances importantes
                inline=False
            )
        
        embed.set_footer(text="🏟️ Que partida! Use -stats para ver suas estatísticas atualizadas.")
        
        return embed
    
    def remover_emprestados(self, user_id):
        if user_id in self.vados.emprestimos:
            emprestimos = self.vados.emprestimos[user_id][:]
            for i, emp in enumerate(emprestimos):
                emp['partidas_restantes'] -= 1
                if emp['partidas_restantes'] <= 0:
                    self.vados.emprestimos[user_id].pop(i)
            
            if not self.vados.emprestimos[user_id]:
                del self.vados.emprestimos[user_id]

# Comando stats melhorado
@bot.command(name='stats')
async def stats(ctx, usuario: discord.Member = None):
    """Visualiza estatísticas detalhadas de um jogador"""
    if usuario is None:
        usuario = ctx.author
    
    user_data = vados.get_user_data(usuario.id)
    
    embed = discord.Embed(
        title=f"📊 Estatísticas de {usuario.display_name}",
        color=0x0099ff
    )
    
    total_jogos = user_data['vitorias'] + user_data['derrotas'] + user_data['empates']
    
    # Estatísticas principais
    embed.add_field(name="🏆 Vitórias", value=user_data['vitorias'], inline=True)
    embed.add_field(name="❌ Derrotas", value=user_data['derrotas'], inline=True)
    embed.add_field(name="🤝 Empates", value=user_data['empates'], inline=True)
    
    embed.add_field(name="🎮 Total de Jogos", value=total_jogos, inline=True)
    embed.add_field(name="💰 Dinheiro", value=f"${user_data['dinheiro']:,}", inline=True)
    embed.add_field(name="⚽ Jogadores no Elenco", value=len(user_data['jogadores']), inline=True)
    
    if total_jogos > 0:
        aproveitamento = (user_data['vitorias'] / total_jogos) * 100
        embed.add_field(name="📈 Aproveitamento", value=f"{aproveitamento:.1f}%", inline=True)
        
        # Determina rank baseado no aproveitamento
        if aproveitamento >= 80:
            rank = "🏆 Lendário"
            cor = 0xffd700
        elif aproveitamento >= 60:
            rank = "💎 Experiente"
            cor = 0x9932cc
        elif aproveitamento >= 40:
            rank = "🔵 Intermediário"
            cor = 0x0099ff
        else:
            rank = "⚪ Iniciante"
            cor = 0x808080
        
        embed.add_field(name="🎖️ Classificação", value=rank, inline=True)
        embed.color = cor
    
    # Informações do elenco
    if user_data['jogadores']:
        media_habilidade = sum(j['habilidade'] for j in user_data['jogadores']) / len(user_data['jogadores'])
        embed.add_field(name="📊 Média do Elenco", value=f"{media_habilidade:.1f}%", inline=True)
    
    embed.set_thumbnail(url=usuario.avatar.url if usuario.avatar else None)
    embed.set_footer(text="🌟 Continue jogando para melhorar suas estatísticas!")
    
    await ctx.send(embed=embed)

# Comandos Admin (apenas owner)
@bot.command(name='add_dinheiro')
async def add_dinheiro(ctx, usuario: discord.Member, quantidade: int):
    """Adiciona dinheiro a um usuário (apenas owner)"""
    if ctx.author.id != OWNER_ID:
        embed = discord.Embed(
            title="🚫 Acesso Negado",
            description="Apenas o owner do bot pode usar este comando!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    user_data = vados.get_user_data(usuario.id)
    user_data['dinheiro'] += quantidade
    await vados.save_data()
    
    embed = discord.Embed(
        title="💰 Dinheiro Adicionado!",
        description=f"**R$ {quantidade:,}** foram adicionados para {usuario.mention}",
        color=0x00ff00
    )
    embed.add_field(name="👤 Usuário", value=usuario.mention, inline=True)
    embed.add_field(name="💵 Valor Adicionado", value=f"R$ {quantidade:,}", inline=True)
    embed.add_field(name="💰 Saldo Atual", value=f"R$ {user_data['dinheiro']:,}", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='add_todos_jogadores')
async def add_todos_jogadores(ctx, usuario: discord.Member):
    """Adiciona todos os jogadores disponíveis a um usuário (apenas owner)"""
    if ctx.author.id != OWNER_ID:
        embed = discord.Embed(
            title="🚫 Acesso Negado",
            description="Apenas o owner do bot pode usar este comando!",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    user_data = vados.get_user_data(usuario.id)
    
    # Adiciona todos os jogadores do olheiro
    for jogador_olheiro in JOGADORES_OLHEIRO:
        jogador = {
            'nome': jogador_olheiro['nome'],
            'posicao': jogador_olheiro['posicao'],
            'habilidade': jogador_olheiro['habilidade'],
            'over': jogador_olheiro['over'],
            'tipo': 'admin_grant'
        }
        user_data['jogadores'].append(jogador)
    
    await vados.save_data()
    
    embed = discord.Embed(
        title="⭐ Todos os Jogadores Adicionados!",
        description=f"**{len(JOGADORES_OLHEIRO)}** jogadores foram adicionados para {usuario.mention}",
        color=0x00ff00
    )
    embed.add_field(name="👤 Usuário", value=usuario.mention, inline=True)
    embed.add_field(name="⚽ Jogadores Adicionados", value=len(JOGADORES_OLHEIRO), inline=True)
    embed.add_field(name="📋 Total no Elenco", value=len(user_data['jogadores']), inline=True)
    embed.set_footer(text="🌟 Todos os jogadores foram concedidos pelo administrador!")
    
    await ctx.send(embed=embed)

# Comando ajuda melhorado
@bot.command(name='ajuda')
async def ajuda(ctx):
    """Central de ajuda completa do Vados Bot"""
    embed = discord.Embed(
        title="🤖 MXP Football Manager - Central de Comandos",
        description="⚽ **Seu assistente completo para futebol no Discord!**",
        color=0x0099ff
    )
    
    comandos = {
        "👥 **Gestão de Jogadores**": [
            "`-criar_jogador <nome> <posição>` - Cria seu jogador único (1 por pessoa)",
            "`-olheiro` - Descobre jogadores disponíveis no mercado",
            "`-elenco [@usuário]` - Visualiza elenco completo",
        ],
        "⚽ **Time & Escalação**": [
            "`-escalar` - Interface moderna para escalar seu time",
            "`-time [@usuário]` - Vê a escalação e formação do time",
        ],
        "⚔️ **Confrontos**": [
            "`-confronto @usuário` - Desafia outro jogador (time completo)",
            "`-x1 @usuário` - Desafio X1 com eventos em tempo real",
            "`-stats [@usuário]` - Estatísticas detalhadas de vitórias/derrotas",
        ],
        "💰 **Sistema Econômico**": [
            "`-ganho_automatico` - Coleta R$ 50.000 (a cada 24h)",
        ],
        "🏆 **Ligas** (Owner only)": [
            "`-criar_liga <nome>` - Cria uma nova liga",
            "`-entrar_liga <id>` - Entra em uma liga existente",
        ],
        "👑 **Comandos Admin** (Owner only)": [
            "`-add_dinheiro @usuário <valor>` - Adiciona dinheiro",
            "`-add_todos_jogadores @usuário` - Dá todos os jogadores",
        ],
        "ℹ️ **Utilitários**": [
            "`-ajuda` - Mostra esta central de comandos",
        ]
    }
    
    for categoria, lista_comandos in comandos.items():
        embed.add_field(
            name=categoria,
            value="\n".join(lista_comandos),
            inline=False
        )
    
    embed.add_field(
        name="💡 **Dicas Importantes**",
        value="• Ganho automático de R$ 50.000 a cada 24h\n• X1 tem eventos em tempo real com narrativa\n• Confrontos completos vs X1 têm prêmios diferentes\n• Jogadores criados evoluem com o tempo",
        inline=False
    )
    
    embed.set_footer(text="🌟 Use o prefixo - antes de cada comando | Bot criado com ❤️")
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild and ctx.guild.icon else None)
    
    await ctx.send(embed=embed)

# Token do bot
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN:
    bot.run("MTM3NjA1MzkxMTg5MDE2OTkwNw.GybP0g.xVRiP9Oo6464uX1JLc6WqczfSJHD_9r1BC23lU")
else:
    print("❌ Token do Discord não encontrado!")
    print("Configure a variável de ambiente DISCORD_BOT_TOKEN ou adicione nas Secrets do Replit")
