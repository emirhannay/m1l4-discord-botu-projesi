# This example requires the 'members' and 'message_content' privileged intents to function.
# Cihan Efe
import discord
from discord.ext import commands
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Merhaba! Ben {bot.user}, bir Discord sohbet botuyum!')

#?add 2 3
@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(right + left)

# Hatalı argüman hatası, eğer kullanıcı geçerli argümanlar girmezse tetiklenir.
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Lütfen geçerli iki sayı girin.")

#?roll 2d6
@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

#?choose elma armut üzüm
@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *parametre: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(parametre))

#?repeat 3 merhaba
@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

#?joined @kullanıcı
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


#Bu, bir ana komut (grup komutu) oluşturur. Yani bu komutun altında başka alt komutlar çalıştırılabilir.
@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

#Bu ise, yukarıdaki cool komutunun alt komutudur. Yani sadece ?cool bot gibi yazarsan çalışır.
@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

#EK
@bot.group()
async def animal(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Hangi hayvanı diyorsun?")

@animal.command()
async def cat(ctx):
    await ctx.send("Miyav!")

@animal.command()
async def dog(ctx):
    await ctx.send("Hav hav!")
#EK SON

bot.run('TOKENİM')
