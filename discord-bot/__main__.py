#!/usr/bin/python3
'''
@author: @paultaiton
'''
import sys
import discord
import argparse


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", action="store", help="Discord authentication token for bot account.")
    arguments = parser.parse_args()

    discord_client = discord.Client()
    discord_token = arguments.token

    @discord_client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(discord_client))

    @discord_client.event
    async def on_message(message):
        if message.author == discord_client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    discord_client.run(discord_token)


if __name__ == '__main__':
    sys.exit(main())
