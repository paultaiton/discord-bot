#!/usr/bin/python3
'''
@author: @paultaiton
'''
import sys
import discord
from discord.ext import commands
import argparse
import boto3
import logging

# #### VARIABLE CONFIG
# The tag and value listed here will be the filter used for listing AWS EC2 machines.
tag_filter = dict(Name='tag:discordbot', Values=['True'])


def main(args=None):
    loggin.basicConfig(level=logging.INFO)
    ec2_client = boto3.client('ec2')

    # ## debug shit
    # ec2_client.start_instances(InstanceIds=[''])
    # instances = ec2_client.describe_instances(Filters=[tag_filter])
    # for i in instances.get('Reservations', []):
    #     for j in i.get('Instances', []):
    #         print('')

    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--token", action="store", help="Discord authentication token for bot account.")
    arguments = parser.parse_args()

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
    async def list_games(ctx):
        instances = ec2_client.describe_instances(Filters=[tag_filter])
        message = "list of games:\n"
        application_set = set()
        for i in instances.get('Reservations', []):
            for j in i.get('Instances', []):
                for tag in j.get('Tags', []):
                    if tag.get('Key') == "application":
                        application_set.add(tag.get('Value'))

        await ctx.send("list of games:\n{}".format(application_set))

    @bot.command()
    async def start_game(ctx, instance_id):
        instances = ec2_client.describe_instances(Filters=[tag_filter])
        await ctx.send('Starting game {}'.format('fuck you'))

    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello World')

    bot.run(discord_token)


if __name__ == '__main__':
    sys.exit(main())
