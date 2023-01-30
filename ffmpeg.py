import time
import discord
from discord.ext import commands
import os.path
import os
from chatGPT import responses

config = responses.get_config()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix='!', help_command = None, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged FFMPEG as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def ffmpeg(ctx, width="help", height="-1", ab="128000"):
    if ctx.guild != None:
        try:
            os.remove("output.mp4")
        except:
            time.sleep(0)
        if width == "help":
            embed = discord.Embed(title='FFMPEG', description='Конвертирует видео.\nПример: !ffmpeg 512 256 9600')
            embed.add_field(name='Ширина (px)', value='Обязательный аргумент. \nДолжен делиться на два.')
            embed.add_field(name='Высота (px)', value='Дополнительный аргумент. \nДефолт: -1 (сохранить пропорции). \nДолжен делиться на два.')
            embed.add_field(name='Аудио битрейт (bps)', value='Дополнительный аргумент. \nДефолт: 128000\nМинимум: 10')
            await ctx.send(content=None, embed=embed)
        else:
            for attachment in ctx.message.attachments:
                name = attachment.filename
                await attachment.save(name)
                if name == "output.mp4":
                    os.rename("output.mp4", "input.mp4")
                    name = "input.mp4"
                    print("renamed")
                if int(height) < 1:
                    height = -1
                await ctx.send("Конвертация... Пожалуйста подождите...")
                os.system(f'ffmpeg -i {name} -vf scale={width}:{height} -ab {ab} output.mp4')
                size = int(os.path.getsize("output.mp4"))
                print(size)
                if size == 0 or size > 8388608:
                    await ctx.send("Произошла ошибка. Проверьте аргументы.")
                    os.remove("output.mp4")
                    os.remove(name)
                else:
                    await ctx.send(file=discord.File('output.mp4'))
                    os.remove("output.mp4")
                    os.remove(name)
    else:
        await ctx.send("Эта команда отключена в личных сообщениях.")
    
@bot.command(name='bot')
async def _bot(ctx):
    time.sleep(6)
    await ctx.send('[Console] FFMPEG Initialized')

token = config['V1_token']
bot.run(token)

