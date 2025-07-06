"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⡄⠀⠀⠀⠀⣇⠀⠀⠀⠀⠀⡸⢐⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢿⡙⠶⢄⣀⠀⢫⠒⢤⣀⠀⠀⢸⠰⠀⠀⣀⡤⣤⠤⠀⠀⠀
⠀⠀⠀⠀⠉⢒⠦⠄⠈⠉⠁⠠⠀⠉⠉⠙⠃⠚⠉⣠⠎⠀⠀⠀
⢀⣄⣠⡐⣈⡀⡄⠀⠀⢠⠀⢀⣴⣠⠀⠀⠀⠀⠀⠻⣀⠀⠀⠀⠀⠀
⠀⠀⢨⠟⢁⢔⡁⢀⠔⠀⠐⣡⣯⠃⢠⠀⡆⢤⠀⡀⢰⡯⡒⠠⠤⠀
⢀⣴⡵⣾⢗⣥⣶⣿⣷⣮⡼⢣⠃⢠⣧⣤⣯⣘⠀⢣⠀⣣⡏⠉⠚⠉
⠟⠁⣸⣣⡃⢿⣿⣿⣿⣿⠷⠾⢶⣿⣿⣿⣿⣿⡆⣿⡀⢿⣸⡀⠀⠀
⠀⢰⠋⠀⠀⠀⠉⠙⠉⠁⢀⣀⡀⠙⠛⠛⠛⠛⠑⡿⣯⣽⠋⣳⡆⠀
⠀⠈⠳⢦⣄⡀⠀⠀⠘⣄⣀⣀⠼⠃⠀⠀⢀⠀⠠⠴⠿⠛⠋⠁⠀⠀
⠀⠀⠀⠀⠀⠉⠉⠓⠒⠒⠤⠤⠤⠤⠔⠚⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀


MIKU MUSIC BOT VER 1

GOALS:
- multiple guild support
- interrupt and stop yt_dlp processing with a command

DEPENDENCIES:
- discord
- discord.py
- ffmpeg
- yt_dlp
"""

import discord
from discord.ext import commands
import asyncio

# Cogs
from music_cog import music_cog
from help_cog import help_cog

# Bot token
with open("token.txt", 'r') as file:
    token = file.readlines()[0]

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Client
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command("help")
    
# Check bot account and server
@client.event
async def on_ready():

    print(f"\nConnected as {client.user}")
    print(f"Connected to the following guilds:")
    for guild in client.guilds:
        print(f" - {guild.name}")
    print("\n")
    
    # Custom bot statuses
    # await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="music with friends!"))    # Normal status
    await client.change_presence(activity=discord.Game(name="Fortnite"))                                                          # Game status

    # For slash command
    await client.tree.sync()

# Start
async def main():
    print("\nRunning")
    print(client)
    try:
        await client.add_cog(music_cog(client))
        await client.add_cog(help_cog(client))
        await client.start(token)
    except Exception as e:
        print(f"｡°(°.◜ᯅ◝°)°｡  |  An error occurred: `{e}`")

# Slash command
@client.tree.command(
    name="yippee",
    description="Yahoo!"
)
async def yippee(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} Yippee!")

asyncio.run(main())
