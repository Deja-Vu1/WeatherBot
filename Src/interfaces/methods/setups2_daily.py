import discord
import requests
import json

from interfaces.admin.logs import oops_log2
from interfaces.methods.current_tr_time import get

footext = "Developed by bis ❤️ "
def sets(bot,weekly):
    @bot.command()
    async def resetup(ctx,*args):
        if ctx.message.author.guild_permissions.administrator:
            name=" "
            name = name.join(args)
            if not name.islower():
                await ctx.send("en iyi kullanım için bütün karakterleri küçük yazarak giriş yapın", delete_after=5)
            else:
                guild_id = str(ctx.guild.id)
                if not guild_id in weekly.keys():
                    await ctx.send("Bu sunucuya ait kayıtlı bilgi yok",delete_after=5)
                    await ctx.message.delete()
                    
                else:
                    if not name in weekly[guild_id].keys():
                        await ctx.send("Bu şehre ait kayıtlı bilgi yok",delete_after=5)
                        await ctx.message.delete()
                    elif [ctx.message.channel.id,ctx.message.author.id] in weekly[guild_id][name]:
                        weekly[guild_id][name].remove([ctx.message.channel.id,ctx.message.author.id])
                        weekly[guild_id]["ZmxhZw=="] -= 1
                        await ctx.send("Kayıtlı bilginiz başarıyla SİLİNDİ",delete_after=5)
                        await ctx.message.delete()
                    else:
                        await ctx.send("Bu şehre ait kayıtlı bilgi yok",delete_after=5)
                        await ctx.message.delete()
                with open('hello.json', 'w') as outfile:
                        json.dump(weekly, outfile)
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
                    guild_id = str(ctx.guild.id)
                    if not guild_id in weekly.keys():
                        weekly[guild_id] = {"ZmxhZw==":1,name:[[ctx.channel.id,ctx.author.id]]}
                        await ctx.send("başarıyla oluşturuldu!")
                        await oops_log2(bot,ctx.channel,ctx.author,ctx.guild,name)
                        for_log(guild_id,ctx.message.author,ctx.message.channel.name,name)
                        
                    else:
                        if weekly[guild_id]["ZmxhZw=="] != 3:
                            if not name in weekly[guild_id].keys():
                                weekly[guild_id][name] = [[ctx.channel.id,ctx.author.id]]
                                weekly[guild_id]["ZmxhZw=="] += 1
                                await ctx.send("Başarıyla oluşturuldu")
                                for_log(guild_id,ctx.message.author,ctx.message.channel.name,name)
                            elif [ctx.message.channel.id,ctx.message.author.id] in weekly[guild_id][name]:
                                await ctx.send("Bu istek önceden gerçekleştirilmiş",delete_after=5)
                                await ctx.message.delete()
                            else:
                                weekly[guild_id][name].append([ctx.channel.id,ctx.author.id])
                                weekly[guild_id]["ZmxhZw=="] += 1
                                await ctx.send("başarıyla oluşturuldu!")
                                await oops_log2(bot,ctx.channel,ctx.author,ctx.guild,name)
                                for_log(guild_id,ctx.message.author,ctx.message.channel.name,name)
                        else:
                            now_turkey = get()
                            embed = discord.Embed(title="PREMİUM", colour=discord.Colour(0xA3FFA9))
                            embed.add_field(name="Sunucu limiti‎", value="Özel ayrıcalığa sahip olmadığınız sürece sunucu başına 3 otomatik mesaj oluşturma hakkınız olur", inline=True)
                            embed.add_field(name="‎", value="||‎|| [İLETİŞİME GEÇ !](https://deja-vu1.github.io/) | [Sunucuya ekle](https://discord.com/oauth2/authorize?client_id=829685204641513532&permissions=93184&scope=bot) | [Oy ver](https://top.gg/bot/829685204641513532)", inline=True)
                            embed.set_image(url="https://raw.githubusercontent.com/Deja-Vu1/WeatherBot/main/Img/discordimage-1.png")
                            embed.set_footer(text=footext+" bugün saat "+str(now_turkey.hour)+":"+str(now_turkey.minute),icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")
                            
                            await ctx.message.channel.send(embed=embed)

                    with open('hello.json', 'w') as outfile:
                        json.dump(weekly, outfile)
                    
                else:
                    await ctx.send("Aradığınız şehir bulunamadı!",delete_after=5)
                    await ctx.message.delete()
        else:
            await ctx.send("Bu komudu kullanmaya yetkiniz yok !")

    def for_log(gid,user,channel,name):
        trtime = get()
        print(f"[{trtime.hour}:{trtime.minute}:{trtime.second}  {get().day}/{get().month}/{get().year}] {user} created oto message protocol #{channel} city: {name} guild: {gid}")