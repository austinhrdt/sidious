""" Darth Sidious discord bot.
https://github.com/austinhrdt/sidious
"""
import logging
import os
import asyncio
import discord
from discord.ext import commands

log = logging.getLogger()
if log.handlers:
    for handler in log.handlers:
        log.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    """ application entrypoint ha """
    log.info("%s total discord servers have been infected.", len(bot.guilds))
    log.info(bot.guilds)


@bot.command(pass_context=True)
async def execute(ctx, *, content):
    """ listens to text channel for !execute.

    :param: context
    :param: content - the text after the command
    """
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f"Star Wars | {len(bot.guilds)} servers infected"))
    if content and content == "66" and is_admin(ctx.message.author):
        users = get_active_users(
            ctx.message.guild.voice_channels, ctx.message.guild.me)
        # assumes main lobby is first voice channel...
        channel = ctx.message.guild.voice_channels[0]
        if ctx.message.author.voice:
            channel = ctx.message.author.voice.channel
            log.info("%s is connected to %s (voice)",
                     ctx.message.author, channel)
        if not_connected(ctx.message.guild.me) and can_connect(channel, ctx.message.guild.me):
            await speak(channel, "media/sixtysix.mp3")
            await disconnect_users(users)
        else:
            log.warning(
                "sidious is either already connected or is not permitted to connect to %s", channel)
    else:
        await ctx.message.channel.send("You have no power here.")


def not_connected(member):
    """ determines if member is already connected to voice

    :param: member object
    :return: boolean
    """
    return not bool(member.voice)


def is_admin(member):
    """ determines if member has admin rights. In this case,
    any member who can ban another is considered an admin.

    :param: member object
    :return: boolean
    """
    return member.guild_permissions.ban_members


async def speak(channel, filename):
    """ joins voice channel & plays audio file. Once audio is done playing,
    bot disconnects itself.

    :param: voice channel object
    :param: path to .mp3 file
    """
    log.info("connecting to %s", channel)
    voice = await channel.connect()
    log.info("connected, playing media")
    voice.play(discord.FFmpegPCMAudio(filename),
               after=lambda e: print('done'))
    while voice.is_playing():
        log.info("still playing...")
        await asyncio.sleep(1)
    await voice.disconnect()


def can_connect(channel, member):
    """ determines if member is permitted to connect to voice channel.

    :param: voice channel object
    :param: member object
    :return: boolean
    """
    return channel.permissions_for(member).connect


def get_active_users(channels, user):
    """retrieves all active users in voice lobbies.

    :param: list of voice channel objects
    :param: bot object
    :return: list of active users
    """
    members = []
    log.info("searching %s voice channels for active users", len(channels))
    for channel in channels:
        if can_connect(channel, user):
            log.info("collecting %s active users in %s",
                     len(channel.members), channel)
            for member in channel.members:
                members.append(member)
        else:
            log.warning("cannot connect to %s", channel)
    return members


async def disconnect_users(members):
    """disconnects users from discord voice.

    :param: list of member objects
    """
    log.info("disconnecting members: %s", members)
    for member in members:
        await member.edit(voice_channel=None)
        log.info("disconnected %s", member)


bot.run(os.getenv("DISCORD_TOKEN", ''))
