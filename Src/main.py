import datetime
from datetime import datetime

# imports for discord api
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import CommandNotFound
from discord.ext import tasks

# extras
import asyncio
import requests
import json
import pytz
from pytz import timezone
import os

# self methods
from interfaces.admin.review_json import supervision
from interfaces.users.weather_by_city import user_interface
from interfaces.users.help_us import help_us
from interfaces.methods.daily import daily_control
from interfaces.methods.setups2_daily import sets


# check little database
f1 = open("hello.json","r")
weekly = json.load(f1)
f1.close()

dictofdays = {"Thursday":"Perşembe","Wednesday":"Çarşamba","Tuesday":"Salı","Monday":"Pazartesi","Sunday":"Pazar","Saturday":"Cumartesi","Friday":"Cuma"}
ADMINID = [596455467585110016,476010467404546052]
prefix = "-"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

sets(bot,weekly)
user_interface(bot,dictofdays)
help_us(bot)
supervision(bot,weekly)

@bot.event
async def on_ready():                                                                                      
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------');await bot.change_presence(
        activity=discord.Game(name="!weather city | 🌐 " + str(len(bot.guilds))+" servers")
        );daily_control(bot,weekly)

@bot.event
async def on_guild_join(guild):
    global ADMINID
    embed = discord.Embed(title="**NEW SERVER**", colour=discord.Colour(0x4aff00), description="\n**Members:** " + str(guild.member_count) + "\n**Banner:** [click](" + str(guild.banner_url) + ")\n**Owner:** " + str(guild.owner_id) + "\n**Server Id:** " + str(guild.id))
    embed.set_footer(text="Information Service")
    embed.set_author(name=guild, icon_url=guild.icon_url)
    embed.set_thumbnail(url=guild.icon_url)
    for i in ADMINID:
        user = await bot.fetch_user(i)
        await user.send(embed=embed)
        await bot.change_presence(
            activity=discord.Game(
                name="!weather city | 🌐 " + str(len(bot.guilds)) + " servers"))

@bot.event
async def on_guild_remove(guild):
    global ADMINID
    embed = discord.Embed(title="**LEAVED**", colour=discord.Colour(0xd0021b), description="\n**Members:** " + str(guild.member_count) + "\n**Banner:** [click](" + str(guild.banner_url) + ")\n**Owner:** " + str(guild.owner_id) + "\n**Server Id:** " + str(guild.id))

    embed.set_footer(text="Information Service")
    embed.set_author(name=guild, icon_url=guild.icon_url)
    embed.set_thumbnail(url=guild.icon_url)
    for i in ADMINID:
        user = await bot.fetch_user(i)
        await user.send(embed=embed)
        await bot.change_presence(
            activity=discord.Game(
                name="!weather city | 🌐 " + str(len(bot.guilds)) + " servers"))

bot.run("TOKEN")