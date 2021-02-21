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
global_tag_filter = [dict(Name='tag:discordbot', Values=['True'])]


def main(args=None):
    logging.basicConfig(level=logging.INFO)
    ec2_client = boto3.client('ec2')

    ## debug shit
    # ec2_client.start_instances(InstanceIds=[''])
    # ec2_response = ec2_client.describe_instances(Filters=global_tag_filter)
    # for i in ec2_response.get('Reservations', []):
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
        ec2_response = ec2_client.describe_instances(Filters=global_tag_filter)
        message = "list of games:\n"
        application_set = set()
        for i in ec2_response.get('Reservations', []):
            for j in i.get('Instances', []):
                for tag in j.get('Tags', []):
                    if tag.get('Key') == "application":
                        application_set.add(tag.get('Value'))

        await ctx.send("list of games:\n{}".format(application_set))

    @bot.command()
    async def list_servers(ctx, game_name=None):
        server_tag_filter = global_tag_filter
        if game_name:
            server_tag_filter.append(dict(Name='tag:application', Values=[game_name]))
        ec2_response = ec2_client.describe_instances(Filters=server_tag_filter)
        # message = "list of servers:\n"
        message = "Name : Game : State : IP : password\n"
        for reservation in ec2_response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                Tags = {x.get('Key'): x.get('Value') for x in instance.get('Tags', [])}
                if instance.get('State', {}).get('Name') != "terminated":
                    message += "{0} : {1} : {2} : {3} : {4}\n".format(Tags.get('servername'),
                                                                      Tags.get('application'),
                                                                      instance.get('State', {}).get('Name'),
                                                                      instance.get('PublicIpAddress'),
                                                                      Tags.get('password'))

        await ctx.send(message)

    @bot.command()
    async def start_server(ctx, servername=None):
        server_tag_filter = global_tag_filter
        message = "THIS IS A BUG, let Paul know."  # Message should be set by one of below cases.
        if servername:
            server_tag_filter.append(dict(Name='tag:servername', Values=[servername]))
            ec2_response = ec2_client.describe_instances(Filters=server_tag_filter)
            for reservation in ec2_response.get('Reservations', []):
                for instance in reservation.get('Instances', []):
                    if instance.get('State', {}).get('Name') == "running":
                        message = "Server {0} is already running.".format(servername)
                    elif instance.get('State', {}).get('Name') == "terminated":
                        message = "Server {0} has been destroyed, and must be rebuilt.".format(servername)
                    elif instance.get('State', {}).get('Name') == "stopping":
                        message = "Server {0} is still shutting down. Please wait for operation to complete.".format(servername)
                    elif instance.get('State', {}).get('Name') == "rebooting":
                        message = "Server {0} is still rebooting. Please wait for operation to complete.".format(servername)
                    elif instance.get('State', {}).get('Name') == "stopped":
                        ec2_client.start_instances(InstanceIds=[instance.get('InstanceId')])
                        message = "Server {0} has been started. Please wait a couple minutes and run $list_servers to check status.".format(servername)
        else:
            message = "You must pass servername as a parameter.\nExample: '$start_game chilivalheim' ."
        await ctx.send(message)

    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello World')

    bot.run(discord_token)


if __name__ == '__main__':
    sys.exit(main())
