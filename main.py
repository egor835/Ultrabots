import discord
from discord.ext import commands
import os
import time
import shutil
import subprocess
from chatGPT import responses

config = responses.get_config()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
activity = discord.Activity(name="ваши пиздежи модераторам", type=2)

bot = commands.Bot(command_prefix='!', help_command = None, intents=intents, activity=activity, status=discord.Status.online)

time.sleep(1)
chatGPT_proc = subprocess.Popen(['python3 chatGPT/bot.py'], shell=True)
time.sleep(1)
v1 = subprocess.Popen(['python3 v1.py'], shell=True)
time.sleep(1)
ffmpeg = subprocess.Popen(['python3 ffmpeg.py'], shell=True)
time.sleep(1)
coin = subprocess.Popen(['python3 coin.py'], shell=True)

#Role names
moder = config["moderator_role"]
pars = config["bot_management_role"]
muted = config["muted_role"]
catrole = config["catrole"]
modlogch = config["log_channel"]

@bot.command()
async def help(ctx, botname: discord.Member=None):
    if botname == bot.user:
        embed = discord.Embed(title='Инструкция использования камеры безопасности.', description='V1 сосёт бибу.')
        embed.add_field(name='!ban', value='Банит пользователя. \nАргументы: @user reason')
        embed.add_field(name='!unban', value='Разбанивает пользователя. \nАргументы: user#descriptor')
        embed.add_field(name='!mute', value='Выдаёт роль "В Муте". \nНЕ ИСПОЛЬЗОВАТЬ ВМЕСТЕ С !isolate \nАргументы: @user')
        embed.add_field(name='!unmute', value='Убирает роль "В Муте". \nАргументы: @user')
        embed.add_field(name='!kick', value='Кикает пользователя. \nАргументы: @user reason')
        embed.add_field(name='!cat', value='Выдаёт роль кота. \nАргументы: @user')
        embed.add_field(name='!reboot', value='Service command. \nАргументы: V1, ffmpeg, coin, chatGPT, all')
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
                v1.terminate()
                time.sleep(1)
                v1 = subprocess.Popen(['python3 v1.py'], shell=True)
                await ctx.send('[Console] V1 rebooted')
            case "ffmpeg":
                await channel.send(f"{ctx.author.mention} перезапустил FFMPEG")
                ffmpeg.terminate()
                time.sleep(1)
                ffmpeg = subprocess.Popen(['python3 ffmpeg.py'], shell=True)
                await ctx.send('[Console] FFMPEG rebooted')
            case "coin":
                await channel.send(f"{ctx.author.mention} перезапустил Coin")
                coin.terminate()
                time.sleep(1)
                coin = subprocess.Popen(['python3 coin.py'], shell=True)
                await ctx.send('[Console] Coin rebooted')
            case "chatGPT":
                await channel.send(f"{ctx.author.mention} перезапустил chatGPT")
                chatGPT_proc.terminate()
                time.sleep(1)
                chatGPT_proc = subprocess.Popen(['python3 chatGPT/bot.py'], shell=True)
                await ctx.send('[Console] chatGPT rebooted')
            case "all":
                await channel.send(f"{ctx.author.mention} перезапустил все модули")

                chatGPT_proc.terminate()
                coin.terminate()
                ffmpeg.terminate()
                v1.terminate()

                time.sleep(1)

                chatGPT_proc = subprocess.Popen(['python3 chatGPT/bot.py'], shell=True)
                coin = subprocess.Popen(['python3 coin.py'], shell=True)
                ffmpeg = subprocess.Popen(['python3 ffmpeg.py'], shell=True)
                v1 = subprocess.Popen(['python3 v1.py'], shell=True)

                await ctx.send('[Console] All modules rebooted')
    else:
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)

@bot.command()
async def fetch(ctx):
    if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles]:
        async for entry in ctx.guild.bans():
            f = open(f'./banned/{str(entry.user)}', "w")
            f.write(str(entry.user.id))
            f.close()
        await ctx.send("Готово.")
    else:
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)

@bot.command(pass_context = True)
async def ban(ctx, member: discord.Member=None, *, reason: str=None):
    global modlogch
    channel = bot.get_channel(modlogch)
    if member == ctx.author:
        await ctx.send("Hey guys. I guess that's it.", file=discord.File('./bot_media/guys.gif'))
        await ctx.send(f"{member} fatally shot himself under the chin during a Facebook livestream.")
        await channel.send(f"{ctx.author.mention} покончил жизнь самоубийством")
        await member.ban(reason=reason)
        f = open(f'./banned/{str(member)}', "w")
        f.write(str(member.id))
        f.close()
    else:
        if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
            if member == None:
                mess = "```Забаненые дурачки:\n"
                async for entry in ctx.guild.bans():
                    mess = mess + f'\n{entry.user}, причина: {entry.reason}'
                await ctx.send(mess + "```")
            else:
                try:
                    await member.send(f"Ты лох и был забанен по причине: {reason}")
                except:
                    time.sleep(0)
                await channel.send(f"{ctx.author.mention} забанил {member}")
                await ctx.send(f"{member} был забанен. Помянем.")
                await member.ban(reason=reason)
                f = open(f'./banned/{str(member)}', "w")
                f.write(str(member.id))
                f.close()
        else:
            await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)
            await channel.send(f"{ctx.author.mention} попытался забанить {member}")

@bot.command()
async def unban(ctx, *, member):
    global modlogch
    channel = bot.get_channel(modlogch)
    if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
        f = open(f'./banned/{member}', "r")
        id = f.read()
        f.close()
        user = await bot.fetch_user(int(id))
        await ctx.guild.unban(user)
        os.remove(f'./banned/{member}')
        await ctx.send(f'{user.mention} теперь может вернуться')
        await channel.send(f"{ctx.author.mention} разбанил {user.mention}")
        try:
            await user.send(f"Ты был разбанен. Поздравляю.")
        except:
            time.sleep(0)
    else:
        await ctx.send(file=discord.File('./bot_media/v2_fuck.png'), delete_after=1)
        await channel.send(f"{ctx.author.mention} попытался разбанить {member.mention}")

@bot.command()
async def mute(ctx, member: discord.Member):
    global modlogch
    channel = bot.get_channel(modlogch)
    if ctx.message.author.guild_permissions.administrator or pars.lower() in [y.name.lower() for y in ctx.author.roles] or moder.lower() in [y.name.lower() for y in ctx.author.roles]:
        if os.path.isdir(f'./roles/{str(member)}') == False:
            os.mkdir(f'./roles/{str(member)}')
        members_roles = member.roles

        for i in range(len(member.roles) - 1):
            f = open(f'./roles/{str(member)}/{str(members_roles[i + 1])}', "w")
            f.close()
            print(members_roles[i + 1])

        a = len(member.roles)
        while a > 1:
            await member.remove_roles(member.roles[1])
            a = len(member.roles)
        print("Роли удалены")

        role = discord.utils.get(ctx.guild.roles, name=muted)
        await member.add_roles(role)
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
        for path in os.scandir(f'./roles/{str(member)}'):
            if path.is_file():
                time.sleep(1)
                print(str(path)[11:-2])
                role = discord.utils.get(ctx.guild.roles, name=str(path)[11:-2])
                await member.add_roles(role)
        shutil.rmtree(f'./roles/{str(member)}')
        role = discord.utils.get(ctx.guild.roles, name=muted)
        await member.remove_roles(role)
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

