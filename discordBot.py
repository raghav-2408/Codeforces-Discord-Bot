import discord
import requests
import datetime
from discord.ext import commands

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

codeforces_api_url = "https://codeforces.com/api/contest.list"
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!batao'):
        contests = get_upcoming_contests()
        if contests:
            await message.channel.send("Reminder:")
            await message.channel.send("Upcoming contests:")
            for contest in contests:
                start_time = contest['startTimeSeconds']
                time_diff = start_time - datetime.datetime.now().timestamp()
                hours = int(time_diff // 3600)
                minutes = int((time_diff % 3600) // 60)
                if hours > 0:
                    time_until_start = f"{hours} hours and {minutes} minutes"
                else:
                    time_until_start = f"{minutes} minutes"
                await message.channel.send(f"**{contest['name']}** is going to start in the next **{time_until_start}**")
            
        else:
            await message.channel.send("No upcoming contests.")

def get_upcoming_contests():
    response = requests.get(codeforces_api_url)
    if response.status_code == 200:
        contests = response.json()['result']
        upcoming_contests = [contest for contest in contests if contest['phase'] == 'BEFORE']
        return upcoming_contests[:5]  # Return first 5 upcoming contests
    else:
        return None

client.run('add your BOT token from BOT section (khud se generate kro)')
