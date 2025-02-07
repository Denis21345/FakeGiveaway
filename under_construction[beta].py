import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import datetime
from datetime import timedelta
load_dotenv()
TOKEN = os.getenv("token")
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=">", case_sensitive=False, intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Bot logged in")
    # Don't give anything here for changing status from Online to Idle etc, don't give a playing status in `on_ready`, making API calls in on_ready can ban your IP from discord.

now = discord.utils.utcnow()
# define an instance of timedelta with minutes set to 5
# we will use this to increase the time of the datetime.datetime instance above
five_minutes = timedelta(minutes=5)
# add the 5 minutes to the current time
time = now + five_minutes
# get the timestamp, cast it to int and assign it to a variable
timestamp = int(time.timestamp())
# construct the discord timestamp format with the timestamp
string = f"<t:{timestamp}:R>"


@bot.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx, winner: discord.Member, duration_hours, *, msg):
    await ctx.message.delete()
    UTC_now = datetime.datetime.utcnow()
    int_dur = int(float(duration_hours))  # int()
    dur_mins = int_dur*60
    dur_seconds = dur_mins*60
    giveaway_embed = discord.Embed()
    giveaway_embed.title = f"{msg}"
    giveaway_embed.description = f"""React with :tada: to enter! \n  Ends: {duration_hours} hours ({timestamp}) This giveaway started at {UTC_now.year}-{UTC_now.month}-{UTC_now.day} \t {UTC_now.hour}:{UTC_now.minute}
      """  # UTC_now.second
    await ctx.send(":tada: **GIVEAWAY** :tada:")  # Check README.md if you want to use giveaway bot's tada emoji without adding the emote in the server whewre the giveaway is going to take place

    gw_msg = await ctx.send(embed=giveaway_embed)
    await gw_msg.add_reaction("🎉")
    await asyncio.sleep(dur_seconds)
    winner_embed = discord.Embed()
    winner_embed.title = "Winner"
    winner_embed.description = f"<@{winner.id}> won **{msg}**"
    await ctx.send(f"<@{winner.id}>", delete_after=0.001)
    await ctx.send(embed=winner_embed)

# use only 'seconds' in the while using the cmd, the time will be given in hrs in embed,
# example
# >giveaway @user(the winner) 5 (5.0 hrs, duration in hours only) Nitro Classic ("msg" is the prize)


bot.run(TOKEN)
