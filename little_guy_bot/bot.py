import asyncio
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from little_guy_bot.pikmin import PIKMIN_TYPES
from zoneinfo import ZoneInfo
import random

TIMEZONE = ZoneInfo("America/Chicago")

load_dotenv()
TOKEN = os.getenv("BOT_SECRET")
SECRET = os.getenv("HIS_ID")
B = os.getenv('USER1')

intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content
intents.members = True  # Needed for member join/leave events

# Bot prefix and description
bot = commands.Bot(command_prefix="!", intents=intents, description="Little guy bot")

bot_data = {
    'pikmin_choosen_this_cycle': [],
    'current_pikmin_of_the_day': None,
    'general': None
}

@tasks.loop(hours=24)
async def daily_pikmin(channel):
    if len(bot_data['pikmin_choosen_this_cycle']) == 10:
        bot_data['pikmin_choosen_this_cycle'].clear()
    num = random.randint(0, 9)
    if num in bot_data['pikmin_choosen_this_cycle']:
        while num in bot_data['pikmin_choosen_this_cycle']:
            num = random.randint(0, 9)
    pikmin = PIKMIN_TYPES[num]
    if pikmin.get('owner'):
        await channel.send(content=f"Today's pikmin is {pikmin['name']} {pikmin['owner']}'s favorite", file={pikmin['image']})
    else:
        await channel.send(content=f"Today's pikmin is {pikmin['name']}", file={pikmin['image']})
    bot_data['pikmin_choosen_this_cycle'].append(num)
    bot_data['current_pikmin_of_the_day'] = pikmin


@daily_pikmin.before_loop
async def before():
    now = datetime.now(TIMEZONE)
    next_8am = now.replace(hour=8, minute=0, second=0, microsecond=0)

    if now >= next_8am:
        next_8am += timedelta(days=1)

    seconds_until = (next_8am - now).total_seconds()
    print(f"Waiting {seconds_until:.0f} seconds until next 8 AM CST/CDT.")
    await asyncio.sleep(seconds_until)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name == "general":
                bot_data['general'] = channel
                await daily_pikmin(channel)
    print(f"✅  Logged in as {bot.user} ({bot.user.id})")


@bot.command(name="daily")
async def get_daily_pikmin(ctx):
    pikmin = bot_data['current_pikmin_of_the_day']
    if pikmin.get('owner'):
        await ctx.send(content=f"Today's pikmin is {pikmin['name']} {pikmin['owner']}'s favorite", file={pikmin['image']})
    else:
        await ctx.send(content=f"Today's pikmin is {pikmin['name']}", file={pikmin['image']})


@bot.command(name="say")
async def say(ctx, *, message: str):
    await ctx.send(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Missing argument!")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ Unknown command.")
    else:
        raise error


@bot.event
async def on_message_delete(message):
    if message.author.id == SECRET:
        await message.channel.send("GRUG!! Stop deleting messages")


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.emoji == "‼️":
        reaction.message.channel.send("‼️")


@bot.event
async def on_member_ban(guild, user):
    log_channel = discord.utils.get(guild.text_channels, name="mod-logs")
    if log_channel:
        await log_channel.send(f'Damn, bro was banished to the shadow realm RIP {user.name}')


@bot.event
async def on_message(message):
    if 'lebron' or 'adam smasher' in message.lower():
        message.channel.send('THE GOAT')
    if 'protein' in message.lower():
        message.channel.send('no one wants your nasty protein hacks')
    if ('good' and 'morning' in message) and (message.author.id == B):
        message.channel.send('Goodmorning Goonbee')


@bot.event
async def on_message_edit(before, after):
    if after.author.id == SECRET:
        await after.channel.send("STICK TO YOUR WORD GRUG")


bot.run(TOKEN)
