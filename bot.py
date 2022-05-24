# pip install pynacl
# pip install youtube_dl
# pip install discord
# pip install beautifulsoup4
# pip install selenium
# ffmpeg-5.0.1-full_build.7z install & set environment variable (https://www.gyan.dev/ffmpeg/builds/)
# download webdriver(chrome)
# bot invite link : https://discord.com/api/oauth2/authorize?client_id=971306432903397436&permissions=8&scope=bot

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from eng_word import get_daily_eng_words, format_words
from quote import quote_generator
from news import news_get_politics, news_get_economy, news_get_society, news_get_life_culture, news_get_IT_science, news_get_world
from secret import *

options = webdriver.ChromeOptions()
options.headless = True

bot = commands.Bot(command_prefix="*", status=discord.Status.online, activity=discord.Game("*Help")) # 명령어 접두사 : *
color_main = 0x2cbf60

bot_info = discord.Embed(title="project_BOT", description="명령어 목록입니다.", color=color_main)
bot_info.add_field(name="1. 인사", value="*hello → 봇이 사용자에게 인사합니다.", inline=False)
bot_info.add_field(name="2. 음악", value="*play <youtube url> → url에 해당하는 음악을 재생합니다."+\
                                       "\n*pause → 재생중인 음악을 정지합니다."+\
                                       "\n*resume → 정지했던 음악을 다시 재생합니다."+\
                                       "\n*quit → 음악을 종료합니다."+\
                                       "\n*leave → 봇이 통화방을 나갑니다.", inline=False)
bot_info.add_field(name="3. 공부", value="*word → 날마다 다른 영단어 5개를 보여줍니다."+\
                                       "\n*quote → 랜덤한 영어 명언을 보여줍니다.", inline=False)
bot_info.add_field(name="4. 뉴스", value="*news → 각기 다른 주제의 뉴스 6개를 보여줍니다.", inline=False)
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
async def play(ctx, *url):
    if not url:
        await ctx.send("음악 기능을 사용하기 위해서는 제목이나 링크를 함께 입력 하셔야 합니다.")
        return
    if type(url) == tuple:
        url = " ".join(url)
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
    res = requests.get(url)
    parsed = BeautifulSoup(res.text, "lxml")
    title = parsed.find("head").find("meta", {"name":"title"})['content']
    await ctx.send(embed = discord.Embed(title="MUSIC INFO", description=f"[{title}]({url})", color=color_main))

@bot.command(aliases=["멈춰", "잠깐만", "정지", "wait", "w"])
async def pause(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed=discord.Embed(title="PAUSE", description = "음악을 일시정지 했습니다.", color=color_main))

@bot.command(aliases=["진행", "계속", "continue", "c"])
async def resume(ctx):
    try:
        vc.resume()
    except:
        await ctx.send("이어서 재생할 음악을 찾을 수 없습니다.")
    else:
        await ctx.send(embed=discord.Embed(title="RESUME", description="음악을 다시 재생했습니다.", color=color_main))

@bot.command(aliases=["꺼", "q", "quit"])
async def stop(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed=discord.Embed(title="QUIT", description="음악을 종료했습니다.", color=color_main))
    else:
        await ctx.send("종료할 음악을 찾을 수 없습니다.")

@bot.command(aliases=["l", "leave", "off", "나가", "끄기"])
async def out(ctx):
    await ctx.send(embed=discord.Embed(title="LEAVE", description="음성 채널에서 퇴장하였습니다.", color=color_main))
    await bot.voice_clients[0].disconnect()

@bot.command(aliases=["영단어", "단어", "word"])
async def eng(ctx):
    daily_words = get_daily_eng_words()
    result = format_words(daily_words)
    await ctx.send(embed=discord.Embed(title="DAILY ENGLISH", description=result, color=color_main))

@bot.command(aliases=["명언", "교훈"])
async def quote(ctx):
    quote = quote_generator()
    await ctx.send(embed=discord.Embed(title="RANDOM QUOTE", description=quote, color=color_main))

@bot.command(aliases=["뉴스"])
async def news(ctx):
    politics_title, politics_link = news_get_politics()
    economy_title, economy_link = news_get_economy()
    society_title, society_link = news_get_society()
    life_culture_title, life_culture_link = news_get_life_culture()
    IT_science_title, IT_science_link = news_get_IT_science()
    world_title, world_link = news_get_world()
    headlines = discord.Embed(title="TODAY'S HEADLINES", color=color_main)
    headlines.add_field(name="POLITICS", value=f"[{politics_title}]({politics_link})", inline=False)
    headlines.add_field(name="ECONOMY", value=f"[{economy_title}]({economy_link})", inline=False)
    headlines.add_field(name="SOCIETY", value=f"[{society_title}]({society_link})", inline=False)
    headlines.add_field(name="LIFE/CULTURE", value=f"[{life_culture_title}]({life_culture_link})", inline=False)
    headlines.add_field(name="IT/SCIENCE", value=f"[{IT_science_title}]({IT_science_link})", inline=False)
    headlines.add_field(name="WORLD", value=f"[{world_title}]({world_link})", inline=False)
    await ctx.send(embed=headlines)

bot.run(token)