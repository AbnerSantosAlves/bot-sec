
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
    {"nome": "Oliver Santos", "posicao": "Goleiro", "over": 80, "habilidade": 82, "preco": 50000},
    {"nome": "Zargão", "posicao": "Zagueiro", "over": 80, "habilidade": 82, "preco": 45000},
    {"nome": "Bruno", "posicao": "Zagueiro", "over": 84, "habilidade": 86, "preco": 60000},
    {"nome": "Anthony", "posicao": "Meia", "over": 85, "habilidade": 87, "preco": 65000},
    {"nome": "Lewis Ferguson", "posicao": "Atacante", "over": 79, "habilidade": 78, "preco": 40000},
    {"nome": "Saulo Bezerra", "posicao": "Atacante", "over": 88, "habilidade": 89, "preco": 80000},
    {"nome": "Pedro Caldas", "posicao": "Atacante", "over": 85, "habilidade": 87, "preco": 65000},
    {"nome": "Brunno Santos", "posicao": "Meio Campo", "over": 80, "habilidade": 82, "preco": 45000},
    {"nome": "Zau", "posicao": "Goleiro", "over": 88, "habilidade": 89, "preco": 75000},
    {"nome": "Hiroshi", "posicao": "Goleiro", "over": 84, "habilidade": 86, "preco": 55000},
    {"nome": "Sassa", "posicao": "Goleiro", "over": 76, "habilidade": 75, "preco": 35000},
    {"nome": "Oliver Wayne", "posicao": "Zagueiro", "over": 91, "habilidade": 93, "preco": 100000},
    {"nome": "Corvino", "posicao": "Ponta", "over": 86, "habilidade": 88, "preco": 70000},
    {"nome": "Pdrz", "posicao": "Atacante", "over": 86, "habilidade": 88, "preco": 70000},
    {"nome": "Nott", "posicao": "Meio", "over": 83, "habilidade": 85, "preco": 55000},
    {"nome": "Keven", "posicao": "Atacante", "over": 86, "habilidade": 88, "preco": 70000},
    {"nome": "Ronaldinho Cruzeiro", "posicao": "Ponta", "over": 84, "habilidade": 86, "preco": 60000},
    {"nome": "Carlos Cruzeiro", "posicao": "Meio", "over": 85, "habilidade": 87, "preco": 65000},
    {"nome": "Gustavo Soares", "posicao": "Meia-Central", "over": 82, "habilidade": 83, "preco": 50000},
    {"nome": "Crazy", "posicao": "Ponta", "over": 88, "habilidade": 89, "preco": 80000},
    {"nome": "Pietro", "posicao": "Volante", "over": 80, "habilidade": 82, "preco": 45000},
    {"nome": "Matheus Taylor", "posicao": "Ponta Esq.", "over": 96, "habilidade": 98, "preco": 150000},
    {"nome": "Juliano Henrique", "posicao": "Atacante", "over": 99, "habilidade": 100, "preco": 200000},
    {"nome": "Michael Owen", "posicao": "Goleiro", "over": 99, "habilidade": 100, "preco": 200000},
    {"nome": "Phillipe Guedes", "posicao": "Atacante", "over": 88, "habilidade": 89, "preco": 80000},
    {"nome": "Prince", "posicao": "Ponta Direita", "over": 91, "habilidade": 93, "preco": 100000},
    {"nome": "Hiroshi", "posicao": "Zagueiro", "over": 90, "habilidade": 92, "preco": 95000},
    {"nome": "Felipe Botelho", "posicao": "Meio Campo", "over": 87, "habilidade": 88, "preco": 75000},
    {"nome": "M. De Light", "posicao": "Zagueiro", "over": 90, "habilidade": 92, "preco": 95000},
    {"nome": "Kai Guedes", "posicao": "Ponta Dir.", "over": 90, "habilidade": 92, "preco": 95000},
    {"nome": "Macaé", "posicao": "Atacante", "over": 89, "habilidade": 90, "preco": 85000},
    {"nome": "Lucas Bask", "posicao": "Zagueiro", "over": 79, "habilidade": 78, "preco": 40000},
    {"nome": "Sam Ker", "posicao": "Atacante", "over": 75, "habilidade": 74, "preco": 30000},
    {"nome": "Jake Willy", "posicao": "Atacante", "over": 69, "habilidade": 68, "preco": 25000},
    {"nome": "Zake Zau", "posicao": "Volante", "over": 80, "habilidade": 82, "preco": 45000},
    {"nome": "Helena Silva", "posicao": "Zagueira", "over": 70, "habilidade": 70, "preco": 28000},
    {"nome": "Luan Alves", "posicao": "Goleiro", "over": 69, "habilidade": 68, "preco": 25000},
    {"nome": "Fernando M.", "posicao": "Atacante", "over": 71, "habilidade": 71, "preco": 30000},
    {"nome": "Coutinho S.", "posicao": "Meio Campo", "over": 69, "habilidade": 68, "preco": 25000},
    {"nome": "Kaio Becker", "posicao": "Zagueiro", "over": 67, "habilidade": 66, "preco": 22000},
    {"nome": "Caio Miguel", "posicao": "Goleiro", "over": 69, "habilidade": 68, "preco": 25000},
    {"nome": "Alex", "posicao": "Volante", "over": 75, "habilidade": 74, "preco": 32000},
    {"nome": "Matheus Mtzx", "posicao": "Ponta Dir.", "over": 70, "habilidade": 70, "preco": 28000}
]

# Arquivo para salvar dados
DATA_FILE = "vados_bot_data.json"

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
                'empates': 0
            }
        return self.users_data[str(user_id)]

vados = VadosBot()

@bot.event
async def on_ready():
    await vados.load_data()
    print(f'🚀 {bot.user} está online e pronto para gerenciar o futebol!')
    print('=' * 50)

# Comando para criar jogador personalizado
@bot.command(name='criar_jogador')
async def criar_jogador(ctx, nome: str, posicao: str, habilidade: int = None):
    """Cria um jogador personalizado para seu time"""
    user_data = vados.get_user_data(ctx.author.id)
    
    if habilidade is None:
        habilidade = random.randint(60, 85)
    
    habilidade = max(50, min(100, habilidade))
    
    jogador = {
        'nome': nome,
        'posicao': posicao,
        'habilidade': habilidade,
        'over': habilidade - random.randint(0, 5),
        'tipo': 'criado'
    }
    
    user_data['jogadores'].append(jogador)
    await vados.save_data()
    
    embed = discord.Embed(
        title="⚽ Jogador Criado!",
        description=f"**{nome}** foi adicionado ao seu elenco!",
        color=0x00ff00
    )
    embed.add_field(name="Posição", value=posicao, inline=True)
    embed.add_field(name="Habilidade", value=f"{habilidade}%", inline=True)
    embed.add_field(name="Over", value=jogador['over'], inline=True)
    
    await ctx.send(embed=embed)

# Comando olheiro
@bot.command(name='olheiro')
async def olheiro(ctx):
    """Veja jogadores disponíveis para contratação"""
    user_data = vados.get_user_data(ctx.author.id)
    
    # Chance de aparecer jogadores baseada na habilidade (mais difícil = menos chance)
    jogadores_disponiveis = []
    for jogador in JOGADORES_OLHEIRO:
        chance = 100 - (jogador['habilidade'] - 50)  # Jogadores melhores têm menos chance
        if random.randint(1, 100) <= chance:
            jogadores_disponiveis.append(jogador)
    
    if not jogadores_disponiveis:
        embed = discord.Embed(
            title="🔍 Olheiro",
            description="Nenhum jogador disponível no momento. Tente novamente!",
            color=0xff9900
        )
        await ctx.send(embed=embed)
        return
    
    # Limita a 5 jogadores por vez
    jogadores_disponiveis = random.sample(jogadores_disponiveis, min(5, len(jogadores_disponiveis)))
    
    embed = discord.Embed(
        title="🔍 Olheiro - Jogadores Disponíveis",
        description="Escolha um jogador para ver as opções de contratação",
        color=0x0099ff
    )
    
    for i, jogador in enumerate(jogadores_disponiveis, 1):
        embed.add_field(
            name=f"{i}. {jogador['nome']}",
            value=f"**Posição:** {jogador['posicao']}\n**Over:** {jogador['over']}\n**Habilidade:** {jogador['habilidade']}%",
            inline=True
        )
    
    view = OlheiroView(jogadores_disponiveis, user_data, vados)
    await ctx.send(embed=embed, view=view)

class OlheiroView(discord.ui.View):
    def __init__(self, jogadores, user_data, vados_instance):
        super().__init__(timeout=300)
        self.jogadores = jogadores
        self.user_data = user_data
        self.vados = vados_instance
        
        for i, jogador in enumerate(jogadores):
            button = discord.ui.Button(
                label=f"{i+1}. {jogador['nome'][:15]}",
                style=discord.ButtonStyle.primary,
                custom_id=f"jogador_{i}"
            )
            button.callback = self.create_callback(i)
            self.add_item(button)
    
    def create_callback(self, index):
        async def callback(interaction):
            jogador = self.jogadores[index]
            embed = discord.Embed(
                title=f"⚽ {jogador['nome']}",
                description=f"**Posição:** {jogador['posicao']}\n**Over:** {jogador['over']}\n**Habilidade:** {jogador['habilidade']}%",
                color=0x0099ff
            )
            
            preco_compra = jogador['preco']
            preco_emprestimo = preco_compra // 4
            
            embed.add_field(name="💰 Comprar", value=f"${preco_compra:,}", inline=True)
            embed.add_field(name="🤝 Emprestar (1 partida)", value=f"${preco_emprestimo:,}", inline=True)
            embed.add_field(name="💳 Seu dinheiro", value=f"${self.user_data['dinheiro']:,}", inline=True)
            
            view = ContratacaoView(jogador, self.user_data, self.vados)
            await interaction.response.edit_message(embed=embed, view=view)
        
        return callback

class ContratacaoView(discord.ui.View):
    def __init__(self, jogador, user_data, vados_instance):
        super().__init__(timeout=300)
        self.jogador = jogador
        self.user_data = user_data
        self.vados = vados_instance
    
    @discord.ui.button(label="💰 Comprar", style=discord.ButtonStyle.success)
    async def comprar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user_data['dinheiro'] >= self.jogador['preco']:
            self.user_data['dinheiro'] -= self.jogador['preco']
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
                title="✅ Compra Realizada!",
                description=f"**{self.jogador['nome']}** foi contratado com sucesso!",
                color=0x00ff00
            )
            embed.add_field(name="Valor pago", value=f"${self.jogador['preco']:,}", inline=True)
            embed.add_field(name="Dinheiro restante", value=f"${self.user_data['dinheiro']:,}", inline=True)
            
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="❌ Dinheiro Insuficiente",
                description=f"Você precisa de ${self.jogador['preco']:,} mas possui apenas ${self.user_data['dinheiro']:,}",
                color=0xff0000
            )
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="🤝 Emprestar", style=discord.ButtonStyle.secondary)
    async def emprestar(self, interaction: discord.Interaction, button: discord.ui.Button):
        preco_emprestimo = self.jogador['preco'] // 4
        
        if self.user_data['dinheiro'] >= preco_emprestimo:
            self.user_data['dinheiro'] -= preco_emprestimo
            
            # Adiciona ao empréstimo temporário
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
                title="✅ Empréstimo Realizado!",
                description=f"**{self.jogador['nome']}** foi emprestado por 1 partida!",
                color=0x00ff00
            )
            embed.add_field(name="Valor pago", value=f"${preco_emprestimo:,}", inline=True)
            embed.add_field(name="Dinheiro restante", value=f"${self.user_data['dinheiro']:,}", inline=True)
            
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed = discord.Embed(
                title="❌ Dinheiro Insuficiente",
                description=f"Você precisa de ${preco_emprestimo:,} mas possui apenas ${self.user_data['dinheiro']:,}",
                color=0xff0000
            )
            await interaction.response.edit_message(embed=embed, view=self)

# Comando para ver elenco
@bot.command(name='elenco')
async def elenco(ctx):
    """Veja seu elenco atual"""
    user_data = vados.get_user_data(ctx.author.id)
    
    if not user_data['jogadores']:
        embed = discord.Embed(
            title="📋 Seu Elenco",
            description="Você ainda não possui jogadores. Use `-olheiro` ou `-criar_jogador` para começar!",
            color=0xff9900
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="📋 Seu Elenco",
        description=f"💰 Dinheiro: ${user_data['dinheiro']:,}",
        color=0x0099ff
    )
    
    # Agrupa jogadores por posição
    posicoes = {}
    for jogador in user_data['jogadores']:
        pos = jogador['posicao']
        if pos not in posicoes:
            posicoes[pos] = []
        posicoes[pos].append(jogador)
    
    for posicao, jogadores in posicoes.items():
        jogadores_texto = []
        for jogador in jogadores:
            jogadores_texto.append(f"**{jogador['nome']}** - {jogador['habilidade']}% (Over: {jogador['over']})")
        
        embed.add_field(
            name=f"⚽ {posicao}",
            value="\n".join(jogadores_texto),
            inline=False
        )
    
    # Adiciona jogadores emprestados se houver
    user_id = str(ctx.author.id)
    if user_id in vados.emprestimos and vados.emprestimos[user_id]:
        emprestados_texto = []
        for emp in vados.emprestimos[user_id]:
            emprestados_texto.append(f"**{emp['nome']}** - {emp['habilidade']}% ({emp['partidas_restantes']} partida restante)")
        
        embed.add_field(
            name="🤝 Emprestados",
            value="\n".join(emprestados_texto),
            inline=False
        )
    
    await ctx.send(embed=embed)

# Comando para escalar time
@bot.command(name='escalar')
async def escalar(ctx):
    """Interface para escalar seu time"""
    user_data = vados.get_user_data(ctx.author.id)
    
    if not user_data['jogadores']:
        embed = discord.Embed(
            title="❌ Sem Jogadores",
            description="Você precisa ter jogadores para escalar! Use `-olheiro` ou `-criar_jogador`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
        return
    
    view = EscalacaoView(user_data, vados)
    embed = view.get_escalacao_embed()
    await ctx.send(embed=embed, view=view)

class EscalacaoView(discord.ui.View):
    def __init__(self, user_data, vados_instance):
        super().__init__(timeout=300)
        self.user_data = user_data
        self.vados = vados_instance
        
        posicoes = [
            ("Goleiro", "goleiro"),
            ("Zagueiro 1", "zagueiro1"),
            ("Zagueiro 2", "zagueiro2"),
            ("Lateral Esq", "lateral_esq"),
            ("Lateral Dir", "lateral_dir"),
            ("Volante", "volante"),
            ("Meia", "meia"),
            ("Ponta Esq", "ponta_esq"),
            ("Ponta Dir", "ponta_dir"),
            ("Atacante 1", "atacante1"),
            ("Atacante 2", "atacante2")
        ]
        
        for nome, key in posicoes[:5]:  # Primeira linha de botões
            button = discord.ui.Button(label=nome, style=discord.ButtonStyle.secondary)
            button.callback = self.create_escalacao_callback(key, nome)
            self.add_item(button)
    
    def create_escalacao_callback(self, posicao_key, posicao_nome):
        async def callback(interaction):
            view = JogadorSelectView(self.user_data, self.vados, posicao_key, posicao_nome, self)
            embed = discord.Embed(
                title=f"Escolha um jogador para {posicao_nome}",
                description="Selecione um jogador do seu elenco:",
                color=0x0099ff
            )
            await interaction.response.edit_message(embed=embed, view=view)
        return callback
    
    def get_escalacao_embed(self):
        embed = discord.Embed(
            title="⚽ Escalação do Time",
            description="Clique nas posições para escalar jogadores",
            color=0x0099ff
        )
        
        formacao = """
```
        {goleiro}
    
{lateral_esq}  {zagueiro1}  {zagueiro2}  {lateral_dir}

      {volante}    {meia}

{ponta_esq}              {ponta_dir}

   {atacante1}  {atacante2}
```
        """
        
        escalacao = self.user_data['escalacao']
        jogadores_escalados = {}
        
        for pos, jogador in escalacao.items():
            if jogador:
                nome = jogador['nome'][:8]  # Limita o nome
                jogadores_escalados[pos] = nome
            else:
                jogadores_escalados[pos] = "-----"
        
        embed.add_field(
            name="📋 Formação Atual",
            value=formacao.format(**jogadores_escalados),
            inline=False
        )
        
        return embed

class JogadorSelectView(discord.ui.View):
    def __init__(self, user_data, vados_instance, posicao_key, posicao_nome, parent_view):
        super().__init__(timeout=300)
        self.user_data = user_data
        self.vados = vados_instance
        self.posicao_key = posicao_key
        self.posicao_nome = posicao_nome
        self.parent_view = parent_view
        
        # Adiciona jogadores próprios
        for i, jogador in enumerate(user_data['jogadores'][:20]):  # Máximo 20 jogadores
            button = discord.ui.Button(
                label=f"{jogador['nome'][:15]} - {jogador['habilidade']}%",
                style=discord.ButtonStyle.primary
            )
            button.callback = self.create_select_callback(jogador)
            self.add_item(button)
        
        # Adiciona jogadores emprestados
        user_id = str(list(user_data.keys())[0] if user_data else "unknown")  # Gambiarra para pegar o user_id
        if hasattr(self.vados, 'emprestimos') and user_id in self.vados.emprestimos:
            for jogador in self.vados.emprestimos[user_id]:
                button = discord.ui.Button(
                    label=f"{jogador['nome'][:15]} (EMP) - {jogador['habilidade']}%",
                    style=discord.ButtonStyle.success
                )
                button.callback = self.create_select_callback(jogador)
                self.add_item(button)
        
        # Botão voltar
        voltar_btn = discord.ui.Button(label="← Voltar", style=discord.ButtonStyle.secondary)
        voltar_btn.callback = self.voltar
        self.add_item(voltar_btn)
    
    def create_select_callback(self, jogador):
        async def callback(interaction):
            self.user_data['escalacao'][self.posicao_key] = jogador
            await self.vados.save_data()
            
            embed = self.parent_view.get_escalacao_embed()
            embed.description = f"✅ {jogador['nome']} foi escalado para {self.posicao_nome}!"
            
            await interaction.response.edit_message(embed=embed, view=self.parent_view)
        return callback
    
    async def voltar(self, interaction):
        embed = self.parent_view.get_escalacao_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)

# Comando para confronto
@bot.command(name='confronto')
async def confronto(ctx, oponente: discord.Member):
    """Desafie outro usuário para um confronto"""
    if oponente.id == ctx.author.id:
        await ctx.send("❌ Você não pode desafiar a si mesmo!")
        return
    
    user_data = vados.get_user_data(ctx.author.id)
    oponente_data = vados.get_user_data(oponente.id)
    
    # Verifica se ambos têm escalação completa
    escalacao_completa = all(pos for pos in user_data['escalacao'].values())
    oponente_escalacao_completa = all(pos for pos in oponente_data['escalacao'].values())
    
    if not escalacao_completa:
        await ctx.send("❌ Você precisa ter uma escalação completa! Use `-escalar`")
        return
    
    if not oponente_escalacao_completa:
        await ctx.send(f"❌ {oponente.mention} precisa ter uma escalação completa!")
        return
    
    embed = discord.Embed(
        title="⚔️ Desafio de Confronto",
        description=f"{ctx.author.mention} desafiou {oponente.mention} para um confronto!",
        color=0xff9900
    )
    
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
    
    @discord.ui.button(label="✅ Aceitar", style=discord.ButtonStyle.success)
    async def aceitar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.oponente.id:
            await interaction.response.send_message("❌ Apenas o desafiado pode aceitar!", ephemeral=True)
            return
        
        resultado = self.simular_partida()
        embed = self.criar_embed_resultado(resultado)
        
        # Atualiza estatísticas
        if resultado['vencedor'] == 'desafiante':
            self.desafiante_data['vitorias'] += 1
            self.oponente_data['derrotas'] += 1
        elif resultado['vencedor'] == 'oponente':
            self.oponente_data['vitorias'] += 1
            self.desafiante_data['derrotas'] += 1
        else:
            self.desafiante_data['empates'] += 1
            self.oponente_data['empates'] += 1
        
        # Remove jogadores emprestados após a partida
        self.remover_emprestados(str(self.desafiante.id))
        self.remover_emprestados(str(self.oponente.id))
        
        await self.vados.save_data()
        await interaction.response.edit_message(embed=embed, view=None)
    
    @discord.ui.button(label="❌ Recusar", style=discord.ButtonStyle.danger)
    async def recusar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.oponente.id:
            await interaction.response.send_message("❌ Apenas o desafiado pode recusar!", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="❌ Confronto Recusado",
            description=f"{self.oponente.mention} recusou o desafio.",
            color=0xff0000
        )
        await interaction.response.edit_message(embed=embed, view=None)
    
    def calcular_forca_time(self, escalacao):
        forca_total = 0
        for jogador in escalacao.values():
            if jogador:
                forca_total += jogador['habilidade']
        return forca_total / 11  # Média da habilidade
    
    def simular_partida(self):
        forca_desafiante = self.calcular_forca_time(self.desafiante_data['escalacao'])
        forca_oponente = self.calcular_forca_time(self.oponente_data['escalacao'])
        
        # Adiciona elemento aleatório
        forca_desafiante += random.randint(-10, 10)
        forca_oponente += random.randint(-10, 10)
        
        # Simula gols baseado na força
        gols_desafiante = max(0, int((forca_desafiante / 100) * random.randint(0, 4)))
        gols_oponente = max(0, int((forca_oponente / 100) * random.randint(0, 4)))
        
        # Determina vencedor
        if gols_desafiante > gols_oponente:
            vencedor = 'desafiante'
        elif gols_oponente > gols_desafiante:
            vencedor = 'oponente'
        else:
            vencedor = 'empate'
        
        # Se empate, vai para pênaltis
        penaltis = None
        if vencedor == 'empate':
            penaltis_desafiante = random.randint(0, 5)
            penaltis_oponente = random.randint(0, 5)
            
            if penaltis_desafiante > penaltis_oponente:
                vencedor = 'desafiante'
            elif penaltis_oponente > penaltis_desafiante:
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
            title="⚽ Resultado da Partida",
            color=0x00ff00
        )
        
        gols_desafiante, gols_oponente = resultado['gols']
        
        placar = f"{self.desafiante.display_name} {gols_desafiante} x {gols_oponente} {self.oponente.display_name}"
        embed.add_field(name="📊 Placar", value=placar, inline=False)
        
        if resultado['penaltis']:
            pen_desafiante, pen_oponente = resultado['penaltis']
            embed.add_field(
                name="🥅 Pênaltis",
                value=f"{self.desafiante.display_name} {pen_desafiante} x {pen_oponente} {self.oponente.display_name}",
                inline=False
            )
        
        if resultado['vencedor'] == 'desafiante':
            embed.add_field(name="🏆 Vencedor", value=self.desafiante.mention, inline=False)
        elif resultado['vencedor'] == 'oponente':
            embed.add_field(name="🏆 Vencedor", value=self.oponente.mention, inline=False)
        else:
            embed.add_field(name="🤝 Resultado", value="Empate!", inline=False)
        
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

# Comando para criar liga
@bot.command(name='criar_liga')
async def criar_liga(ctx, *, nome_liga):
    """Cria uma nova liga"""
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
    embed.add_field(name="ID da Liga", value=liga_id, inline=True)
    embed.add_field(name="Criador", value=ctx.author.mention, inline=True)
    
    await ctx.send(embed=embed)

# Comando para entrar em liga
@bot.command(name='entrar_liga')
async def entrar_liga(ctx, liga_id: int):
    """Entra em uma liga existente"""
    if liga_id not in vados.ligas:
        await ctx.send("❌ Liga não encontrada!")
        return
    
    if ctx.author.id in vados.ligas[liga_id]['participantes']:
        await ctx.send("❌ Você já está nesta liga!")
        return
    
    vados.ligas[liga_id]['participantes'].append(ctx.author.id)
    await vados.save_data()
    
    embed = discord.Embed(
        title="✅ Entrada na Liga",
        description=f"Você entrou na liga **{vados.ligas[liga_id]['nome']}**!",
        color=0x00ff00
    )
    
    await ctx.send(embed=embed)

# Comando para ver estatísticas
@bot.command(name='stats')
async def stats(ctx, usuario: discord.Member = None):
    """Veja suas estatísticas ou de outro jogador"""
    if usuario is None:
        usuario = ctx.author
    
    user_data = vados.get_user_data(usuario.id)
    
    embed = discord.Embed(
        title=f"📊 Estatísticas de {usuario.display_name}",
        color=0x0099ff
    )
    
    total_jogos = user_data['vitorias'] + user_data['derrotas'] + user_data['empates']
    
    embed.add_field(name="🏆 Vitórias", value=user_data['vitorias'], inline=True)
    embed.add_field(name="❌ Derrotas", value=user_data['derrotas'], inline=True)
    embed.add_field(name="🤝 Empates", value=user_data['empates'], inline=True)
    embed.add_field(name="🎮 Total de Jogos", value=total_jogos, inline=True)
    embed.add_field(name="💰 Dinheiro", value=f"${user_data['dinheiro']:,}", inline=True)
    embed.add_field(name="⚽ Jogadores", value=len(user_data['jogadores']), inline=True)
    
    if total_jogos > 0:
        aproveitamento = (user_data['vitorias'] / total_jogos) * 100
        embed.add_field(name="📈 Aproveitamento", value=f"{aproveitamento:.1f}%", inline=True)
    
    await ctx.send(embed=embed)

# Comando de ajuda personalizado
@bot.command(name='ajuda')
async def ajuda(ctx):
    """Mostra todos os comandos disponíveis"""
    embed = discord.Embed(
        title="🤖 Vados Bot - Comandos",
        description="Bot para gerenciamento de futebol no Discord",
        color=0x0099ff
    )
    
    comandos = {
        "👥 **Jogadores**": [
            "`-criar_jogador <nome> <posição> [habilidade]` - Cria um jogador personalizado",
            "`-olheiro` - Vê jogadores disponíveis para contratação",
            "`-elenco` - Mostra seu elenco atual"
        ],
        "⚽ **Time**": [
            "`-escalar` - Interface para escalar seu time",
            "`-confronto @usuário` - Desafia outro usuário",
            "`-stats [@usuário]` - Vê estatísticas de vitórias/derrotas"
        ],
        "🏆 **Ligas**": [
            "`-criar_liga <nome>` - Cria uma nova liga",
            "`-entrar_liga <id>` - Entra em uma liga existente"
        ],
        "ℹ️ **Outros**": [
            "`-ajuda` - Mostra esta mensagem"
        ]
    }
    
    for categoria, lista_comandos in comandos.items():
        embed.add_field(
            name=categoria,
            value="\n".join(lista_comandos),
            inline=False
        )
    
    embed.set_footer(text="Use o prefixo - antes de cada comando")
    await ctx.send(embed=embed)

# Token do bot (substitua pelo seu token)
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Token do Discord não encontrado!")
    print("Configure a variável de ambiente DISCORD_BOT_TOKEN ou adicione nas Secrets do Replit")
