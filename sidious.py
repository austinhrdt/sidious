""" Darth Sidious discord bot.
https://github.com/austinhrdt/sidious
"""
import os
import asyncio
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='!')


@bot.command(pass_context=True)
async def execute(ctx, *, content):
    """ listens to text channel for !execute.
    :param: context
    :param: content - the text after the command
    """
    if content == "66" and is_admin(ctx.message.author):
        users = get_active_users(ctx.message.guild.voice_channels)
        await speak(ctx.message.author.voice.channel, "media/sixtysix.mp3")
        await disconnect_users(users)
    else:
        await ctx.message.channel.send("You have no power here.")


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
    if channel is not None:
        voice = await channel.connect()
        voice.play(discord.FFmpegPCMAudio(filename),
                   after=lambda e: print('done'))
        while voice.is_playing():
            await asyncio.sleep(1)
        await voice.disconnect()


def get_active_users(channels):
    """retrieves all active users in voice lobbies.

    :param: list of voice channel objects
    :yield: generator object of active users
    """
    for channel in channels:
        for member in channel.members:
            yield member


async def disconnect_users(members):
    """disconnects users from discord voice.

    :param: list of member objects
    """
    for member in members:
        await member.edit(voice_channel=None)


bot.run(os.getenv("DISCORD_TOKEN", ''))
