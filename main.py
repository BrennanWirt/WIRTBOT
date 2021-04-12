import os
import youtube_dl
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import urllib.request
import urllib.parse
import re

client = commands.Bot(command_prefix='!', case_insensitive=True)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

##Bootup message and change status

@client.event
async def on_ready():
    print('Hello World!')
    await client.change_presence(activity=discord.Game(name="only fucking BANGERS"))

##youtube search and download async function

async def yt_dl(ctx, message, url):
  song_there = os.path.isfile("song.webm")
  try:
      if song_there:
          os.remove("song.webm")
  except PermissionError:
        await ctx.send("There is music playing already and there is no queue (shits hard bruh)")
        return
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
  await ctx.send('Now playing '+ url)
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
  for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "song.webm")
  voice.play(discord.FFmpegOpusAudio("song.webm"))




##Client commands for leaving pausing etc


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("I am not connected to a channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("Music paused.")
    else:
        await ctx.send("No audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("Music resumed.")
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("Music stopped.")


##Main playing fuctions


@client.command()
async def play(ctx):
    message = ctx.message
    print(message)
    if ctx.author == client.user:
        return

    search = message.content
    val1 = search.replace("!play", "")
    val2 = val1.replace(" ", "")
    print('THIS IS WORKING')
    ##see if message is a url
    if val2.startswith("http" or "www"):
        url = val2
        print('THIS is WORKING 2')
        await yt_dl(ctx, message, url)

    else:
        print(val2)
        search_keyword = val2
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        url = ("https://www.youtube.com/watch?v=" + video_ids[0])
        print(url)
        await yt_dl(ctx, message, url)


client.run(TOKEN)
