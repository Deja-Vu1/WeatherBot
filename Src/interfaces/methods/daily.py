import discord
from discord.ext import tasks
import json

from interfaces.methods.current_tr_time import get
from interfaces.methods.auto_message import secret
from interfaces.admin.logs import oops_log

def daily_control(bot,weekly):
    weekly = weekly
    @tasks.loop(minutes=1)
    async def daily():
        now_turkey = get()
        nowmo = int(now_turkey.month)
        nowd = int(now_turkey.day)
        nowh = int(now_turkey.hour)
        nowmi = int(now_turkey.minute)
        lastmo = weekly["aygünsaat"][0]
        lastd = weekly["aygünsaat"][1]
        lasth = weekly["aygünsaat"][2]
        lastmi = weekly["aygünsaat"][3]
        if ((nowd > lastd) or (nowd<=lastd and nowmo>lastmo)) and nowh == lasth and nowmi >= lastmi:
            for i in weekly.keys():
                if i != "aygünsaat":
                    for j in weekly[i].keys():
                        if j != "ZmxhZw==":
                            if weekly[i][j] != None or weekly[i] != []:
                                for z in weekly[i][j]:
                                    try:
                                        b = await bot.fetch_channel(z[0])
                                        d = await bot.fetch_user(z[1])
                                        url = "https://cdn.discordapp.com" +d.avatar_url._url
                                        await secret(j,b,str(d),url)
                                    except:
                                        weekly[i][j].remove([z[0],z[1]])
                                        weekly[i]["ZmxhZw=="] -= 1
                                        await oops_log(bot,z[0],z[1],j)
            weekly["aygünsaat"] = [nowmo,nowd,12,0]
            with open('hello.json', 'w') as outfile:
                json.dump(weekly, outfile)
    daily.start()