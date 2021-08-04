import os

import discord  # noqa: F401
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

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


@client.event
async def on_ready():
    print(">> Bot is online <<")


@client.command()
async def kktix_status(ctx):
    await ctx.message.delete()
    msg = "PyCon TW 2021 目前售票狀況為：\n" + kktix_pycontw2021_all()
    await ctx.send(msg)


client.run(TOKEN)
