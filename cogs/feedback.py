from discord.ext import commands
from discord.utils import get

org_channel_id = 700079115918770345
org = "Organização"


class FeedbackCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Feedback and compalaints commands
    @commands.command()
    async def feedback(self, ctx):
        user = ctx.message.author
        if ctx.message.guild:
            await ctx.message.delete()
            await user.send("Olá, parece que você tentou mandar feedback sobre o RPG4N em um canal aberto."
                            "\nPor segurança, preferimos que feedbacks e denúncias sejam enviadas por mensagem privada "
                            "para o bot. Use o comando que você acabou de utilizar - !feedback - por aqui mesmo, "
                            "e seu feedback chegará aos organizadores do evento!")
        else:
            msg = ctx.message.content
            msg = msg.replace("!feedback ", "")
            org_channel = self.bot.get_channel(org_channel_id)
            guild = org_channel.guild
            org_role = get(guild.roles, name=org)
            await org_channel.send(f'{org_role.mention} Feedback de {user}: {msg}')
            await user.send('Feedback recebido! Obrigado por ajudar a tornar o RPG4N um evento melhor!')

    @commands.command()
    async def feedback_anon(self, ctx):
        user = ctx.message.author
        if ctx.message.guild:
            await ctx.message.delete()
            await user.send('Olá, parece que você tentou mandar feedback anônimo sobre o RPG4N em um canal aberto. '
                            'Não se preocupe, ninguém da organização consegue ver esta conversa. '
                            'Sua anonimidade está protegida.'
                            '\nPor segurança, preferimos que feedbacks e denúncias sejam '
                            'enviadas por mensagem privada para o bot. Use o comando que você acabou de utilizar - '
                            '!feedback_anon - por aqui mesmo, e seu feedback chegará aos organizadores do evento!')
        else:
            msg = ctx.message.content
            msg = msg.replace("!feedback_anon ", "")
            org_channel = self.bot.get_channel(org_channel_id)
            guild = org_channel.guild
            org_role = get(guild.roles, name=org)
            await org_channel.send(f'{org_role.mention} Feedback anônimo: {msg}')
            await user.send('Feedback recebido! Obrigado por ajudar a tornar o RPG4N um evento melhor! '
                            'Seu nome não será divulgado para a organização.')

    @commands.command()
    async def denuncia(self, ctx):
        user = ctx.message.author
        if ctx.message.guild:
            await ctx.message.delete()
            await user.send('Olá, parece que você tentou mandar uma denúncia sobre algo no RPG4N em um canal aberto.'
                            '\nPor segurança, preferimos que feedbacks e denúncias sejam enviadas por mensagem privada '
                            'para o bot. Use o comando que você acabou de utilizar - !denuncia - por aqui mesmo, '
                            'e seu feedback chegará aos organizadores do evento!')
        else:
            msg = ctx.message.content
            user = ctx.message.author
            msg = msg.replace("!denuncia ", "")
            org_channel = self.bot.get_channel(org_channel_id)
            guild = org_channel.guild
            org_role = get(guild.roles, name=org)
            await org_channel.send(f'{org_role.mention} Denúncia de {user}: {msg}')
            await user.send('Denúncia recebida. Obrigado por ajudar a tornar o RPG4N um evento melhor!')

    @commands.command()
    async def denuncia_anon(self, ctx):
        user = ctx.message.author
        if ctx.message.guild:
            await ctx.message.delete()
            await user.send('Olá, parece que você tentou mandar uma denúncia anônima sobre algo no RPG4N em um '
                            'canal aberto. Não se preocupe, ninguém da organização consegue ver esta conversa. '
                            'Sua anonimidade está protegida.\nPor segurança, preferimos que feedbacks e denúncias '
                            'sejam enviadas por mensagem privada para o bot. Use o comando que você acabou de utilizar '
                            '- !denuncia_anon - por aqui mesmo, e seu feedback chegará aos organizadores do evento!')
        else:
            msg = ctx.message.content
            msg = msg.replace("!denuncia_anon ", "")
            org_channel = self.bot.get_channel(org_channel_id)
            guild = org_channel.guild
            org_role = get(guild.roles, name=org)
            await org_channel.send(f'{org_role.mention} Denúncia anônima: {msg}')
            await user.send('Denúncia recebida Obrigado por ajudar a tornar o RPG4N um evento melhor! '
                            'Seu nome não será divulgado para a organização.')


def setup(bot):
    bot.add_cog(FeedbackCog(bot))
