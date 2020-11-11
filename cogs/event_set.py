from discord.ext import commands

n_def = "ainda não tem data definida"
date_def = "será em "


class EventSetCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=["queromais", "proximoevento"])
    async def next_event(self, ctx):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                proxdata = await connection.fetchrow('SELECT * FROM proxevento')
                data = proxdata['proxevento']
                print(data)
                await ctx.send(f'A próxima edição do RPG4N {data}!')
                return

    @commands.command()
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    async def set_next_event(self, ctx, new_date=n_def):
        async with self.bot.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute('TRUNCATE TABLE proxevento')
                if new_date == n_def:
                    await connection.execute('INSERT INTO proxevento (proxevento) VALUES ($1)', n_def)
                    await ctx.send(f'A próxima edição do RPG4N {new_date}!')
                else:
                    data = date_def + new_date
                    await connection.execute('INSERT INTO proxevento (proxevento) VALUES ($1)', data)
                    await ctx.send(f'A próxima edição do RPG4N {data}!')
        return


def setup(bot):
    bot.add_cog(EventSetCog(bot))
