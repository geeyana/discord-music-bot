"""
COMMANDS:
- join
- play
- queue
- clear
- remove
- resume
- pause
- loop
- ily
- ty
- slay
- disconnect
- move
"""

import discord
from discord.ext import commands
import yt_dlp
import asyncio
import random

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Client
client = commands.Bot(command_prefix="!", intents=intents)

# Loop variables
loop = False

# Defining options which configure ffmpeg to process audio and youtube-dl to download the best audio format from a video
FFMPEG_OPTIONS = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}
YDL_OPTIONS = {
    # 'cookiefile': 'cookies.txt',            # Use cookies from account to bypass bot check (hehe)
    'format': 'bestaudio',                  # Play with the best audio format
    'noplaylist': False,                    # Allow playlists to be played
    'skip_download': True,                  # No downloads
    'force_generic_extractor': False,       # Use specific extractors instead of generic
    'default_search': 'auto',               # Automatically process if search term or URL
    'source_address': '0.0.0.0',            # Bind to 0.0.0.0 (IPv4)
    'playliststart': 1,                     # Play up to 30 songs in playlist 
    'playlistend': 30
}

class music_cog(commands.Cog):
    def __init__(self, client): 
        self.client = client
        self.queue = []

    # Check to see if users are in the same voice channel as the bot if the bot is already connected
    async def is_connected(self, ctx):
        user_vc = ctx.author.voice.channel if ctx.author.voice else None
        bot_vc = ctx.voice_client.channel if ctx.voice_client else None

        if not ctx.author.voice:
            await ctx.send("( ｡ •` ⤙´• ｡)  |  You're not in a voice channel! To use my help, join a channel first.")
            return False
        elif user_vc != bot_vc and bot_vc != None:
            await ctx.send("( ｡ •`ᴖ´• ｡)  |  We must be in the same voice channel to use that command!")
            return False
        else:
            return True
        
    # List queue
    async def list_queue(self, ctx):
        
        songList = ""

        for i in range(0, len(self.queue)):
            songList += f"**❥ {i+1}**  ~  **`" + self.queue[i][1] + "`**\n"

        embed = discord.Embed(
            title="♡ ₊˚ ✧ ‿︵‿୨୧‿︵‿ :cherry_blossom: 𝐐𝐮𝐞𝐮𝐞 :cherry_blossom: ‿︵‿୨୧‿︵‿ ✧ ₊˚ ♡",
            description=f"\n{songList}",
            colour=discord.Color.from_rgb(249,206,231)
        )

        if songList != "":
            await ctx.send(embed=embed)
        else:
            await ctx.send("( • ᴖ • ｡)  |  Queue is empty.")

    # Greeting sound (on join)
    async def greet(self, ctx):
        greeting = random.choice(["sounds/hey.mp3", "sounds/yo.mp3", "sounds/ooo.mp3", "sounds/hi.mp3"])
        ctx.voice_client.play(discord.FFmpegPCMAudio(greeting))

    # Upset sound (on error)
    async def error(self, ctx):
        upset = random.choice(["sounds/upset1.mp3", "sounds/upset2.mp3", "sounds/upset3.mp3", "sounds/upset4.mp3", "sounds/upset5.mp3"])
        ctx.voice_client.play(discord.FFmpegPCMAudio(upset))

    # 
    #   JOIN COMMAND
    #
    @commands.command(
        name="join", 
        aliases=['j'], 
        help="Have Miku join your voice channel."
    )
    async def join(self, ctx):
        user_vc = ctx.author.voice.channel if ctx.author.voice else None
        bot_vc = ctx.voice_client.channel if ctx.voice_client else None

        if not user_vc:
            await ctx.send("( ｡ •` ⤙´• ｡)  |  You're not in a voice channel!")
            return
        elif user_vc != bot_vc and bot_vc is not None:
            await ctx.send("ヾ(„• ֊ •„)  |  Connecting... hi everyone!")
            await ctx.voice_client.move_to(user_vc)
        elif user_vc != bot_vc:
            await ctx.send("ヾ(„• ֊ •„)  |  Connecting... hi everyone!")
            await user_vc.connect()
        else:
            await ctx.send("(ꐦ¬_¬)  |  I'm already here!")
   
        await ctx.guild.change_voice_state(channel=user_vc, self_mute=False, self_deaf=True)

        # Greet user
        await self.greet(ctx)

    # 
    #   PLAY COMMAND
    #
    @commands.command(
        name="play", 
        aliases=['p'], 
        help="Plays a selected video from YouTube."
    )
    async def play(self, ctx, *, input):
        user_vc = ctx.author.voice.channel if ctx.author.voice else None
        bot_vc = ctx.voice_client.channel if ctx.voice_client else None

        # If client is not connected to a voice channel, send message
        if not user_vc:
            await ctx.send("( ｡ •` ⤙´• ｡)  |  You're not in a voice channel!")
            return
        
        # Wait for client to connect to a voice channel then join, or move to their channel
        elif not ctx.voice_client:
            await user_vc.connect()
            await self.greet(ctx)
            await ctx.guild.change_voice_state(channel=user_vc, self_mute=False, self_deaf=True)

        elif user_vc != bot_vc and bot_vc is not None:
            await ctx.voice_client.move_to(user_vc)
            await self.greet(ctx)
            await ctx.guild.change_voice_state(channel=user_vc, self_mute=False, self_deaf=True)

        # While processing information, make it look as if the bot is typing
        async with ctx.typing():

            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(input, download=False)

                # Playlist, search term --> add all videos for playlist or first entry for search
                if 'entries' in info:
                    
                    for entry in info['entries']:
                        url = entry['url']
                        title = entry['title']

                        self.queue.append((url, title))
                        await ctx.send(f'ദ്ദി ( ᵔ ᗜ ᵔ )  |  Added to queue: **`{title}`**')

                # Single video URL --> play video
                else:
                    
                    url = info['url']
                    title = info['title']
                    
                    self.queue.append((url, title))
                    await ctx.send(f'ദ്ദി ( ᵔ ᗜ ᵔ )  |  Added to queue: **`{title}`**')

            # If nothing is playing and no video is paused, play the next video in queue
            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():   
                await self.play_next(ctx)

    # Function to play the next video in queue
    async def play_next(self, ctx):

        try:
            # If something is in the queue, take the front of the queue and play it
            if self.queue:

                # This is for the loop command
                url, title = self.queue.pop(0)
                global currentSong
                currentSong = url, title

                # If looping, add the song back to the queue
                if loop:
                    self.queue.append((url, title))
                
                source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
                ctx.voice_client.play(source, after=lambda _: self.client.loop.create_task(self.play_next(ctx)))
                await ctx.send(f'٩(ˊᗜˋ*)و ♡  |  Now playing: **`{title}`**')
            
            # If nothing is in the queue, send a message
            elif not ctx.voice_client.is_playing():
                await ctx.send("( • ᴖ • ｡)  |  Queue is empty.")

        # Error message
        except Exception as e:
            print(f"An error occurred: `{e}`")
            await self.error(ctx)
            await ctx.send(f"｡°(°.◜ᯅ◝°)°｡  |  An error occurred: `{e}`")

    #
    #   LOOP COMMAND
    #
    @commands.command(
        name="loop", 
        aliases=["l"], 
        help="Loops/unloops the queue and current video playing."
    )
    async def loop(self, ctx):
        if not await self.is_connected(ctx): 
            return
        
        global loop
        global currentSong

        if loop:
            # Remove the last video (current song playing) from the queue because it is already being played
            if self.queue:
                self.queue.pop()
            loop = False
            await ctx.send("( ˘͈ ᵕ ˘͈♡)  |  ✖ Looping off.")

        else:
            if ctx.voice_client.is_playing():
                self.queue.append(currentSong)
            loop = True
            await ctx.send("(˶ᵔ ᵕ ᵔ˶)  |  ⟳ Looping on.")

    #
    #   SKIP COMMAND
    #
    @commands.command(
        name="skip", 
        aliases=["s"], 
        help="Skips the current video being played."
    )
    async def skip(self, ctx):
        if not await self.is_connected(ctx): 
            return
        
        if ctx.voice_client and ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            ctx.voice_client.stop()
            await ctx.send("(˵ •̀ ᴗ •́ ˵ ) ✧  |  ⏭ Skipped.")
        else:
            await self.error(ctx)
            await ctx.send("( ᗒᗣᗕ )  |  There is nothing to skip!")

    #
    #   PAUSE COMMAND
    #
    @commands.command(
        name="pause", 
        aliases=['ps'], 
        help="Pauses the current video being played."
    )
    async def pause(self, ctx):
        if not await self.is_connected(ctx): 
            return
        
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("(  •̀ ^ •́  ) ✧  |  ❚❚ Paused.")
        elif ctx.voice_client.is_paused():
            await ctx.send("(๑•̀ㅁ•́๑) ✧  |  The video is already paused!")
        else:
            await self.error(ctx)
            await ctx.send("୧(๑•̀ᗝ•́)૭  |  There is nothing to pause!")

    #
    #   RESUME COMMAND
    #
    @commands.command(
        name="resume", 
        aliases=['r'], 
        help="Resumes a paused video."
    )
    async def resume(self, ctx):
        if not await self.is_connected(ctx): 
            return
        
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("(\*˘︶˘\*)  |  ▶ Resuming.")
        elif ctx.voice_client.is_playing():
            await ctx.send("( ｡ •̀ ᴖ •́ ｡)  |  The video is already playing!")
        else:
            await self.error(ctx)
            await ctx.send("୧( `д´*)૭  |  There is nothing to resume!")

    #
    #   QUEUE COMMAND
    #
    @commands.command(
        name="queue", 
        aliases=["q"], 
        help="Displays the queue."
    )
    async def queue(self, ctx):
        if not await self.is_connected(ctx): 
            return
        
        await self.list_queue(ctx)

    #
    #   REMOVE COMMAND
    #
    @commands.command(
        name="remove", 
        aliases=['re'], 
        help="Removes a video from the queue with !remove [#]."
    )
    async def remove(self, ctx, index):
        if not await self.is_connected(ctx): 
            return

        # Check if entry is an integer and within range of the queue
        try:
            index = int(index)
        except:
            await ctx.send("(-‿-\")  |  Please enter a valid number.")
            return

        if self.queue:
            if index > len(self.queue) or index <= 0:
                await ctx.send("(╯°□°)╯  |  Number out of range!")
                return
            else:
                self.queue.pop(index-1)
                await ctx.send(f"( ´ ▽ ` )b  |  Video #{index} removed.")
                await self.list_queue(ctx)
        else:
            await ctx.send("(˶˙ᯅ˙˶)  |  There are no videos in the queue to remove!")
            

    #
    #   MOVE COMMAND
    #
    @commands.command(
        name="move", 
        aliases=['m'], 
        help="Moves a video's position in queue. Use !move [song #] [new #]."
    )
    async def move(self, ctx, old, new):
        if not await self.is_connected(ctx): 
            return

        if old is None or new is None:
            await ctx.send("(｡•́︿•̀｡)  |  You must give 2 positions. `!move [current #] [new #]`")
            return

        try:
            old = int(old)
            new = int(new)
        except:
            await ctx.send("(-‿-\")  |  Please enter a valid number.")
            return

        if self.queue:
            if old > len(self.queue) or new > len(self.queue) or new <= 0 or old <=0:
                await ctx.send("(╯°□°)╯  |  One of your numbers is out of range!")
                return
            else:
                song = self.queue.pop(old-1)
                self.queue.insert(new-1, song)
                await ctx.send(f"(˶˃ ᵕ ˂˶)  |  Video #{old} moved to position #{new}.")
                await self.list_queue(ctx)
        else:
            await ctx.send("(◞‸◟；)  |  There are no videos in the queue to move!")

    #
    #   CLEAR COMMAND
    #
    @commands.command(
        name="clear", 
        aliases=['c'], 
        help="Clears the queue."
    )
    async def clear(self, ctx):
        if not await self.is_connected(ctx): 
            return
        
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            ctx.voice_client.stop()
        if self.queue:
            self.queue = []
            await ctx.send("(  •̀ ᗜ •́  )ᕤ  |  Queue cleared.")
        else:
            await ctx.send("( ｰ̀εｰ́ )  |  There is nothing in the queue to clear!")

    #
    #   DISCONNECT COMMAND
    #
    @commands.command(
        name="disconnect", 
        aliases=['dc', 'leave'], 
        help="Disconnect Miku from the voice channel."
    )
    async def disconnect(self, ctx):      
        user_vc = ctx.author.voice.channel if ctx.author.voice else None
        bot_vc = ctx.voice_client.channel if ctx.voice_client else None

        # Check for bot connection
        if bot_vc is None:
            await ctx.send("<( •̀ᴖ•́)>  |  I'm not even connected to a channel!")
            return
        
        # Check if user is disconnecting the bot while it's with other members 
        elif (len(bot_vc.members) >= 2 and user_vc != bot_vc):
            await ctx.send("( ｡ •` ⤙´• ｡)  |  We must be in the same voice channel to use that command!")
            return
        
        if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            ctx.voice_client.stop()
        
        self.queue = []
        
        # Play disconnect message if user is in the same vc
        if (bot_vc == user_vc):
            goodbye = random.choice(["sounds/bye.mp3", "sounds/thank-you.mp3"])
            ctx.voice_client.play(discord.FFmpegPCMAudio(goodbye))

            while ctx.voice_client.is_playing():
                await asyncio.sleep(1)

        await ctx.voice_client.disconnect()
        await ctx.send("(￣▽￣)ゞ  |  Disconnecting... bye bye!")


#   BOT SPECIFIC COMMANDS (aka the fun commands) ---------------------------------------------------------------------


    #
    #   THANK YOU COMMAND
    #
    @commands.command(
        name="thanks", 
        aliases=['ty'], 
        help="Thank Miku for her service."
    )
    async def thanks(self, ctx):
        await ctx.send("(ㅅ´ ˘ `)  |  You're welcome!")
    
    #
    #   I LOVE YOU COMMAND
    #
    @commands.command(
        name="iloveyou", 
        aliases=['ily'], 
        help="Show your love to Miku."
    )
    async def ily(self, ctx):
        await ctx.send("(Ɔ ˘⌣˘)♡  |  I love you too!")

    #
    #   SLAY COMMAND
    #
    @commands.command(
        name="slay", 
        aliases=[], 
        help="Slay."
    )
    async def slay(self, ctx):
        await ctx.send("(˵ •̀ ᴗ - ˵ ) ✧  |  Periodt! ☆☆☆☆☆")

    #
    #   BRITISH COMMAND
    #
    @commands.command(
        name="brit", 
        aliases=['b'], 
        help="Hatsune Miku does not talk to British people."
    )
    async def brit(self, ctx):
        if not await self.is_connected(ctx): 
            return
        
        ctx.voice_client.play(discord.FFmpegPCMAudio("sounds/british.mp3"))

        while ctx.voice_client.is_playing():
            await asyncio.sleep(13)
        
