import discord
import datetime
from datetime import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import CommandNotFound
from discord.ext import tasks
from discord.ext import menus
import asyncio
import requests
import json
import pytz
from pytz import timezone
import os

f1 = open("hello.json","r")
weekly = json.load(f1)
f1.close()
footext = "Developed by bis ❤️ |"
dictofdays = {"Thursday":"Perşembe","Wednesday":"Çarşamba","Tuesday":"Salı","Monday":"Pazartesi","Sunday":"Pazar","Saturday":"Cumartesi","Friday":"Cuma"}
ADMINID = 596455467585110016
prefix = "!"
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

@tasks.loop(minutes=1)
async def daily():
    utc_now = datetime.utcnow()
    utc = pytz.timezone('UTC')
    aware_date = utc.localize(utc_now)
    turkey = timezone('Europe/Istanbul')
    now_turkey = aware_date.astimezone(turkey)
    nowmo = int(now_turkey.month)
    nowd = int(now_turkey.day)
    nowh = int(now_turkey.hour)
    nowmi = int(now_turkey.minute)
    lastmo = weekly["aygünsaat"][0]
    lastd = weekly["aygünsaat"][1]
    lasth = weekly["aygünsaat"][2]
    lastmi = weekly["aygünsaat"][3]
    if ((nowd > lastd) or (nowd<lastd and nowmo>lastmo)) and nowh == lasth and nowmi >= lastmi:
        for i in weekly.keys():
            if i != "aygünsaat":
                for j in weekly[i]:
                    try:
                        b = await bot.fetch_channel(j[0])
                        d = await bot.fetch_user(j[1])
                        url = "https://cdn.discordapp.com" +d.avatar_url._url
                        await secret(i,b,str(d),url)
                    except:
                        weekly[i] = weekly[i].remove([j[0],j[1]])
        weekly["aygünsaat"] = [nowmo,nowd,12,0]
        with open('hello.json', 'w') as outfile:
            json.dump(weekly, outfile)

@bot.event
async def on_ready():                                                                                      
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print('------');await bot.change_presence(
        activity=discord.Game(name="!weather city | 🌐 " + str(len(bot.guilds))+" servers")
        );daily.start()

class MultiPageEmbed(menus.ListPageSource):
    async def format_page(self, menu, entry):
        return entry

@bot.command()
async def resetup(ctx,*args):
    if ctx.message.author.guild_permissions.administrator:
        name=" "
        name = name.join(args)
        if not name.islower():
            await ctx.send("en iyi kullanım için bütün karakterleri küçük yazarak giriş yapın", delete_after=5)
        else:
            if not name in weekly.keys():
                await ctx.send("Böyle bir şehre ait kayıtlı bilgi yok")
                await ctx.message.delete()
            elif weekly[name] != None:
                for z in weekly[name]:
                    if ctx.channel.id == z[0]:
                        weekly[name] = weekly[name].remove([ctx.channel.id,z[1]])
                        await ctx.send("Kayıtlı aktiviteniz başarıyla SİLİNDİ !")
                        with open('hello.json', 'w') as outfile:
                            json.dump(weekly, outfile)
                        break
                else:
                    await ctx.send("Problem oluştu")
            else:
                await ctx.send("Problem oluştu")
    else:
        await ctx.send("Bu komudu kullanmaya yetkiniz yok !")

@bot.command()
async def setup(ctx,*args):
    if ctx.message.author.guild_permissions.administrator:
        name=" "
        name = name.join(args)
        if not name.islower():
            await ctx.send("en iyi kullanım için bütün karakterleri küçük yazarak giriş yapın", delete_after=5)
        else:
            flag = 0

            if flag ==0:

                a = requests.post(f"https://openweathermap.org/data/2.5/find?q={name}&appid=439d4b804bc8187953eb36d2a8c26a02&units=metric")
                a = json.loads(a.text)
                if a["cod"] == "200" and a["list"] != []:
                    flag = 1 

            if flag ==1:
                
                if not name in weekly.keys():
                    await ctx.send("başarıyla oluşturuldu!")
                    weekly[name] = [[ctx.channel.id,ctx.author.id]]
                elif weekly[name] != None:
                    if [ctx.channel.id,ctx.author.id] in weekly[name]:
                        await ctx.send("Zaten önceden bu istek gerçekleştirilmiş",delete_after=5)
                        await ctx.message.delete()
                    else:
                        value = weekly[name]
                        value.append([ctx.channel.id,ctx.author.id])
                        weekly[name] = value
                        await ctx.send("başarıyla oluşturuldu!")
                else:
                    weekly[name] = [[ctx.channel.id,ctx.author.id]]
                    await ctx.send("başarıyla oluşturuldu!")
                with open('hello.json', 'w') as outfile:
                    json.dump(weekly, outfile)
                
            else:
                await ctx.send("Aradığınız şehir bulunamadı!",delete_after=5)
                await ctx.message.delete()
    else:
        await ctx.send("Bu komudu kullanmaya yetkiniz yok !")

async def secret(name,channel,author_name,author_url):

    a = requests.post(f"https://openweathermap.org/data/2.5/find?q={name}&appid=439d4b804bc8187953eb36d2a8c26a02&units=metric")
    a = json.loads(a.text)
    b = requests.post(f'https://openweathermap.org/data/2.5/onecall?lat={a["list"][0]["coord"]["lat"]}&lon={a["list"][0]["coord"]["lon"]}&units=metric&appid=439d4b804bc8187953eb36d2a8c26a02')
    b = json.loads(b.text)
    des = a["list"][0]["weather"][0]["description"]
    arr = a["list"][0]["weather"][0]["main"]
    deg = a["list"][0]["main"]["temp"] - 273.15
    feel = a["list"][0]["main"]["feels_like"] - 273.15
    dmin = a["list"][0]["main"]["temp_min"] - 273.15
    dmax = a["list"][0]["main"]["temp_max"] - 273.15
    press = a["list"][0]["main"]["pressure"]
    hum = a["list"][0]["main"]["humidity"]
    if a["list"][0]["rain"] != None:footext+=" 🌧"
    if a["list"][0]["snow"] != None:footext+=" ❄️"

    utc_now = datetime.utcnow()
    utc = pytz.timezone('UTC')
    aware_date = utc.localize(utc_now)
    turkey = timezone('Europe/Istanbul')
    now_turkey = aware_date.astimezone(turkey)
    embed = discord.Embed(title=name.upper(), colour=discord.Colour(0x9beec), url="https://discordapp.com")

    embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{a["list"][0]["weather"][0]["icon"]}.png')
    embed.set_author(name=author_name, url="https://discordapp.com", icon_url=author_url)
    embed.set_footer(text="Bu mesaj BIS❤️ ailesi tarafından otomatik olarak atılmıştır•bugün saat "+str(now_turkey.hour)+":"+str(now_turkey.minute), icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")

    embed.add_field(name=f"🌸 Hava Durumu : **{arr}**", value=f"Açıklama : **{des}**",inline=True)
    embed.add_field(name=f"🌡️ Sıcaklık : **{round(deg, 5)}**°C", value=f"\t🔺max: **{round(dmax, 5)}**°C\n🔻min: **{round(dmin, 5)}**°C", inline=True)
    embed.add_field(name=f"Hissedilen : **{round(feel, 5)}**°C", value="‎", inline=True)
    embed.add_field(name=f"💨 Basınç : **{press}**hPa", value="‎",inline=True)
    embed.add_field(name=f"Nem : **{round(hum, 5)}**%", value="‎‎", inline=True)


    daily=""
    days=[]
    for i in range(1,8):
        dt = str(b["daily"][i]["dt"])
        deg = str(round(b["daily"][i]["temp"]["day"],2))
        arr = str(b["daily"][i]["weather"][0]["main"])
        press = str(b["daily"][i]["pressure"])
        hum = str(round(b["daily"][i]["humidity"],2))
        day = dictofdays[str(datetime.fromtimestamp(int(dt)).strftime("%A"))]
        days.append([day,deg,arr,press,hum])
            
    day2day = f"önümüzdeki {days[0][0]} ──► önümüzdeki {days[6][0]}"
    template = f"""{day2day}
┌─────────┐┌─────────┐
│{days[0][0].center(9, " ")}││{days[1][0].center(9, " ")}│
├─────────┤├─────────┤
│°C:{days[0][1].rjust(6, " ")}││°C:{days[1][1].rjust(6, " ")}│
│{days[0][2].center(9, " ")}││{days[1][2].center(9, " ")}│
│hPa:{days[0][3].rjust(5, " ")}││hPa:{days[1][3].rjust(5, " ")}│
│Nem:{days[0][4].rjust(5, " ")}││Nem:{days[1][4].rjust(5, " ")}│
└─────────┘└─────────┘
┌─────────┐┌─────────┐
│{days[2][0].center(9, " ")}││{days[3][0].center(9, " ")}│
├─────────┤├─────────┤
│°C:{days[2][1].rjust(6, " ")}││°C:{days[3][1].rjust(6, " ")}│
│{days[2][2].center(9, " ")}││{days[3][2].center(9, " ")}│
│hPa:{days[2][3].rjust(5, " ")}││hPa:{days[3][3].rjust(5, " ")}│
│Nem:{days[2][4].rjust(5, " ")}││Nem:{days[3][4].rjust(5, " ")}│
└─────────┘└─────────┘
┌─────────┐┌─────────┐
│{days[4][0].center(9, " ")}││{days[5][0].center(9, " ")}│
├─────────┤├─────────┤ 
│°C:{days[4][1].rjust(6, " ")}││°C:{days[5][1].rjust(6, " ")}│
│{days[4][2].center(9, " ")}││{days[5][2].center(9, " ")}│
│hPa:{days[4][3].rjust(5, " ")}││hPa:{days[5][3].rjust(5, " ")}│
│Nem:{days[4][4].rjust(5, " ")}││Nem:{days[5][4].rjust(5, " ")}│
└─────────┘└─────────┘
    ┌─────────┐
    │{days[6][0].center(9, " ")}│
    ├─────────┤
    │°C:{days[6][1].rjust(6, " ")}│
    │{days[6][2].center(9, " ")}│
    │hPa:{days[6][3].rjust(5, " ")}│
    │Nem:{days[6][4].rjust(5, " ")}│
    └─────────┘"""
    embed.add_field(name="‎‎", value=f"```{template}```",inline=False)
    ctx = await channel.send(embed=embed)






@bot.command()
async def weather(ctx,*args):
    name=" "
    name = name.join(args)
    footext = "Developed by bis ❤️ |"

    a={}
    a["list"] = []
    if len(name) != 0:
        a = requests.post(f"https://openweathermap.org/data/2.5/find?q={name}&appid=439d4b804bc8187953eb36d2a8c26a02&units=metric")
        a = json.loads(a.text)

    try:
        a["list"] = a["list"]
        a["cod"] = 200
    except:
        a["cod"] = 500

    if a["cod"] == 200 and a["list"] != []:
        b = requests.post(f'https://openweathermap.org/data/2.5/onecall?lat={a["list"][0]["coord"]["lat"]}&lon={a["list"][0]["coord"]["lon"]}&units=metric&appid=439d4b804bc8187953eb36d2a8c26a02')
        b = json.loads(b.text)
        des = a["list"][0]["weather"][0]["description"]
        arr = a["list"][0]["weather"][0]["main"]
        deg = a["list"][0]["main"]["temp"] - 273.15
        feel = a["list"][0]["main"]["feels_like"] - 273.15
        dmin = a["list"][0]["main"]["temp_min"] - 273.15
        dmax = a["list"][0]["main"]["temp_max"] - 273.15
        press = a["list"][0]["main"]["pressure"]
        hum = a["list"][0]["main"]["humidity"]
        if a["list"][0]["rain"] != None:footext+=" 🌧"
        if a["list"][0]["snow"] != None:footext+=" ❄️"

        utc_now = datetime.utcnow()
        utc = pytz.timezone('UTC')
        aware_date = utc.localize(utc_now)
        turkey = timezone('Europe/Istanbul')
        now_turkey = aware_date.astimezone(turkey)
        embed = discord.Embed(title=name.upper(), colour=discord.Colour(0x9beec), url="https://discordapp.com")

        embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{a["list"][0]["weather"][0]["icon"]}.png')
        embed.set_author(name=ctx.author.name, url="https://discordapp.com", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=footext+" • bugün saat "+str(now_turkey.hour)+":"+str(now_turkey.minute), icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")

        embed.add_field(name=f"🌸 Hava Durumu : **{arr}**", value=f"Açıklama : **{des}**",inline=True)
        embed.add_field(name=f"🌡️ Sıcaklık : **{round(deg, 5)}**°C", value=f"\t🔺max: **{round(dmax, 5)}**°C\n🔻min: **{round(dmin, 5)}**°C", inline=True)
        embed.add_field(name=f"Hissedilen : **{round(feel, 5)}**°C", value="‎", inline=True)
        embed.add_field(name=f"💨 Basınç : **{press}**hPa", value="‎",inline=True)
        embed.add_field(name=f"Nem : **{round(hum, 5)}**%", value="‎‎", inline=True)

        embed2 = discord.Embed(title=name.upper(), colour=discord.Colour(0x9beec), url="https://discordapp.com") 

        embed2.set_thumbnail(url=f'http://openweathermap.org/img/wn/{a["list"][0]["weather"][0]["icon"]}.png')
        embed2.set_author(name=ctx.author.name, url="https://discordapp.com", icon_url=ctx.author.avatar_url)
        embed2.set_footer(text=footext+" • bugün saat "+str(now_turkey.hour)+":"+str(now_turkey.minute), icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")

        daily=""
        days=[]
        for i in range(1,8):
            dt = str(b["daily"][i]["dt"])
            deg = str(round(b["daily"][i]["temp"]["day"],2))
            arr = str(b["daily"][i]["weather"][0]["main"])
            press = str(b["daily"][i]["pressure"])
            hum = str(round(b["daily"][i]["humidity"],2))
            day = dictofdays[str(datetime.fromtimestamp(int(dt)).strftime("%A"))]
            days.append([day,deg,arr,press,hum])
            
        day2day = f"önümüzdeki {days[0][0]},{days[1][0]}"
        template = f"""{day2day}
┌─────────┐┌─────────┐
│{days[0][0].center(9, " ")}││{days[1][0].center(9, " ")}│
├─────────┤├─────────┤
│°C:{days[0][1].rjust(6, " ")}││°C:{days[1][1].rjust(6, " ")}│
│{days[0][2].center(9, " ")}││{days[1][2].center(9, " ")}│
│hPa:{days[0][3].rjust(5, " ")}││hPa:{days[1][3].rjust(5, " ")}│
│Nem:{days[0][4].rjust(5, " ")}││Nem:{days[1][4].rjust(5, " ")}│
└─────────┘└─────────┘"""
        embed.add_field(name="‎‎", value=f"```{template}```",inline=False)

        day2day = f"önümüzdeki {days[2][0]} ──► önümüzdeki {days[6][0]}"
        template = f"""{day2day}
┌─────────┐┌─────────┐
│{days[2][0].center(9, " ")}││{days[3][0].center(9, " ")}│
├─────────┤├─────────┤
│°C:{days[2][1].rjust(6, " ")}││°C:{days[3][1].rjust(6, " ")}│
│{days[2][2].center(9, " ")}││{days[3][2].center(9, " ")}│
│hPa:{days[2][3].rjust(5, " ")}││hPa:{days[3][3].rjust(5, " ")}│
│Nem:{days[2][4].rjust(5, " ")}││Nem:{days[3][4].rjust(5, " ")}│
└─────────┘└─────────┘
┌─────────┐┌─────────┐
│{days[4][0].center(9, " ")}││{days[5][0].center(9, " ")}│
├─────────┤├─────────┤ 
│°C:{days[4][1].rjust(6, " ")}││°C:{days[5][1].rjust(6, " ")}│
│{days[4][2].center(9, " ")}││{days[5][2].center(9, " ")}│
│hPa:{days[4][3].rjust(5, " ")}││hPa:{days[5][3].rjust(5, " ")}│
│Nem:{days[4][4].rjust(5, " ")}││Nem:{days[5][4].rjust(5, " ")}│
└─────────┘└─────────┘
     ┌─────────┐
     │{days[6][0].center(9, " ")}│
     ├─────────┤
     │°C:{days[6][1].rjust(6, " ")}│
     │{days[6][2].center(9, " ")}│
     │hPa:{days[6][3].rjust(5, " ")}│
     │Nem:{days[6][4].rjust(5, " ")}│
     └─────────┘"""
        embed2.add_field(name="‎‎", value=f"```{template}```",inline=False)

        embeds = [embed,embed2]
        menu = menus.MenuPages(MultiPageEmbed(embeds, per_page=1))
        await menu.start(ctx)
    else:
        embed = discord.Embed(title="Pardon bulamadım :/", colour=discord.Colour(0x9beec), timestamp=datetime.utcfromtimestamp(1617872085))

        embed.set_image(url="https://sinbawebtasarim.com/images/404.png")
        embed.set_author(name=ctx.author.name, url="https://discordapp.com", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=footext, icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")
        await ctx.send(embed=embed,delete_after=5)
        await ctx.message.delete()

@bot.event
async def on_guild_join(guild):
    global ADMINID
    embed = discord.Embed(title="**NEW SERVER**", colour=discord.Colour(0x4aff00), description="\n**Members:** " + str(guild.member_count) + "\n**Banner:** [click](" + str(guild.banner_url) + ")\n**Owner:** " + str(guild.owner_id) + "\n**Server Id:** " + str(guild.id))
    embed.set_footer(text="Information Service")
    embed.set_author(name=guild, icon_url=guild.icon_url)
    embed.set_thumbnail(url=guild.icon_url)
    user = await bot.fetch_user(ADMINID)
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
    user = await bot.fetch_user(ADMINID)
    await user.send(embed=embed)
    await bot.change_presence(
        activity=discord.Game(
            name="!weather city | 🌐 " + str(len(bot.guilds)) + " servers"))
@bot.command(aliases=['yardim','yardım'])
async def help(ctx):
    utc_now = datetime.utcnow()
    utc = pytz.timezone('UTC')
    aware_date = utc.localize(utc_now)
    turkey = timezone('Europe/Istanbul')
    now_turkey = aware_date.astimezone(turkey)
    embed = discord.Embed(title="YARDIM", colour=discord.Colour(0xA3FFA9))
    embed.add_field(name="<:map:832150636228247553>", value="**!weather** ``<şehir>``\nAtlasta bulabildiğim kadar şehrin hava durumunu getirebilirim\n||öyle, değil mi?||", inline=True)
    embed.add_field(name="<:screwdriver:832150872221548564>", value="**!setup** ``<şehir>``\nYazdığınız kanala her gün hava durumu raporu gönderebilirim", inline=True)
    embed.add_field(name="<:track_previous:832152345399525377>", value="**!resetup** ``<şehir>``\nYazdığınız kanala her gün gönderdiğim hava durumu raporunu kaldırabilirim", inline=True)
    embed.add_field(name="‎", value="||‎|| [Sunucuya ekle](https://discord.com/oauth2/authorize?client_id=829685204641513532&permissions=93184&scope=bot) | [Oy ver](https://top.gg/bot/829685204641513532)", inline=True)
    embed.set_image(url="https://raw.githubusercontent.com/Deja-Vu1/WeatherBot/main/Img/discordimage-1.png")
    embed.set_footer(text=footext+" bugün saat "+str(now_turkey.hour)+":"+str(now_turkey.minute),icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")
    
    await ctx.message.channel.send(embed=embed)

bot.run(os.getenv("TOKEN"))