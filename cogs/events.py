from discord.ext import commands
from discord.utils import get

running_tables = {}
base_role_names = ["Organização", "Narradores", "@everyone", "Admin"]
max_players = 4


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("bot is ready.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined the server!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server. Goodbye.')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        emoji = reaction.emoji
        if emoji == "\N{GAME DIE}":
            msg_channel = reaction.message.channel
            guild = reaction.message.guild
            base_roles = [x for x in guild.roles if x.name in base_role_names]
            print(msg_channel)
            category_id = msg_channel.category_id
            print(category_id)
            category_name = guild.get_channel(category_id).name
            print(category_name)
            role = get(guild.roles, name=category_name)
            if role is not None:
                if category_id not in running_tables.keys():
                    running_tables[category_id] = 0
                if running_tables[category_id] < max_players:
                    if not user.bot:
                        user_roles = user.roles
                        game_roles = [x for x in user_roles if x not in base_roles]
                        print(game_roles)
                        if game_roles:
                            await user.send(f'Olá, aqui é o RPG4N Bot, você já está inscrito na mesa {game_roles[0]} '
                                            f'deste evento.')
                            await user.send(
                                'Se quiser trocar de mesa, fale com a Organização. Obrigado por participar!')
                            await reaction.remove(user)
                        else:
                            await user.add_roles(role)
                            running_tables[category_id] += 1
                            await msg_channel.send(f'{user} se increveu para jogar na mesa!')
            if running_tables[category_id] >= max_players:
                if not category_name.startswith('[FECHADA]'):
                    category = guild.get_channel(category_id)
                    await category.edit(name="[FECHADA]  " + category_name)
                await msg_channel.send(f'Mesa {category_name} FECHADA, tendo atingido {max_players} jogadores.')
                main_channel = get(guild.channels, name="general")
                await main_channel.send(f'Mesa {category_name} FECHADA, tendo atingido {max_players} jogadores.')


def setup(bot):
    bot.add_cog(EventsCog(bot))
