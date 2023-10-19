import discord
from discord.ext import commands
import time
import os.path
import os
import shutil
import random
from simpledemotivators import Demotivator
import responses

config = responses.get_config()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
activity = discord.Game(name="монетку с вами даунами")

bot = commands.Bot(command_prefix='!', help_command = None, intents=intents, activity=activity, status=discord.Status.online)

@bot.event
async def on_ready():
    print(f'Logged V1 as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def help(ctx):
    embed = discord.Embed(title='Инструкция использования GoPro', description='V2 безрукий)))))')
    embed.add_field(name='!coin', value='Кидает монетку')
    embed.add_field(name='!shoot', value='Стреляет в монетку, если та в воздухе')
    embed.add_field(name='!coins', value="Показывает кол-во монеток. \nАргументы: (@user)")
    embed.add_field(name='!score', value="Показывает лучший счёт. \nАргументы: (@user)")
    embed.add_field(name='!scoreboard', value='Показывает таблицу счёта и монет.')
    embed.add_field(name='!ffmpeg', value='Шакалит видео. \nАргументы: (help) width height bitrate')
    embed.add_field(name='!stickershop', value='Показвает товары в магазине стикеров. \nАргументы: (stickername)')
    embed.add_field(name='!sticker', value="Отправляет выбранный стикер. \nАргументы: (list) stickername ")
    embed.add_field(name='!ping', value='Пинг.')
    embed.add_field(name='!clear', value="Отдаёт монеты и стикеры бомжам. \nСчёт вы платите государству")
    embed.add_field(name='!repeat', value="Повторяет любое сообщение пользователя. \n1 повтор - 100 монет.\nАргументы: число текст")
    embed.add_field(name='!news', value="Рандомная новость, спизженная с t.me/neuralmeduza")
    embed.add_field(name='!dem', value="Делает демотиватор. \nАргументы: верхняя_строка;нижняя_строка")
    await ctx.send(content=None, embed=embed)


#Coin&Shoot команды

@bot.command()
async def repeat(ctx, counter: int, *, txt):
    for i in range(counter):
        f = open(f'./coins/{str(ctx.author)}', "r");
        deposit = int(f.read())
        f.close()
        if 100 > deposit:
            await ctx.send("Казна пустеет милорд.")
            break
        balance = deposit - 100
        f = open(f'./coins/{str(ctx.author)}', "w");
        f.write(str(balance))
        f.close()
        await ctx.send(txt)

@bot.command()
async def scoreboard(ctx):
    #embed = discord.Embed(title='Scoreboard', description='Coin&Shoot')
    mess = "```Таблица счётов:"
    dir_path = r'./scores'
    for path in os.scandir(dir_path):
        if path.is_file():
            usname = str(path)[11:-2]
            f = open(f'./scores/{usname}', "r");
            #embed.add_field(name=f'{usname[:-5]}', value=f'{f.read()} ms')
            mess = mess + f'\n\n{usname}: {f.read()} мс'
            f.close()

    mess = mess + "\n\n\nМонетки:"
    dir_path = r'./coins'
    for path in os.scandir(dir_path):
        if path.is_file():
            usname = str(path)[11:-2]
            f = open(f'./coins/{usname}', "r");
            #embed.add_field(name=f'{usname[:-5]}', value=f'{f.read()}')
            mess = mess + f'\n\n{usname}: {f.read()}'
            f.close()      
    #await ctx.send(content=None, embed=embed)
    await ctx.send(mess + "```")


@bot.command()
async def stickershop(ctx, stickername=None):
    if stickername == None:
        mess = "```Стикеры:\n"
        dir_path = r'./stickers/prices'
        for path in os.scandir(dir_path):
            if path.is_file():
                stname = str(path)[11:-2]
                print(stname)
                f = open(f'./stickers/prices/{stname}', "r");
                mess = mess + f'\n{stname}: {str(f.read())} монет'
                f.close()
        await ctx.send(mess + "```")
    else:
        if os.path.isfile(f'./stickers/png/{str(stickername) + ".png"}') == False:
            await ctx.send("Неправильное имя стикера.")
        else:
            while 1 == 1:
                if os.path.isdir(f'./stickers/perms/{str(ctx.author)}') == False:
                    os.mkdir(f'./stickers/perms/{str(ctx.author)}')
                if os.path.isfile(f'./stickers/perms/{str(ctx.author)}/{str(stickername)}') == True:
                    await ctx.send("Мы не можем себе позволить себе такие траты дважды.")
                    break
                f = open(f'./coins/{str(ctx.author)}', "r");
                deposit = int(f.read())
                f.close()
                print(deposit)
                f = open(f'./stickers/prices/{str(stickername)}', "r");
                price = int(f.read())
                f.close()
                print(price)
                if price > deposit:
                    await ctx.send("Казна пустеет милорд.")
                    break
                f = open(f'./stickers/perms/{str(ctx.author)}/{str(stickername)}', "w")
                f.close()
                balance = deposit - price
                f = open(f'./coins/{str(ctx.author)}', "w");
                f.write(str(balance))
                f.close()
                await ctx.send(f'Вы купили "{stickername}" за {price}!')
                break

@bot.command()
async def sticker(ctx, st_name="list"):
    if str(st_name) == "list":
        mess = "```Ваши стикеры:\n"
        dir_path = f'./stickers/perms/{ctx.author}'
        for path in os.scandir(dir_path):
            if path.is_file():
                stname = str(path)[11:-2]
                mess = mess + f'\n{stname}'
        await ctx.send(mess + "```")
    else:
        if os.path.isfile(f'./stickers/perms/{str(ctx.author)}/{str(st_name)}') == True:
            await ctx.send(file=discord.File(f'./stickers/png/{str(st_name) + ".png"}'))
        else:
            await ctx.send("У вас нету этого стикера милорд.")

@bot.command()
async def score(ctx, user: discord.Member=None):
    if user == None:
        f = open(f'./scores/{str(ctx.author)}', "r");
        await ctx.send(f'Ваш лучший счёт: {f.read()} мс.')
        f.close()
    else:
        f = open(f'./scores/{str(user)}', "r");
        await ctx.send(f"Лучший счёт {str(user)}: {f.read()} мс.")
        f.close()

@bot.command()
async def coins(ctx, user: discord.Member=None):
    if user == None:
        f = open(f'./coins/{str(ctx.author)}', "r");
        await ctx.send(f'Ваши монетки: {f.read()}')
        f.close()
    else:
        f = open(f'./coins/{str(user)}', "r");
        await ctx.send(f"Монеты {str(user)}: {f.read()}")
        f.close()

@bot.command()
async def clear(ctx):
    await ctx.send("Спасибо за пожертвование. Все средства будут отданы в фонд Anti-Bidon Coalition.")
    os.remove(f'./scores/{str(ctx.author)}')
    os.remove(f'./coins/{str(ctx.author)}')
    shutil.rmtree(f'./stickers/perms/{ctx.author}')

@bot.command()
async def dem(ctx, *, string):
    if ctx.guild != None:
        for attachment in ctx.message.attachments:
            name = attachment.filename
            await attachment.save(name)
            if string.find(";") == -1:
                dem = Demotivator(string)
                print('dem1')
            else:
                text1 = string[:string.find(";")]
                text2 = string[string.find(";") + 1:]
                dem = Demotivator(text1, text2)
                print("dem2")
            dem.create(name)
            await ctx.send(file=discord.File('demresult.jpg'))
            os.remove("demresult.jpg")
            os.remove(name)
    else:
        await ctx.send("пшёл нахуй отсюда.")

@bot.command()
async def news(ctx):
    num = 0
    with open("neural shit.txt", "r") as f:
        ran = random.randint(0, 1000)
        for index, line in enumerate(f):
            a = line.strip()
            if index % 3 == 0:
                if num == ran:
                    print(f"Line {num}: {a}")
                    await ctx.send(a)
                num = num + 1
    f.close()



#Секретные команды

@bot.command()
async def bidonishe699228(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/bidon.mp4'))

@bot.command()
async def V3(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/ns.mp4'))

@bot.command()
async def zalupa(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/zalupa.mp4'))

@bot.command()
async def iguessthatsitguys(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/guys.gif'))

@bot.command()
async def FCKINGCTAS(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/cts.mp4'))

@bot.command()
async def meowmeowmeowmeowmeowmeowoooh(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/dillema.mp4'))
    
@bot.command()
async def timka16di1(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/timka16di1.mp4'))

@bot.command()
async def pon(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/pon.gif'))

@bot.command()
async def meow(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/meow.mp4'))

@bot.command()
async def cars(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/cars.mp4'))

@bot.command()
async def hry(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/hry.gif'))

@bot.command()
async def funy(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('./bot_media/funy.gif'))



#Служебные команды

@bot.command()
async def ping(ctx):
    print(bot.latency)
    await ctx.send(f'{round(bot.latency * 1000)} мс')
    
@bot.command(name='bot')
async def _bot(ctx):
    time.sleep(2)
    await ctx.send('[Console] V1 Initialised')

token = config['V1_token']
bot.run(token)

