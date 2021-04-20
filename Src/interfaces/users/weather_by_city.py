import discord
from datetime import datetime
from interfaces.methods.current_tr_time import get
from interfaces.methods.multi_pages import multi
import requests
import json
from discord.ext import menus



def user_interface(bot,dictofdays):
    
    @bot.command()
    async def weather(ctx,*args):

        footext = "Developed by bis ❤️ "
        name=" "
        name = name.join(args)
        
        now_turkey = get()

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
            url = "https://openweathermap.org/city/" + str(a['list'][0]['id'])
            if a["list"][0]["rain"] != None:footext+=" 🌧"
            if a["list"][0]["snow"] != None:footext+=" ❄️"

            
            embed = discord.Embed(title=name.upper(), colour=discord.Colour(0x9beec), url=url)

            embed.set_thumbnail(url=f'http://openweathermap.org/img/wn/{a["list"][0]["weather"][0]["icon"]}.png')
            embed.set_author(name=ctx.author.name, url=url, icon_url=ctx.author.avatar_url)
            embed.set_footer(text=footext+" • bugün saat "+str(now_turkey.hour)+":"+str(now_turkey.minute), icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")

            embed.add_field(name=f"🌸 Hava Durumu : **{arr}**", value=f"Açıklama : **{des}**",inline=True)
            embed.add_field(name=f"🌡️ Sıcaklık : **{round(deg, 5)}**°C", value=f"\t🔺max: **{round(dmax, 5)}**°C\n🔻min: **{round(dmin, 5)}**°C", inline=True)
            embed.add_field(name=f"Hissedilen : **{round(feel, 5)}**°C", value="‎", inline=True)
            embed.add_field(name=f"💨 Basınç : **{press}**hPa", value="‎",inline=True)
            embed.add_field(name=f"Nem : **{round(hum, 5)}**%", value="‎‎", inline=True)

            embed2 = discord.Embed(title=name.upper(), colour=discord.Colour(0x9beec), url=url) 

            embed2.set_thumbnail(url=f'http://openweathermap.org/img/wn/{a["list"][0]["weather"][0]["icon"]}.png')
            embed2.set_author(name=ctx.author.name, url=url, icon_url=ctx.author.avatar_url)
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
            
            await multi(embeds).start(ctx)
        else:
            embed = discord.Embed(title="Pardon bulamadım :/", colour=discord.Colour(0x9beec))

            embed.set_image(url="https://sinbawebtasarim.com/images/404.png")
            embed.set_author(name=ctx.author.name, url="https://discordapp.com", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=footext+"• bugün saat "+str(now_turkey.hour)+":"+str(now_turkey.minute), icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")
            await ctx.send(embed=embed,delete_after=5)
            await ctx.message.delete()