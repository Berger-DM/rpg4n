import discord
from discord.ext import commands


class DeletesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def msg_clear(self, ctx, amount=3):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'\"clear_message\" chamado; {amount} mensagens apagadas.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, motive=None):
        await member.kick(reason=motive)
        await ctx.send(f' User {member} kickado do servidor. Motivo: {motive}.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, motive=None):
        await member.ban(reason=motive)
        await ctx.send(f' User {member} banido do servidor. Motivo: {motive}.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'User {user.mention} desbanido do servidor.')
                return


def setup(bot):
    bot.add_cog(DeletesCog(bot))
