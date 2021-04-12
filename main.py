import os
import youtube_dl
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import urllib.request
import urllib.parse
import re


client = commands.Bot(command_prefix='!')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

##Bootup message

@client.event
async def on_ready():
	print('Hello World!')

##Client commands for leaving pausing etc

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
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

##Main playing fuctions		

@client.command()
async def play(ctx):
	message = ctx.message
	print(message)
	if ctx.author == client.user:
		return
		
	search = message.content
	val1 = search.replace("!play", "")
	val2= val1.replace (" ", "")
	print('THIS IS WORKING')
	##see if message is a url
	if val2.startswith("http" or "www"):
		print('THIS is WORKING 2')
		song_there = os.path.isfile("song.webm")
		url=val2
		try:
				if song_there:
						os.remove("song.webm")
		except PermissionError:
				await ctx.send("Wait for the current playing music to end or use the 'stop' command")
				return
		channel = message.author.voice.channel
		if not channel:
				await message.send("You are not connected to a voice channel")
				return
		voice = get(client.voice_clients, guild=ctx.guild)
		if voice and voice.is_connected():
				await voice.move_to(channel)
		##if not url, search input
		else:
					voice = await channel.connect()


		voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

		ydl_opts = {
				'format': '249/250/251'
				,
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([url])
		for file in os.listdir("./"):
				if file.endswith(".webm"):
						os.rename(file, "song.webm")
		voice.play(discord.FFmpegOpusAudio("song.webm"))

	else:			
			print(val2)
			search_keyword=val2
			html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
			video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
			url=("https://www.youtube.com/watch?v=" + video_ids[0])
				
			song_there = os.path.isfile("song.webm")
			try:
					if song_there:
							os.remove("song.webm")
			except PermissionError:
					await ctx.send("Wait for the current playing music to end or use the 'stop' command")
					return
			channel = message.author.voice.channel
			if not channel:
					await ctx.send("You are not connected to a voice channel")
					return
			voice = get(client.voice_clients, guild=ctx.guild)
			if voice and voice.is_connected():
					await voice.move_to(channel)
			else:
					voice = await channel.connect()


			voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

			ydl_opts = {
					'format': '249/250/251'
							
			}
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
					ydl.download([url])
			for file in os.listdir("./"):
					if file.endswith(".webm"):
							os.rename(file, "song.webm")
			voice.play(discord.FFmpegOpusAudio("song.webm"))
				


    
client.run(TOKEN)
