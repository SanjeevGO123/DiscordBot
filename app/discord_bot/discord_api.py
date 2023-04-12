import discord
import os
from dotenv import load_dotenv
from app.chatgpt_ai.openai import chatgpt_response
from discord.ext import commands
import asyncio

load_dotenv()
discord_token = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Logged on as', client.user)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

    command,user_message=None,None

    for text in ['/ai','/bot','/chatgpt']:
        if message.content.startswith(text):
            command=message.content.split(' ')[0]
            user_message=message.content.replace(text,'')
            print(command,user_message)

    if command == '!ai' or command == '!bot' or command == '!chatgpt':
        bot_response = chatgpt_response(prompt=user_message)
        await message.channel.send(f"Answer: {bot_response}")

@client.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    server = ctx.message.guild
    voice_state = server.voice_client

    audio_source = await discord.FFmpegOpusAudio.from_probe(url)
    voice_state.play(audio_source)

@client.command()
async def ai(ctx, *args):
    user_message = " ".join(args)
    bot_response = chatgpt_response(prompt=user_message)
    await ctx.send(f"Answer: {bot_response}")

@client.command()
async def bot(ctx, *args):
    user_message = " ".join(args)
    bot_response = chatgpt_response(prompt=user_message)
    await ctx.send(f"Answer: {bot_response}")
@client.command()
async def chatgpt(ctx, *args):
    user_message = " ".join(args)
    bot_response = chatgpt_response(prompt=user_message)
    await ctx.send(f"Answer: {bot_response}")

@client.command()
async def reminder(ctx, time, *, reminder):
    # Parse the time string
    time_seconds = 0
    for unit in time.split():
        if unit[-1] == 's':
            time_seconds += int(unit[:-1])
        elif unit[-1] == 'm':
            time_seconds += int(unit[:-1]) * 60
        elif unit[-1] == 'h':
            time_seconds += int(unit[:-1]) * 60 * 60
        elif unit[-1] == 'd':
            time_seconds += int(unit[:-1]) * 60 * 60 * 24

    # Set the reminder
    await asyncio.sleep(time_seconds)
    await ctx.send(f"Reminder for {ctx.author.mention}: {reminder}")

client.run(discord_token)
