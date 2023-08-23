import random
import requests
import discord
import mysql.connector
from discord.ext import commands
from bot_key import key
from bot_script import Bot

class BotGame(Bot):
    list_pictures = ["bmw_logo.webp", "astonMartin_logo.png", "mercedes_logo.jpg", "ford_logo.jpg",
                     "chevrolet_logo.png", "jaguar_logo.png"]

    dict_of_pics = {
        "bmw_logo.webp": 'bmw',
        "astonMartin_logo.png": 'aston martin',
        "mercedes_logo.jpg": "mercedes",
        "ford_logo.jpg": "ford",
        "chevrolet_logo.png": 'chevrolet',
        "jaguar_logo.png": 'jaguar'
    }



    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.random_pics = (random.choice(BotGame.list_pictures))
        self.game_status = False
        self.counter=0
        self.list_players=[]
        self.win_list=[]
        self.add_connect()
        self.add_play()
        self.add_answer()
        self.add_rules()
        self.add_teams()

    def add_connect(self):
        @self.command(name='connect')
        async def connect(ctx):
            if ctx.author.name not in self.list_players:
                self.list_players.append(ctx.author.name)
                await ctx.send("you are in the game!")
            else:
                await ctx.send("you are already in the game!")

    def add_play(self):
        @self.command(name='play')
        async def play(ctx):
            if len(self.list_players) == 0 or self.game_status == True:
                await ctx.send("the game has been started or list of players is empty")
            else:
                self.game_status = True
                self.random_pics = (random.choice(BotGame.list_pictures))
                await ctx.send("the game started")
                await ctx.send(file=discord.File(f'./Pictures/{self.random_pics}'))


    def add_answer(self):
            @self.command(name='answer')
            async def answer(ctx, *, arg):
                if self.game_status and ctx.author.name in self.list_players and arg.lower() == BotGame.dict_of_pics[self.random_pics]:
                    self.win_list.append(ctx.author.name)
                    await ctx.send("winning player: " + self.win_list[0])
                    self.game_status = False
                    self.list_players.clear()
                    self.win_list.clear()
                elif self.game_status and ctx.author.name in self.list_players and arg.lower() != BotGame.dict_of_pics[self.random_pics]:
                    await ctx.send("you picked the wrong answer try again")
                else:
                    if self.game_status == False:
                        await ctx.send("game is not started")
                    if ctx.author.name not in self.list_players:
                        await ctx.send("your not connected to the game")

    def add_rules(self):
        @self.command(name='rules')
        async def rules(ctx):
            await ctx.send("**Game Information**\n\n" \
                           "Teams: There are no teams in this game.\n\n" \
                           "Game Rules:\n" \
                           "1. Use the `>connect` command to join the game.\n" \
                           "2. Use the `>play` command to start the game.\n" \
                           "3. The bot will display a picture. You need to guess the word and use the `>answer` command to submit your answer.\n" \
                           "4. If you guess the correct word, you win the game.")

    def add_teams(self):
        @self.command(name='team')
        async def team(ctx):
            if len(self.list_players) == 0:
                await ctx.send("there is no user in the game")
            else:
                all_names = ''
                for i in self.list_players:
                    all_names += i
                await ctx.send(f'users in game: {all_names}')



bot=BotGame(command_prefix='>', self_bot=False)
bot.run(key)