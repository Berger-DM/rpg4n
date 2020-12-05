import discord

from discord.utils import get
from discord.ext import commands

narr = "Narradores"


class GameControlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["nova_mesa"])
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def create_game_setup(self, ctx, game_name: str):
        guild = ctx.guild
        game_role = get(guild.roles, name=game_name)
        if game_role is None:
            role = await guild.create_role(name=game_name)
            category = await guild.create_category(name=game_name)
            text_ch_created = await guild.create_text_channel(name="canal-de-texto", category=get(ctx.guild.categories,
                                                                                                  name=game_name))
            await guild.create_voice_channel(name="canal-de-audio", category=get(ctx.guild.categories, name=game_name))
            await category.set_permissions(guild.default_role, read_messages=True, send_messages=False, speak=False,
                                           stream=False, add_reactions=False)
            other_role = get(guild.roles, name=narr)
            sidekick = get(guild.roles, name="Sidekick Bot")
            await category.set_permissions(other_role, read_messages=True, send_messages=False, speak=False,
                                           stream=False, add_reactions=False)
            await category.set_permissions(role, send_messages=True, speak=True, stream=True)
            await category.set_permissions(sidekick, send_messages=True)
            return text_ch_created
        else:
            await ctx.send(f'Mesa \"{game_name}\" já existe!')
            return None

    @commands.command(aliases=["apaga_mesa"])
    @commands.has_permissions(manage_channels=True)
    async def cleanup_game_setup(self, ctx, game_name: str):
        guild = ctx.guild
        if game_name.startswith('[FECHADA] '):
            true_game_name = game_name.split(' ', 1)[1]
            print(true_game_name)
        else:
            true_game_name = game_name
        game_role = get(guild.roles, name=true_game_name)
        game_members = game_role.members
        narr_role = get(guild.roles, name=narr)
        for member in game_members:
            if member in narr_role.members:
                await member.remove_roles(narr_role)
        game_category = get(guild.categories, name=game_name)
        category_id = game_category.id
        text_channel = get(guild.text_channels, category_id=category_id)
        voice_channel = get(guild.voice_channels, category_id=category_id)
        await text_channel.delete()
        await voice_channel.delete()
        await game_category.delete()
        await game_role.delete()
        await ctx.send(f'Mesa \"{true_game_name}\" removida.')

    @commands.command(aliases=["limpa_mesas"])
    @commands.has_permissions(manage_channels=True)
    async def cleanup_full_games(self, ctx):
        guild = ctx.guild
        full_games = [x.name for x in guild.categories if x.name.startswith('[FECHADA]')]
        for full_game in full_games:
            await ctx.invoke(self.bot.get_command('cleanup_game_setup'), game_name=full_game)
        await ctx.send('Todas as mesas [FECHADAS] removidas.')

    @commands.command(aliases=["narra_mesa"])
    @commands.has_permissions(manage_channels=True, manage_permissions=True)
    async def game_claim(self, ctx, member: discord.Member, game_name):
        guild = ctx.guild
        try:
            category = get(guild.categories, name=game_name)
        except Exception as e:
            await ctx.send(f'Algo deu errado na obtenção das permissões para {game_name}. Verifique as informações e '
                           f'tente novamente.')
            print(e)
            return
        else:
            role = get(guild.roles, name="Narradores")
            await member.add_roles(role)
            game_role = get(guild.roles, name=game_name)
            await member.add_roles(game_role)
            await category.set_permissions(member, send_messages=True, speak=True, stream=True, manage_messages=True,
                                           attach_files=True, mute_members=True)
            text_ch = get(category.text_channels)
            msg = await text_ch.send(f'{member.mention} narrará a mesa {game_name}!')
            return msg

    @commands.command(aliases=["libera_mesa"])
    @commands.has_permissions(manage_channels=True, manage_permissions=True)
    async def game_strip(self, ctx, member: discord.Member, game_name):
        guild = ctx.guild
        try:
            category = get(guild.categories, name=game_name)
        except Exception as e:
            await ctx.send(f'Algo deu errado na obtenção das permissões para {game_name}. Verifique as informações '
                           f'e tente novamente.')
            print(e)
            return
        else:
            role = get(guild.roles, name="Narradores")
            game_role = get(guild.roles, name=game_name)
            await member.remove_roles(role)
            await member.remove_roles(game_role)
            perm_overwrite = discord.PermissionOverwrite(read_messages=None, send_messages=None, speak=None,
                                                         stream=None,
                                                         manage_messages=None, attach_files=None, mute_members=None)
            await category.set_permissions(member, overwrite=perm_overwrite)
            await ctx.send(f'{member.mention} não narrará a mesa {game_name}.')

    @commands.command(aliases=["aluga_bot"])
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def rent_a_bot(self,ctx, bot_role_name):
        bot = bot_role_name
        guild = ctx.guild
        category_id = ctx.channel.category_id
        category = get(guild.categories, id=category_id)
        roles_names = [x.name for x in guild.roles]
        if bot not in roles_names:
            if not bot.endswith(' Bot'):
                bot += ' Bot'
                if bot not in roles_names:
                    await ctx.send(f'{bot_role_name} não é um bot ou não está configurado no servidor.')
                    return
                else:
                    bot_role = get(guild.roles, name=bot)
                    await category.set_permissions(bot_role, send_messages=True, speak=True, connect=True,
                                                   add_reactions=True, embed_links=True, read_message_history=True,
                                                   use_external_emojis=True, use_voice_activation=True)
                    await ctx.send(f'{bot_role_name} recebeu permissões nesta mesa.')
            else:
                if not bot.endswith(' Bot'):
                    await ctx.send(f'{bot_role_name} não é um bot.')
                else:
                    bot_role = get(guild.roles, name=bot)
                    await category.set_permissions(bot_role, send_messages=True, speak=True)
                    await ctx.send(f'{bot_role_name} recebeu permissões nesta mesa.')


    @commands.command()
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def pull_and_set(self, ctx):
        mesas = list()
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                mesas = await connection.fetch("SELECT * FROM mesas WHERE NOT posted")
                print(mesas)
                for mesa in mesas:
                    print(mesa)
                    print(mesa['discorduser'])
                    guild = ctx.guild
                    user = get(guild.members, display_name=mesa['discorduser'])
                    print(user)
                    composed_announce = list()
                    composed_announce.append(mesa['titulo'].upper())
                    composed_announce.append(mesa['sinopse'])
                    composed_announce.append('')
                    composed_announce.append(f'Narrador(a): {user.mention} ({mesa["name"]})')
                    composed_announce.append(f'Gênero/Cenário: {mesa["genero"]}')
                    composed_announce.append(f'Sistema: {mesa["sistema"]}')
                    composed_announce.append(f'Idade mínima: {mesa["minima"]}')
                    composed_announce.append('--------------------------------')
                    composed_announce.append('--------------------------------')
                    full_message = '\n'.join(composed_announce)
                    await ctx.send(full_message)
                    text_ch = await self.bot.get_command("create_game_setup")(ctx, mesa['titulo'])
                    if text_ch is None:
                        continue
                    await text_ch.send(full_message)
                    msg = await self.bot.get_command("game_claim")(ctx, user, mesa['titulo'])
                    await msg.delete()
                await connection.execute("UPDATE mesas SET posted = NOT posted WHERE posted = FALSE")
        return


def setup(bot):
    bot.add_cog(GameControlCog(bot))
