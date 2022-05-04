# pip install pynacl
# pip install youtube_dl
# pip install discord
# pip install beautifulsoup4
# pip install selenium
# ffmpeg-5.0.1-full_build.7z install & set environment variable (https://www.gyan.dev/ffmpeg/builds/)
# download webdriver(chrome)

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from selenium import webdriver
from bs4 import BeautifulSoup
from secret import *

options = webdriver.ChromeOptions()
options.headless = True

bot = commands.Bot(command_prefix="*", status=discord.Status.online, activity=discord.Game("*Help")) # 명령어 접두사 : *

bot_info = discord.Embed(title="DJU-assistant", description="명령어 목록입니다.", color=0x2cbf60)
bot_info.add_field(name="1. 인사", value="*hello --> 봇이 사용자에게 인사합니다.", inline=False)
bot_info.add_field(name="2. 음악", value="*play <youtube url> --> url에 해당하는 음악을 재생합니다."+\
                                            "\n*pause --> 재생중인 음악을 정지합니다."+\
                                            "\n*resume --> 정지했던 음악을 다시 재생합니다."+\
                                            "\n*quit --> 음악을 종료합니다."+\
                                            "\n*leave --> 봇이 통화방을 나갑니다.", inline=False)
bot_info.set_footer(text = "made by KJH, MJY, KJH, LJM, JJY")

@bot.event
async def on_ready():
    print("We have logged in as {}".format(bot.user))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=bot_info)

@bot.command(aliases=["hi", "Hi", "Hello", "안녕", "ㅎㅇ", "안녕하세요"])
async def hello(ctx):
    await ctx.send(f"{ctx.author.mention} 안녕하세요", reference=ctx.message)

@bot.command(aliases=["p", "music", "m", "음악"])
async def play(ctx, url):
    print(url)
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
                await ctx.send("음악 재생 기능은 명령자가 음성 채널에 접속해 있는 경우에만 사용 가능합니다.")
                return

    YDL_OPTIONS = {"format":"bestaudio", "noplaylist":"True"}
    FFMPEG_OPTIONS = {"before_options":"-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options":"-vn"}
    if not url.startswith("https://"):
        global entireText
        chromedriver_dir = "chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options=options)
        driver.get("https://www.youtube.com/results?search_query="+url)
        source = driver.page_source
        bs = BeautifulSoup(source, "lxml")
        entire = bs.find_all('a', {"id":"video-title"})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get("href")
        url = "https://www.youtube.com"+musicurl
        driver.quit()
    else:
        pass
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info["formats"][0]["url"]
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    await ctx.send(embed = discord.Embed(title="MUSIC INFO", description="현재 "+url+" 을(를) 재생하고 있습니다.", color=0x2cbf60))

@bot.command(aliases=["멈춰", "잠깐만", "정지", "wait", "w"])
async def pause(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed=discord.Embed(title="PAUSE", description = "음악을 일시정지 했습니다.", color=0x2cbf60))

@bot.command(aliases=["진행", "계속", "continue", "c"])
async def resume(ctx):
    try:
        vc.resume()
    except:
        await ctx.send("이어서 재생할 음악을 찾을 수 없습니다.")
    else:
        await ctx.send(embed=discord.Embed(title="RESUME", description="음악을 다시 재생했습니다.", color=0x2cbf60))

@bot.command(aliases=["꺼", "q", "quit"])
async def stop(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed=discord.Embed(title="QUIT", description="음악을 종료했습니다.", color=0x2cbf60))
    else:
        await ctx.send("종료할 음악을 찾을 수 없습니다.")

@bot.command(aliases=["l", "leave", "off", "나가", "끄기"])
async def out(ctx):
    await bot.voice_clients[0].disconnect()

bot.run(token)