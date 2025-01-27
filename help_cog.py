import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, client):
        self.client = client

    #
    #   HELP COMMAND
    #
    @commands.command(
        name="help",
        aliases=['h'],
        help="Learn what Miku can do."
    )
    async def help(self, ctx):

        embed1 = discord.Embed(
            title="♡ ₊˚ ✧ ‿︵‿୨୧‿︵‿ :cherry_blossom: 𝐍𝐨𝐭𝐞 :cherry_blossom: ‿︵‿୨୧‿︵‿ ✧ ₊˚ ♡",
            description="""
                When Miku is typing, or there is a delay before playing, she is processing your video(s).               \
                **She cannot play playlists with more than 3 songs or videos longer than one hour.**                    \n

                Queueing up multiple songs in quick succession may result in an error reading `Already playing audio.`  \
                This occurs when no songs are playing, and Miku tries to play queued songs at the same time because     \
                requests were sent in quickly. Requeue the last song before the error message.                          
            """,
            colour=discord.Color.from_rgb(238,161,205),
        )

        embed1.set_thumbnail(url="https://i.postimg.cc/1X4dPpky/help-pfp.png")

        embed2 = discord.Embed(
            colour=discord.Color.from_rgb(244,184,218)
        )

        embed2.set_image(url='https://i.postimg.cc/ZRwQ1fDf/help-divider.png')

        embed3 = discord.Embed(
            title=" ♡₊˚ ✧ ‿︵‿୨୧‿︵‿ :cherry_blossom: 𝐂𝐨𝐦𝐦𝐚𝐧𝐝𝐬 :cherry_blossom: ‿︵‿୨୧‿︵‿ ✧ ₊˚ ♡",
            colour=discord.Color.from_rgb(249,206,231)
        )

        embed3.add_field(
            name="`!join` / `!j`", 
            value="Have Miku join your voice channel."
        )
        embed3.add_field(
            name="`!disconnect` / `!dc` / `!leave`", 
            value="Disconnect Miku from the voice channel."
        )
        embed3.add_field(
            name="`!play` / `!p`", 
            value="Play a selected video from YouTube."
        )
        embed3.add_field(
            name="`!loop` / `!l`", 
            value="Loop/unloop the queue and the current video playing."
        )
        embed3.add_field(
            name="`!skip` / `!s`", 
            value="Skip the current video being played."
        )
        embed3.add_field(
            name="`!pause` / `!ps`", 
            value="Pause the current video being played."
        )
        embed3.add_field(
            name="`!resume` / `!r`", 
            value="Resume a paused video."
        )
        embed3.add_field(
            name="`!queue` / `!q`", 
            value="Display the queue."
        )
        embed3.add_field(
            name="`!remove [song #]` / `!re [#]`", 
            value="Remove a video from the queue."
        )
        embed3.add_field(
            name="`!move [song #] [new #]` / `!m [#] [#]`", 
            value="Move a video's position in queue from one place to another."
        )
        embed3.add_field(
            name="`!clear` / `!c`", 
            value="Clear the queue including the current video playing."
        )
        embed3.add_field(
            name="`!thanks` / `!ty`", 
            value="Thank Miku for her service."
        )
        embed3.add_field(
            name="`!iloveyou` / `!ily`", 
            value="Show your love to Miku."
        )
        embed3.add_field(
            name="`!slay`", 
            value="Slay."
        )
        embed3.add_field(
            name="`!help` / `!h`",
            value="See this message again."
        ) 
    
        embed3.set_image(url="https://i.postimg.cc/gj5T0xp8/help-image.png")
        embed3.set_footer(text="© 2024 [username]")
        
        await ctx.send(embed=embed1)
        await ctx.send(embed=embed2)
        await ctx.send(embed=embed3)