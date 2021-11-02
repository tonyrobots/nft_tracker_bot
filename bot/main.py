import os
from typing import Collection
from discord.ext import commands
import discord
import datetime
import re
import random
from discord.permissions import Permissions
from discord.utils import get

from web3.auto.infura import w3

import logging

logging.basicConfig(level=logging.INFO)


if os.getenv("env") == "production":
    # PRODUCTION Settings
    TESTING = False


else:
    # DEV Settings
    from dotenv import load_dotenv
    load_dotenv() 
    TESTING = True


bot = commands.Bot(command_prefix="$")
TOKEN = os.getenv("DISCORD_TOKEN")
ALLOWED_CHANNELS = ["admin-test-channel", "general"]  

print (w3.isConnected())

### command listeners

# listen for !allow command
@bot.command(brief='!allow <wallet address> to add your wallet address to the appropriate allow list.', usage="<wallet>", aliases=["add"], cog_name='General')
async def allow(message, arg):
    #only allow in defined channel(s)
    if not is_allowed_channel(message, ALLOWED_CHANNELS):
        await wrong_channel_message(message, ALLOWED_CHANNELS)
        return

    if message.author == bot.user:
        return



#### helper functions

def validate_wallet(wallet = ""):
    p = re.compile("0x[a-fA-F0-9]{40}")
    # wallet = wallet.strip()
    address = p.search(wallet)
    # return EthereumAddress(wallet)
    # return /^0x[a-fA-F0-9]{40}$/
    print(f"checking wallet {wallet}, found {address}")
    if address:
        return address.string
    else:
        return False

def is_allowed_channel(message, allowed_channels):
    if allowed_channels and message.channel.name not in allowed_channels:
        return False
    else:
        return True


async def wrong_channel_message(message,allowed_channels):
    # filtered_allowed_channels = filter_channels(message, allowed_channels)
    # await message.reply("You can only do that in the following channels: " + ', '.join(filtered_allowed_channels))
    await message.reply("Sorry, you can't do that in this channel.")


# def user_is_admin(member):
#     return member.hasPermissions(manage_guild=True)

bot.run(TOKEN)
