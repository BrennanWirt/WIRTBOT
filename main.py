import os
import asyncio
import youtube_dl
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import urllib.request, urllib.parse, re
import pafy

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

videos = []
client = commands.Bot(command_prefix='!', case_insensitive=True)

##asyncs and defs


@client.event
async def on_ready():
    print('Hello World!')
    if os.path.isfile("song.webm"):
        os.remove("song.webm")
    videos.clear()
    await client.change_presence(activity=discord.Game('only fuckin BANGERS'))


async def duration():
    global is_playing
    is_playing = True
    await asyncio.sleep(lent)
    is_playing = False


is_playing = False


def length(url):
    global lent
    Pafy = pafy.new(url)
    lent = Pafy.length
    print(lent)


##queuelist function


async def queuelist(ctx, message, url):
    song_there = os.path.isfile("song.webm")
    if is_playing == False:
        while len(videos) > 0:
            if song_there == False:
                await yt_dl(ctx, message, url)
    if is_playing == True:
        queuemsg = videos[0], 'Added to the queue!'
        await ctx.send(queuemsg)


##download video via join voice channel, dowload via youtube-dl and play


async def yt_dl(ctx, message, url):
    channel = message.author.voice.channel
    if not channel:
        await message.send("You are not connected to a voice channel.")
        return
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': '249/250/251',
    }
    await ctx.send('Now playing ' + videos[0])
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videos[0]])
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "song.webm")
    length(videos[0])
    voice.play(discord.FFmpegOpusAudio("song.webm"))
    del videos[0]
    await duration()
    if is_playing == False:
        voice.stop()
        try:
            os.remove("song.webm")
        except:
            return


##command to summon bot and play music


@client.command()
async def play(ctx):
    message = ctx.message
    print(message.content)
    if message.content.startswith('htt' or 'www'):
        val1 = message.content
        url = val1
        await queuelist(ctx, message, url)
    else:
        search = message.content
        val1 = search.replace("!play", "")
        val2 = val1.replace(" ", "")
        search_keyword = val2
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = ("https://www.youtube.com/watch?v=" + video_ids[0])
        videos.append(url)
        await queuelist(ctx, message, url)


##client commands (skip clear and such)


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    global is_playing
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if len(videos) > 0:
        voice.stop()
        os.remove("song.webm")
        is_playing = False
        await ctx.send("Music stopped and queue cleared!")
    else:
        voice.stop()
        os.remove("song.webm")
        is_playing = False
        await ctx.send('Music stopped!')


@client.command()
async def clear(ctx):
    global is_playing
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if len(videos) > 0:
        videos.clear()
        voice.stop()
        is_playing = False
        await ctx.send("Queue cleared!")
    else:
        await ctx.send('The queue is empty!')


@client.command()
async def queue(ctx):
    if len(videos) > 0:
        await ctx.send(videos)
    else:
        await ctx.send('Theres is nothing left in the queue!')


@client.command()
async def skip(ctx):
    global is_playing
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    message = ctx.message
    os.remove("song.webm")
    if len(videos) > 0:
        url = videos[0]
        voice.stop()
        await ctx.send('Song Skipped!')
        await yt_dl(ctx, message, url)
    else:
        voice.stop()
        is_playing = False
        await ctx.send('There is nothing to skip to!')


##Use token from .ENV to start bot

client.run(TOKEN)


