#!/usr/bin/python3
'''
@author: @paultaiton
'''
import sys
import discord
from discord.ext import commands
import argparse


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", action="store", help="Discord authentication token for bot account.")
    arguments = parser.parse_args()

    # discord_client = discord.Client()
    intents = discord.Intents.default()
    bot = commands.Bot(command_prefix='$', description='Description Text Sample Paul', intents=intents)

    discord_token = arguments.token

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))

    # @discord_client.event
    # async def on_message(message):
    #   # if message.author == discord_client.user:
    #       # return

    #   # if message.content.startswith('$hello'):
    #       # await message.channel.send('Hello!')

    @bot.command()
    async def list_games(ctx, name='list_games'):
        await ctx.send('sample blah blah')

    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello World')

    bot.run(discord_token)


if __name__ == '__main__':
    sys.exit(main())
