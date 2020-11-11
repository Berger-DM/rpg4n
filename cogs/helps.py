from discord.ext import commands


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(pass_context=True, aliases=["ajuda"])
    async def help(self, ctx, command=""):
        guild = ctx.guild
        user = ctx.author
        help_channel = guild.get_channel(703999850361913364)
        org_channel = guild.get_channel(700079115918770345)
        author_roles = [x.name for x in user.roles]
        big_perms = ["Organização", "Admin", "RPG4N Bot"]
        perm_level = [x for x in author_roles if x in big_perms]

        # INICIO DICT DE AJUDA
        help_dict = {
            "ajuda": "(ou `!help`) Chama esta mensagem de ajuda.",
            "proximoevento": "Mostra a data do próximo RPG4N.",
            "mesas": "Mostra as mesas registradas no momento da chamada.",
            "feedback": """Uso: `!feedback texto`; Envia feedback para os organizadores do evento. 
                                        Se quer fazer isso de forma anônima, utilize o `!feedback_anon` 
                                        ao invés deste comando.""",
            "feedback_anon": """Uso: `!feedback_anon texto`; Envia feedback de forma anônima para os 
                                            organizadores do evento.""",
            "denuncia": """Uso: `!denuncia texto`; Envia uma denúncia para os organizadores do evento. 
                                        Se quer fazer isso de forma anônima, utilize o `!denuncia_anon` 
                                        ao invés deste comando.""",
            "denuncia_anon": """Uso: `!denuncia_anon texto`; Envia uma denúncia de forma anônima para os 
                                            organizadores do evento.""",
            "set_next_event": """Marca o próximo evento para \'data\'. Se deixar esta informação em branco, 
                                        o próximo evento fica com data indefinida.""",
            "clear": """Apaga \'no_msg\' mensagens. Se deixar esta informação em branco, 
                                apagará 3 mensagens.""", "kick": "Uso: `!kick @membro`; Remove o membro do servidor.",
            "ban": "Uso: `!ban @membro`; Bane o membro do servidor.",
            "nova_mesa": """Uso: `!nova_mesa \"Nome da Mesa\"`; Cria a infraestrutura para uma mesa 
                                         (categoria, canal de texto, canal de áudio, e role para ela) com o nome 
                                         \"Nome da Mesa\".""",
            "apaga_mesa": """Uso: `!apaga_mesa \"Nome da Mesa\"`; Deleta a infraestrutura criada para a 
                                            mesa \"Nome da Mesa\".""",
            "limpa_mesas": "Deleta a infraestrutura de todas as mesas [FECHADAS].",
            "narra_mesa": """Uso: `!narra_mesa @membro \"Nome da Mesa\"`; Atribui membro como narrador da 
                                            mesa \"Nome da Mesa\".""",
            "libera_mesa": """Uso: `!libera_mesa @membro \"Nome da Mesa\"`; Remove membro como narrador da 
                                            mesa \"Nome da Mesa\".""",
            "aluga_bot": """Uso: `!aluga_bot \"Nome do Bot\"`; Concede permissões de escrita e fala ao Bot. 
                                        USE NO CANAL DE TEXTO DA MESA DESEJADA.""",
            "grab_games": """Uso: Selecione um arquivo para compartilhar no canal, e digite o comando na 
                                            mesma mensagem. O arquivo (se for do tipo correto) alimentará o banco de 
                                            dados do bot para que ele tenha as informações necessárias das mesas do 
                                            evento. Preferível que o criador do bot execute este comando para 
                                            garantir sucesso. """,
            "pull_and_set": """Puxa as mesas registradas no Banco de Dados e cria a infraestrutura para seu 
                                            funcionamento no evento.""",
            "rpg4n": """Lança as mesas registradas para o evento, permitindo que jogadores se 
                                inscrevam nelas. Só faça isso no momento do evento!"""
        }

        # LISTA DE COMANDOS BÁSICOS
        base_cmds = ["ajuda", "proximoevento", "mesas", "feedback", "feedback_anon", "denuncia", "denuncia_anon"]

        # LISTA DE COMANDOS DE ADMINISTRAÇÃO
        admin_cmds = ["set_next_event", "clear", "kick", "ban", "nova_mesa", "apaga_mesa", "limpa_mesas", "narra_mesa",
                      "libera_mesa", "aluga_bot", "grab_games", "pull_and_set", "rpg4n"]

        # INICIO DA LISTA DE COMANDOS
        help_start = f"{user.mention}, você pode chamar os comandos:\n"
        # COMANDO FINAL PRA USUÁRIO BASE
        help_end = ("\nSe precisar de mais ajuda, fale com a Organização, ou faça uma pergunta no "
                    f"{help_channel.mention}. ")

        # INICIO DA LISTA DE ADMINISTRAÇÃO
        help_admin = f"\nAgora, os comandos de administração, {user.mention}:\n"

        if not command:
            if not perm_level:
                msg = list()
                msg.append(help_start)
                for cmd in base_cmds:
                    msg.append(f'`!{cmd}`: {help_dict[cmd]}')
                msg.append(help_end)
                await ctx.send("\n".join(msg))
            else:
                msg = list()
                msg.append(help_start)
                for cmd in base_cmds:
                    msg.append(f'`!{cmd}`: {help_dict[cmd]}')
                await ctx.send("\n".join(msg))
                msg = list()
                msg.append(help_admin)
                for cmd in admin_cmds:
                    msg.append(f'`!{cmd}`: {help_dict[cmd]}')
                await org_channel.send("\n".join(msg))
        else:
            if not perm_level:
                if command not in base_cmds:
                    await ctx.send(f'{user.mention}, ou este comando não existe ou não está disponível para você.')
                else:
                    await ctx.send(f'`!{command}`: {help_dict[command]}')
            else:
                if command in help_dict.keys():
                    await ctx.send(f'`!{command}`: {help_dict[command]}')
                else:
                    await ctx.send(f'{user.mention}, o comando {command} não existe.')


def setup(bot):
    bot.add_cog(HelpCog(bot))
