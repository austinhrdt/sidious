""" darth sidious bot """
import os, io
from random import randint
import asyncio
from pydub import AudioSegment
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='!')  # pylint:disable=invalid-name
client = discord.Client()  # pylint:disable=invalid-name


@bot.event
async def on_ready():
    """ start up ... """
    print(bot.user.name)
    print(bot.user.id)


@bot.command(pass_context=True)
async def execute(ctx, *, content):
    """ execute [order] """
    print(ctx)
    if content == "66":
        await sixty_six(ctx)
    elif content == "65":
        await sixty_five(ctx)
    elif content == "37":
        await thirty_seven(ctx)
    elif content == "5":
        await five(ctx)
    elif content == "help":
        await ctx.message.channel.send(
            f"4 - {FOUR}\n5 - {FIVE}\n37 - {THIRTY_SEVEN}\n65 - {SIXTY_FIVE}\n66 - {SIXTY_SIX}")
    else:
        await ctx.message.channel.send(random_failure_quote())


async def sixty_six(ctx):
    """ order 66 """
    print(ctx.message.guild.voice_channels)
    print(ctx.message.guild.roles)
    if is_admin(ctx.message.author):
        await play_sound(ctx)
        for member in ctx.message.guild.members:
            try:
                if member != ctx.message.guild.me:
                    await member.edit(voice_channel=None, reason=random_success_quote())
            except: #pylint:disable=bare-except
                pass
        await ctx.message.channel.send(random_success_quote())
    else:
        await ctx.message.channel.send(random_failure_quote())


async def sixty_five(ctx):
    """ order 5 """
    print(ctx.message.guild.voice_channels)
    print(ctx.message.guild.roles)
    if is_admin(ctx.message.author):
        for member in ctx.message.guild.members:
            try:
                if member != ctx.message.guild.me and is_barb(member):
                    await member.edit(
                        voice_channel=get_voice_channel(
                            ctx, "⚓Barbossa's Chamber"),
                        reason=random_success_quote())
            except: #pylint:disable=bare-except
                pass
        await ctx.message.channel.send(random_success_quote())
    else:
        await ctx.message.channel.send(random_failure_quote())


async def thirty_seven(ctx):
    """ order 5 """
    if is_admin(ctx.message.author):
        for member in ctx.message.guild.members:
            try:
                if member not in (ctx.message.author, ctx.message.guild.me):
                    await member.edit(
                        voice_channel=get_voice_channel(
                            ctx, "💦Moist Chamber"),
                        reason=random_success_quote())
            except: #pylint:disable=bare-except
                pass
        await ctx.message.channel.send(random_success_quote())
    else:
        await ctx.message.channel.send(random_failure_quote())


async def five(ctx):
    """ order 5 """
    if is_admin(ctx.message.author):
        for member in ctx.message.guild.members:
            try:
                if member != ctx.message.guild.me and is_admin(member):
                    await member.edit(
                        voice_channel=get_voice_channel(
                            ctx, "🎩Admin Lobby"),
                        reason=random_success_quote())
            except: #pylint:disable=bare-except
                pass
        await ctx.message.channel.send(random_success_quote())
    else:
        await ctx.message.channel.send(random_failure_quote())


async def play_sound(ctx):
    """ play sound """
    user = ctx.message.author
    voice_channel = user.voice.channel
    if voice_channel is not None:
        vc = await voice_channel.connect() #pylint:disable=invalid-name
        vc.play(discord.FFmpegPCMAudio('audio.mp3'), after=lambda e: print('done'))
        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()

def get_voice_channel(ctx, name):
    """ returns voice channel """
    for channel in ctx.message.guild.voice_channels:
        if channel.name == name:
            return channel
    return None


def is_barb(member):
    """ if barbossa """
    return True if member.name == "Barbossa" else False


def is_admin(member):
    """ determines if admin """
    for role in member.roles:
        if role.name in ADMIN_ROLES:
            return True
    return False


def is_sherp(member):
    """ determines if sherp """
    for role in member.roles:
        if role.name == "Trailer Park Supervisor":
            return True
    return False


def random_success_quote():
    """ return string of random success quote """
    return SUCCESS[randint(0, len(SUCCESS) - 1)]


def random_failure_quote():
    """ return string of random failure quote """
    return FAILURE[randint(0, len(FAILURE) - 1)]


VIDEO = "https://www.youtube.com/watch?v=sNjWpZmxDgg"

ADMIN_ROLES = [
    "adminnss",
    "Shareholder",
    "Trailer Park Supervisor",
    "The OG's"]


# Trailer Park Supervisor
# ----------------------------- QUOTES -----------------------------
SUCCESS = [
    "Everything that has transpired has done so according to my design.",
    "Wipe them out. All of them.",
    "Are you threatening me, Master Jedi?",
    "The remaining Jedi will be hunted down and defeated!",
    "POWER!!! UNLIMITED... POWER!!!",
    "Do it!"
]

FAILURE = [
    "Your feeble skills are no match for the power of the dark side.",
    "You have no power here."
]

# ----------------------------- ORDERS -----------------------------
# promote fucking randys gut
FOUR = """In the event of the Supreme Commander (Chancellor) being incapacitated,
overall GAR command shall fall to the vice chair of the Senate until a successor
is appointed or alternative authority identified as outlined in Section 6
"""

# put all admins in admin lobby
FIVE = """In the event of the Supreme Commander (Chancellor) being declared unfit to issue
orders, as defined in Section 6 (ii), the Chief of the Defense Staff shall assume
GAR command and form a strategic cell of senior officers (see page 1173, para 4)
until a successor is appointed or alternative authority identified.
"""

# put everyone in a chamber
THIRTY_SEVEN = """Capture of a single wanted individual through the mass arrest and threatened
execution of a civilian population. Follow-up directives include scenarios for
body disposal of civilian casualties and suppression of communications.
"""

# put barbossa in a chamber
SIXTY_FIVE = """In the event of either (i) a majority in the Senate declaring the
Supreme Commander (Chancellor) to be unfit to issue orders, or (ii) the
Security Council declaring him or her to be unfit to issue orders, and an
authenticated order being received by the GAR, commanders shall be authorized
to detain the Supreme Commander, with lethal force if necessary, and command
of the GAR shall fall to the acting Chancellor until a successor is appointed
or alternative authority identified as outlined in Section 6.
"""

# disconnect everyone
SIXTY_SIX = """In the event of Jedi officers acting against the interests of
the Republic, and after receiving specific orders verified as coming directly
from the Supreme Commander (Chancellor), GAR commanders will remove those officers
by lethal force, and command of the GAR will revert to the Supreme Commander (Chancellor)
until a new command structure is established.
"""


bot.run(os.getenv("DISCORD_TOKEN"))
