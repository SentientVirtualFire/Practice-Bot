import discord
from discord.ext import commands, tasks
import random as rand
import yaml


try:
    config_file = open('config.yaml')
except FileNotFoundError:
    config_file = open('example_config.yaml')
finally:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
    prefix = config['bot']['prefix']
    bot_token, dev_token = config['bot']['token'], config['bot']['dev_token']
    DEBUG = bot_token == dev_token
    bot_id = config['bot']['id']
    owner_id = config['bot']['owner_id']

async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, prefix)
    return prefix

bot = commands.Bot(command_prefix=determine_prefix,
                   description='The all-competitive-programming-purpose Discord bot!',
                   owner_id=owner_id)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        ctx.send(ctx.message.author.display_name + ' the bot is currently under scheduled maintenance. Please be patient as we try to bring it back up as soon as possible.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    if DEBUG:
        user = bot.get_user(bot.owner_id)
        await user.send('Maintenance Bot Online!')

if __name__ == '__main__':
    bot.run(bot_token)
