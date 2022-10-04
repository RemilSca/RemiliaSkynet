
import asyncio
import discord
from discord.ext import tasks
import tohu
import datetime as dt
import czapki as cp






intents = discord.Intents.default()
intents.messages = True
intents.members = True

from discord.ext import commands
bot = commands.Bot(command_prefix='%', intents=discord.Intents.all())




@bot.event
async def on_ready():
    print('Online')

    guilg = await bot.fetch_guild(647798243207544842)
    bot.tree.copy_global_to(guild=guilg)
    await bot.tree.sync(guild=guilg)
    msg1.start()
    morde.start()

@commands.is_owner()
@bot.command()
async def newword(ctx):
    x = cp.new()
    await ctx.send(f'{x}')

@bot.command()
async def rejestrw(ctx):
    x = cp.create(str(ctx.author.id))
    await ctx.send(f'{x}')

@bot.command()
async def zgadnij(ctx, message):
    x = cp.verify(message, str(ctx.author.id))
    await ctx.send(f'{x}')

@bot.command()
async def statystyki(ctx):
    x = cp.stats(str(ctx.author.id))
    await ctx.send(f'{x}')
@commands.is_owner()
@bot.command()
async def resetw(ctx):
    x = cp.reset()
    await ctx.send(f'{x}')


@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)
    if ctx.author != bot.user:
        if isinstance(ctx.channel, discord.channel.DMChannel):
            pass

@bot.tree.command(name=f'ping', description=f'ping kurde')
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("ping")

@bot.tree.command(name=f'upload', description=f'Przeslij swoj replay')
async def upload(interaction: discord.Interaction) -> None:

    ID = interaction.channel.id
    channel = bot.get_channel(int(ID))

    message = await channel.fetch_message(channel.last_message_id)


    if str(message.attachments) == "[]":  # Checks if there is an attachment on the message
        return
    else:  # If there is it gets the filename from message.attachments
        split_v1 = str(message.attachments).split("filename='")[1]
        filename = str(split_v1).split("' ")[0]
        if filename.endswith(".rpy"):  # Checks if it is a .csv file
            await message.attachments[0].save(fp=f'replays/{interaction.user.id}.rpy')
            x = tohu.parse(interaction.user.id)
            await interaction.response.send_message(f'{x}')
        else:
            await interaction.response.send_message(f'To nie jest plik replayu')

@bot.tree.command(name=f'weekstats', description=f'Pokazuje statystyki tego tygodnia')
async def weekstats(interaction: discord.Interaction) -> None:
    f = open(f'week', 'r')
    week = eval(f.read())
    f.close()
    x = f'Weekly challange to: {week["g"]} {week["t"]} {week["m"]} {week["c"]}\n'
    scores = tohu.sta()
    for y in scores:
        us = bot.get_user(int(y[0]))
        x += f'{us.display_name} score: {y[1]} stage:{y[2]}\n'
    await interaction.response.send_message(f'{x}')

@bot.tree.command(name=f'getkey', description=f'Pokazuje klucz którym masz podpisać replay')
async def getkey(interaction: discord.Interaction) -> None:
    id = interaction.user.id
    u = tohu.floady(id)
    klucz = u.akey
    x = f'Twój klucz to {klucz}'
    await interaction.response.send_message(f'{x}')

@bot.tree.command(name=f'register', description=f'Rejestruje konto do weekly challangu')
async def register(interaction: discord.Interaction) -> None:
    id = interaction.user.id
    x = tohu.create(id)
    await interaction.response.send_message(f'{x}')

@bot.tree.command(name=f'staty', description=f'Pokazuje statystyki')
async def staty(interaction: discord.Interaction) -> None:
    scores = tohu.staty()
    x = f''
    for y in scores:
        us = bot.get_user(int(y[0]))
        x += f'{us.display_name} Liczba punktow:{y[1]}\n'
    await interaction.response.send_message(f'{x}')


@commands.is_owner()
@bot.tree.command(name=f'override', description=f'dupa')
async def override(interaction: discord.Interaction, userid:str, score:str, stage:str) -> None:
    u = tohu.floady(userid)
    u.stage = int(stage)
    u.lastscore = int(score)
    u.submit = True
    tohu.save(u)
    await interaction.response.send_message(f'Zapisano wynik :hopium:')

@commands.is_owner()
@bot.tree.command(name=f'endweek', description=f'konczytydzien (debug)')
async def endweek(interaction: discord.Interaction) -> None:
    await endw()
    await interaction.response.send_message(f'juz')

# 7 days => 24 hour * 7 days = 168
@tasks.loop(hours=168)
async def msg1():
    await endw()


@msg1.before_loop
async def before_msg1():
    # loop the whole 7 day (60 sec 60 min 24 hours 7 days)
    for _ in range(60*60*24*7):
        if dt.datetime.utcnow().strftime("%H:%M UTC %w") == "10:00 UTC 0":

            print('It is time')
            return

        # wait some time before another loop. Don't make it more than 60 sec or it will skip
        await asyncio.sleep(30)
async def endw():

    wyg = (tohu.endweek())
    if type(wyg) is type(0):
        g = await bot.fetch_guild(647798243207544842)
        c = await g.fetch_channel(790562786992193548)
        await c.send(f'Weekly danmaku challange wygrał: <@!{wyg}>')
        x = tohu.newweek()
        await c.send(f'Nowy weekly challange to: {x["g"]} {x["t"]} {x["m"]} {x["c"]}')
    else:
        g = await bot.fetch_guild(647798243207544842)
        c = await g.fetch_channel(790562786992193548)
        await c.send(f'Weekly danmaku challange wygrał: Nikt!')
        x = tohu.newweek()
        await c.send(f'Nowy weekly challange to: {x["g"]} {x["t"]} {x["m"]} {x["c"]}')



@tasks.loop(hours=24)
async def morde():
    await resetw()
    await newword()

@morde.before_loop
async def before_morde():
    # loop the whole 7 day (60 sec 60 min 24 hours 7 days)
    for _ in range(60*60*24):
        if dt.datetime.utcnow().strftime("%H:%M") == "10:00":

            print('It is time')
            return

        # wait some time before another loop. Don't make it more than 60 sec or it will skip
        await asyncio.sleep(30)





with open(f'token.txt', 'r') as f:
    token = f.read()


bot.run(token)
