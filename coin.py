import time
import discord
from discord.ext import commands
import os.path
import os
from time import gmtime, strftime
import random
from chatGPT import responses

config = responses.get_config()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix='!', help_command = None, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged COIN as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def coin(ctx):
    if ctx.guild != None:
        f = open("var.txt", "w")
        f.write(str(ctx.author))
        f.close()
        run = 1
        begintime = int(strftime("%S"))
        print(begintime)
        randomint = random.randint(3, 8)
        await ctx.send(f'{str(ctx.author)[:-5]}, готов?', delete_after=randomint)
        endtime = begintime+randomint
        if endtime > 59:
            endtime = endtime - 60
        print(endtime)
        while run == 1:
            f = open("var.txt", "r")
            if f.read() == "shoot":
                f.close()
                await ctx.send(":bruh:")
                f = open("var.txt", "w")
                f.write(" ")
                f.close()
                run = 0
            if run == 1 and int(strftime("%S")) == endtime:
                f.close()
                begintime = int(strftime("%S"))
                endtime = begintime+2
                if endtime > 59:
                    endtime = endtime - 60
                print(begintime)
                print(endtime)
                print("SHOOT!")
                begintime_ns = time.time_ns()
                await ctx.send('https://cdn.discordapp.com/attachments/832604996720918574/1041934924560732190/Coin_Throw.gif', delete_after=1)
                while run == 1:
                    f = open("var.txt", "r")
                    if f.read() == "shoot":
                        endtime_ns = time.time_ns()
                        f.close()
                        await ctx.send("https://cdn.discordapp.com/attachments/832604996720918574/1041939967758319686/Coin_Shoot.gif", delete_after=2)
                        realtime_ns = endtime_ns - begintime_ns
                        realtime = round(realtime_ns / 1000000)
                        print(f"Time = {realtime}")
                        if realtime > 799:
                            realtime = realtime - 800
                        elif realtime < 800 and realtime > 399:
                            realtime = 0
                        elif realtime < 400:
                            realtime = realtime - 400
                        await ctx.send(f'Твой счёт: {realtime} мс.')
                        f = open("var.txt", "w")
                        f.write(" ")
                        f.close()
                        if os.path.isfile(f'./scores/{str(ctx.author)}') == False:
                            f = open(f'./scores/{str(ctx.author)}', "w")
                            f.write("2000")
                            f.close()
                        f = open(f'./scores/{str(ctx.author)}', "r");
                        a = f.read()
                        if int(a) > realtime:
                            f.close()
                            f = open(f'./scores/{str(ctx.author)}', "w");
                            f.write(str(realtime))
                            f.close()
                        f.close()
                        if os.path.isfile(f'./coins/{str(ctx.author)}') == False:
                            f = open(f'./coins/{str(ctx.author)}', "w")
                            f.write("0")
                            f.close()
                        f = open(f'./coins/{str(ctx.author)}', "r");
                        a = f.read()
                        f.close()
                        if realtime > 299:
                            a = int(a) + 1
                            await ctx.send("+1 монета")
                        elif realtime < 300 and realtime > -1:
                            a = int(a) + 2
                            await ctx.send("+2 монеты")
                        elif realtime < 0:
                            a = int(a) + 3
                            await ctx.send("+3 монеты")
                        f = open(f'./coins/{str(ctx.author)}', "w");
                        f.write(str(a))
                        f.close()
                        run = 0
                    if int(strftime("%S")) == endtime:
                        f.close()
                        f = open("var.txt", "w")
                        f.write(" ")
                        f.close()
                        run = 0
    else:
        await ctx.send("Эта команда отключена в личных сообщениях.")
    
@bot.command(name='bot')
async def _bot(ctx):
    time.sleep(4)
    await ctx.send('[Console] Coin Initialized')

token = config['V1_token']
bot.run(token)

