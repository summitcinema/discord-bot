from discord.ext import commands

def limit_bot_owner():
    def predicate(ctx):
        return ctx.bot.is_owner(ctx.author)
    return commands.check(predicate)
