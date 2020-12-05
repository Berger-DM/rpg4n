import os
import ssl
import csv
import asyncio
import asyncpg
import discord
from discord.utils import get
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')
extensions = ['cogs.deletes', 'cogs.event_set', 'cogs.events', 'cogs.feedback', 'cogs.game_control', 'cogs.helps',
              'cogs.show']
load_dotenv(find_dotenv())

if __name__ == "__main__":
    for extension in extensions:
        client.load_extension(extension)

org = "Organização"
org_permissions = discord.Permissions.all()
narr = "Narradores"


# BASE BOT COMMANDS

# Server setup commands
@client.command(aliases=["init_server"])
@commands.has_permissions(manage_roles=True)
async def init_base_roles(ctx):
    guild = ctx.guild
    if get(ctx.guild.roles, name=org) is None:
        await guild.create_role(name=org, permissions=org_permissions, hoist=True)
    else:
        print(f'Role \"{org}\" already exists in the server.')
    if get(ctx.guild.roles, name=narr) is None:
        await guild.create_role(name=narr, permissions=guild.default_role.permissions, hoist=True)
    else:
        print(f'Role \"{narr}\" already exists in the server.')


@client.command(aliases=["org"])
@commands.has_permissions(manage_roles=True)
async def org_role(ctx, member: discord.Member):
    role = get(ctx.guild.roles, name="Organização")
    await member.add_roles(role)


# NEXT LEVEL COMMANDS - USE THOSE ABOVE THEM
@client.command()
@commands.has_permissions(manage_channels=True)
async def grab_games(ctx):
    message = ctx.message
    print("entrou no try")
    attach = message.attachments[0]
    await attach.save('file.csv')
    first_line = False
    if Path('file.csv').is_file():
        with Path('file.csv').open() as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                if not first_line:
                    first_line = True
                    continue
                timestamp = row[0]
                nome = row[1]
                discorduser = row[2]
                titulo = row[7]
                sinopse = row[8]
                genero = row[9]
                sistema = row[10]
                minima = row[11]
                print('\n'.join([timestamp, nome, discorduser, titulo, sinopse, genero, sistema, minima]))
                async with client.pool.acquire() as connection:
                    async with connection.transaction():
                        await connection.execute(
                                "INSERT INTO mesas "
                                "VALUES ($1, $2, $3, $4, $5, $6, $7, $8) "
                                "ON CONFLICT (timestamp) DO NOTHING",
                                timestamp, nome, discorduser, titulo, sinopse, genero, sistema, minima)
    else:
        print('Não tá encontrando file.csv nessa merda de bagulho do caralho fdp')

    print("finalizou try")
    print("chegou no finally")
    return


# Event control commands
@client.command(aliases=["rpg4n"])
@commands.has_permissions(manage_channels=True)
async def launch_event(ctx):
    emoji = "\N{GAME DIE}"
    guild = ctx.guild
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            mesas_turno = await connection.fetch("SELECT * FROM mesas")
            if not mesas_turno:
                await ctx.send("Sem mesas registradas para este turno no Banco de Mesas do RPG4N")
                return
            titulos_mesas = [x['titulo'] for x in mesas_turno]
            cats = [x for x in guild.categories if x.name in titulos_mesas]
            print(cats)
            for category in cats:
                cat_id = category.id
                text_channel = get(guild.text_channels, category_id=cat_id)
                launch_msg = await text_channel.send("Se você quer se increver para essa mesa, adicione a reação "
                                                     ":game_die: a este post!")
                await launch_msg.add_reaction(emoji)
            text_ch = get(guild.text_channels, name="taverna")
            await text_ch.send(
                f'{guild.default_role}, o evento se inicia! Entre no canal de texto da sua mesa desejada e '
                f'se inscreva adicionando a reação indicada.')
    return


heroku_url = os.getenv("DATABASE_URL")
ssl_obj = ssl.create_default_context(cafile='./rds-combined-ca-bundle.pem')
ssl_obj.check_hostname = False
ssl_obj.verify_mode = ssl.CERT_NONE
loop = asyncio.get_event_loop()
client.pool = loop.run_until_complete(asyncpg.create_pool(dsn=heroku_url, ssl=ssl_obj))
client.run(os.getenv("TOKEN"), bot='true')
