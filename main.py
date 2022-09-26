import discord

intents = discord.Intents.default()
intents.messages = True
intents.members = True

from discord.ext import commands
bot = commands.Bot(command_prefix='%', intents=intents)

@bot.event
async def on_ready():
    print('Online')

    guilg = await bot.fetch_guild(647798243207544842)
    bot.tree.copy_global_to(guild=guilg)
    await bot.tree.sync(guild=guilg)


@bot.event
async def on_message(ctx):
    await bot.process_commands(ctx)

@bot.tree.command(name=f'ping', description=f'ping kurde')
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("ping")








with open(f'token.txt', 'r') as f:
    token = f.read()

bot.run(token)
