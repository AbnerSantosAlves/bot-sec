
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
                'jogadores_criados': 0
            }
        return self.users_data[str(user_id)]

vados = VadosBot()

@bot.event
async def on_ready():
    await vados.load_data()
    print(f'🚀 {bot.user} está online e pronto para gerenciar o futebol!')
    print('=' * 50)

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
        
        # Adiciona jogadores próprios
        for jogador in user_data['jogadores'][:20]:  # Máximo 20
            emoji = "⭐" if jogador['tipo'] == 'criado' else "💰"
            options.append(discord.SelectOption(
                label=f"{jogador['nome']} - {jogador['habilidade']}%",
                value=f"proprio_{jogador['nome']}",
                emoji=emoji,
                description=f"{jogador['posicao']} | Over: {jogador['over']}"
            ))
        
        # Adiciona jogadores emprestados
        user_id = str(author.id)
        if hasattr(vados_instance, 'emprestimos') and user_id in vados_instance.emprestimos:
            for jogador in vados_instance.emprestimos[user_id]:
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
            embed.add_field(name="🌟 Tipo", value="Criado" if jogador_escalado['tipo'] == 'criado' else "Comprado", inline=True)
            
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
        
        resultado = self.simular_partida()
        embed = self.criar_embed_resultado(resultado)
        
        # Atualiza estatísticas e dinheiro
        if resultado['vencedor'] == 'desafiante':
            self.desafiante_data['vitorias'] += 1
            self.oponente_data['derrotas'] += 1
            self.desafiante_data['dinheiro'] += 5000  # Prêmio por vitória
        elif resultado['vencedor'] == 'oponente':
            self.oponente_data['vitorias'] += 1
            self.desafiante_data['derrotas'] += 1
            self.oponente_data['dinheiro'] += 5000  # Prêmio por vitória
        else:
            self.desafiante_data['empates'] += 1
            self.oponente_data['empates'] += 1
            self.desafiante_data['dinheiro'] += 2000  # Prêmio menor por empate
            self.oponente_data['dinheiro'] += 2000
        
        # Remove jogadores emprestados
        self.remover_emprestados(str(self.desafiante.id))
        self.remover_emprestados(str(self.oponente.id))
        
        await self.vados.save_data()
        await interaction.response.edit_message(embed=embed, view=None)
    
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

# Comando ajuda melhorado
@bot.command(name='ajuda')
async def ajuda(ctx):
    """Central de ajuda completa do Vados Bot"""
    embed = discord.Embed(
        title="🤖 Vados Bot - Central de Comandos",
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
            "`-confronto @usuário` - Desafia outro jogador",
            "`-stats [@usuário]` - Estatísticas detalhadas de vitórias/derrotas",
        ],
        "🏆 **Ligas** (Owner only)": [
            "`-criar_liga <nome>` - Cria uma nova liga",
            "`-entrar_liga <id>` - Entra em uma liga existente",
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
        value="• Cada jogador pode criar apenas 1 jogador personalizado\n• Jogadores criados têm habilidade aleatória (45-60%)\n• Empréstimos duram apenas 1 partida\n• Vitórias dão $5,000 e empates $2,000",
        inline=False
    )
    
    embed.set_footer(text="🌟 Use o prefixo - antes de cada comando | Bot criado com ❤️")
    embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild and ctx.guild.icon else None)
    
    await ctx.send(embed=embed)

# Token do bot
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Token do Discord não encontrado!")
    print("Configure a variável de ambiente DISCORD_BOT_TOKEN ou adicione nas Secrets do Replit")
