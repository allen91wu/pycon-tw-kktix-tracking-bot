import asyncio
import datetime
import os

import discord  # noqa: F401
import requests
from bs4 import BeautifulSoup
from discord import channel  # noqa: F401
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
NOTIFY_CHANNEL_ID = os.getenv("NOTIFY_CHANNEL_ID")
target_time = str("Sunday 14:00")

client = commands.Bot(command_prefix="!")


def kktix_count(web):
    r = requests.get(web)
    soup = BeautifulSoup(r.text, "html.parser")
    ticket_count = soup.find("span", class_="info-count")
    return ticket_count.text


def kktix_pycontw2021_all():
    individual = "個人票：" + kktix_count("https://pycontw.kktix.cc/events/2021-individual")
    corporate = "企業票：" + kktix_count("https://pycontw.kktix.cc/events/2021-corporate")
    reserved = "保留票：" + kktix_count("https://pycontw.kktix.cc/events/2021-reserved")
    combined = individual + "\n" + corporate + "\n" + reserved
    return combined


@client.command()
async def kktix_status(ctx):
    await ctx.message.delete()
    msg = "PyCon TW 2021 目前售票狀況為：\n" + kktix_pycontw2021_all()
    await ctx.send(msg)


async def time_task():
    await client.wait_until_ready()
    client.channel = client.get_channel(int(NOTIFY_CHANNEL_ID))
    while not client.is_closed():
        now_time = datetime.datetime.now().strftime("%A %H:%M")
        if now_time == target_time:
            msg = "PyCon TW 2021 本週售票狀況為：\n" + kktix_pycontw2021_all()
            await client.channel.send(msg)
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(1)
            pass


@client.event
async def on_ready():
    client.loop.create_task(time_task())
    print(">> Bot is online <<")


client.run(TOKEN)
