from discord.ext import commands
from discord.utils import get

base_role_names = ["Organização", "Narradores", "@everyone", "Admin"]


class ShowCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def get_username(self, ctx):
        name = ctx.author.name
        print(name)
        guild = ctx.guild
        members = guild.members
        print(members)
        sender = get(guild.members, display_name=name)
        print(sender)
        await ctx.send(sender.mention)

    @commands.command(aliases=["roles"])
    @commands.has_permissions(manage_roles=True)
    async def show_roles(self, ctx):
        roles = ctx.guild.roles
        roles.pop(0)
        await ctx.send('Roles no momento:')
        for role in roles:
            await ctx.send(f'{role.name}')

    @commands.command(aliases=["categs"])
    @commands.has_permissions(manage_channels=True)
    async def show_cats(self, ctx):
        cats = ctx.guild.categories
        await ctx.send('Categorias e/ou mesas no momento:')
        for cat in cats:
            await ctx.send(f'{cat.name}')

    @commands.command(aliases=["games", "mesas"])
    async def show_games(self, ctx):
        excluded_categories = base_role_names + [x for x in ctx.guild.categories if x.name.endswith('Bot')] + \
                              ["Principal", "Voice Channels"]
        games = [x for x in ctx.guild.categories if x.name not in excluded_categories]
        await ctx.send('Mesas registradas no momento:')
        if games:
            for game in games:
                await ctx.send(f'{game.name}')
        else:
            await ctx.send('Não há nenhuma mesa registrada no momento.')


def setup(bot):
    bot.add_cog(ShowCog(bot))
