from datetime import timedelta
import discord
from discord.ext import commands
import os
import time
import subprocess
import responses

config = responses.get_config()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
activity = discord.Activity(name="ваши пиздежи модераторам", type=2)

bot = commands.Bot(command_prefix='!', help_command = None, intents=intents, activity=activity, status=discord.Status.online)

time.sleep(1)
v1 = subprocess.Popen('exec python3 v1.py', stdout=subprocess.PIPE, shell=True)
time.sleep(1)
ffmpeg = subprocess.Popen('exec python3 ffmpeg.py', stdout=subprocess.PIPE, shell=True)
time.sleep(1)
coin = subprocess.Popen('exec python3 coin.py', stdout=subprocess.PIPE, shell=True)

#Role names
moder = config["moderator_role"]
pars = config["bot_management_role"]
catrole = config["catrole"]
modlogch = config["log_channel"]


@bot.command()
async def help(ctx):
    time.sleep(1)
    embed = discord.Embed(title='Инструкция использования камеры безопасности.', description='V1 сосёт бибу.')
    embed.add_field(name='!ban', value='Банит пользователя. \nАргументы: @user reason sec')
    embed.add_field(name='!unban', value='Разбанивает пользователя. \nАргументы: userid')
    embed.add_field(name='!mute', value='Мутит. \nАргументы: @user, reason, sec (max 28 days)')
    embed.add_field(name='!unmute', value='Убирает мут. \nАргументы: @user')
    embed.add_field(name='!kick', value='Кикает пользователя. \nАргументы: @user reason')
    embed.add_field(name='!cat', value='Выдаёт роль кота. \nАргументы: @user')
    embed.add_field(name='!reboot', value='Service command. \nАргументы: V1, ffmpeg, coin, all')
    await ctx.send(content=None, embed=embed)

@bot.event
async def on_ready():
    print(f'Logged V2 as {bot.user} (ID: {bot.user.id})')
    print('------')
                
@bot.command()
async def shoot(ctx):
    f = open("var.txt", "r")
    a = str(ctx.author)
    if a == f.read():
        f.close()
        f = open("var.txt", "w")
        f.write("shoot")
        f.close()

@bot.command()
async def reboot(ctx, process):
    if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles]:
        global modlogch
        global chatGPT_proc
        global coin
        global ffmpeg
        global v1
        channel = bot.get_channel(modlogch)
        match process:
            case "V1":
                await channel.send(f"{ctx.author.mention} перезапустил V1")
                v1.kill()
                time.sleep(1)
                v1 = subprocess.Popen('exec python3 v1.py', stdout=subprocess.PIPE, shell=True)
                await ctx.send('[Console] V1 rebooted')
            case "ffmpeg":
                await channel.send(f"{ctx.author.mention} перезапустил FFMPEG")
                ffmpeg.kill()
                time.sleep(1)
                ffmpeg = subprocess.Popen('exec python3 ffmpeg.py', stdout=subprocess.PIPE, shell=True)
                await ctx.send('[Console] FFMPEG rebooted')
            case "coin":
                await channel.send(f"{ctx.author.mention} перезапустил Coin")
                coin.kill()
                time.sleep(1)
                coin = subprocess.Popen('exec python3 coin.py', stdout=subprocess.PIPE, shell=True)
                await ctx.send('[Console] Coin rebooted')
            case "all":
                await channel.send(f"{ctx.author.mention} перезапустил все модули")

                coin.kill()
                ffmpeg.kill()
                v1.kill()

                time.sleep(1)

                coin = subprocess.Popen('exec python3 coin.py', stdout=subprocess.PIPE, shell=True)
                ffmpeg = subprocess.Popen('exec python3 ffmpeg.py', stdout=subprocess.PIPE, shell=True)
                v1 = subprocess.Popen('exec python3 v1.py', stdout=subprocess.PIPE, shell=True)

                await ctx.send('[Console] All modules rebooted')
    else:
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)

@bot.command()
async def ban(ctx, user: discord.Member=None, reason=None, sec = 0):
    global modlogch
    channel = bot.get_channel(modlogch)
    if user == None:
        mess = "```Забаненые дурачки:\n"
        n = 0
        async for entry in ctx.guild.bans():
            n += 1
            mess = mess +f'\n{n}. {str(entry.user)[:-2]}, id:{int(entry.user.id)}, причина: {entry.reason}'
        await ctx.send(mess + "```")
    elif user == ctx.author:
        await ctx.send("Hey guys. I guess that's it.", file=discord.File('./bot_media/guys.gif'))
        await ctx.send(f"{user} fatally shot himself under the chin during a Facebook livestream.")
        await channel.send(f"{ctx.author.mention} покончил жизнь самоубийством")
        await user.ban(reason=reason)
    else:
        if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
            prog = f'''
import time
import discord
from discord.ext import commands
import os.path
import os

time.sleep({sec})

server = {config['server']}
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='/', help_command = None, intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel({modlogch})
    guild = bot.get_guild(server)
    time.sleep(1)
    user = await bot.fetch_user(int({user.mention[2:-1]}))
    await guild.unban(user)
    await channel.send("{user} разбанен")
    time.sleep(1)
    os.remove("./bans/{user.mention[2:-1]}.py")
    exit()

bot.run("{config['V2_token']}")'''
            if sec == 0:
                await user.ban(reason=reason)
                await channel.send(f"{ctx.author.mention} забанил {user.mention} навсегда (длительный срок).")
            else:
                f = open(f'./bans/{user.mention[2:-1]}.py', "w")
                f.write(prog)
                f.close()
                subprocess.Popen([f'python3 ./bans/{user.mention[2:-1]}.py'], shell=True)
                await ctx.guild.ban(user, reason=reason)
                await channel.send(f"{ctx.author.mention} забанил {user.mention} на {sec} секунд")
        else:
            await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)
            await channel.send(f"{ctx.author.mention} попытался забанить {user.mention}")

@bot.command()
async def unban(ctx, member):
    global modlogch
    channel = bot.get_channel(modlogch)
    if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
        user = await bot.fetch_user(int(member))
        await ctx.guild.unban(user)
        try:
            os.remove(f'./bans/{member}.py')
        except:
            pass
        await ctx.send(f'{user.mention} теперь может вернуться')
        await channel.send(f"{ctx.author.mention} разбанил {user.mention}")
    else:
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)
        await channel.send(f"{ctx.author.mention} попытался разбанить {member}")

@bot.command()
async def mute(ctx, member: discord.Member, reason=None, sec=2419200):
    global modlogch
    channel = bot.get_channel(modlogch)
    if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
        await member.timeout(timedelta(seconds=int(sec)), reason=reason)
        await ctx.send(f'{member.mention} теперь в муте')
        await channel.send(f"{ctx.author.mention} замутил {member.mention}")
    else:
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)
        await channel.send(f"{ctx.author.mention} поытался замутить {member.mention}")

@bot.command()
async def unmute(ctx, member: discord.Member):
    global modlogch
    channel = bot.get_channel(modlogch)
    if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
        await member.timeout(None)
        await ctx.send(f'{member.mention}, голос')
        await channel.send(f"{ctx.author.mention} размутил {member.mention}")
    else:
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)
        await channel.send(f"{ctx.author.mention} попытался размутить {member.mention}")

@bot.command()
async def cat(ctx, user: discord.Member):
    global modlogch
    channel = bot.get_channel(modlogch)
    if user.name == "V1":
        await ctx.send("он не кот, он пидор")
    elif user.name == "V2":
        await ctx.send("мяу нахуй", file=discord.File('./bot_media/V2-cat.png'))
    elif ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
        role = discord.utils.get(ctx.guild.roles, name=catrole)
        await user.add_roles(role)
        await ctx.send(f'{user.mention}, мяу')
        await channel.send(f"{ctx.author.mention} сделал {user.mention} котом")
    else:
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)
        await channel.send(f"{ctx.author.mention} попытался сделать {user.mention} котом")


@bot.command(pass_context = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    global modlogch
    channel = bot.get_channel(modlogch)
    if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
        try:
            await member.send(f"Ты лох и был кикнут по причине: {reason}")
        except:
            time.sleep(0)
        await ctx.send(f"{member} ыыы по причине: {reason}.")
        await channel.send(f"{ctx.author.mention} кикнул {member}")
        await member.kick(reason=reason)
    else:
        await channel.send(f"{ctx.author.mention} попытался кикнуть {member}")
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)

@bot.command(name='bot')
async def _bot(ctx):
    await ctx.send('[Console] V2 Initialised')

token = config['V2_token']
bot.run(token)

