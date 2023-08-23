import discord
from discord.ext import commands


class Bot(commands.Bot):
    intents = discord.Intents.default()
    intents.message_content = True

    def __init__(self, command_prefix,self_bot):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot, intents=Bot.intents)

