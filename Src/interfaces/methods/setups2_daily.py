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
            flag2=0
            name = name.join(args)
            if not name.islower():
                await ctx.send("en iyi kullanım için bütün karakterleri küçük yazarak giriş yapın", delete_after=5)
            else:
                guild_id = str(ctx.guild.id)
                if not guild_id in weekly.keys():
                    await refailed(ctx)
                    await ctx.message.delete()
                    
                else:
                    if name in weekly[guild_id].keys():
                        for i in weekly[guild_id][name]:
                            if i[0] == ctx.message.channel.id:
                                flag2=1
                                author = i[1]
                    if not name in weekly[guild_id].keys():
                        await refailed(ctx)
                        await ctx.message.delete()
                    elif flag2==1:
                        weekly[guild_id][name].remove([ctx.message.channel.id,author])
                        weekly[guild_id]["ZmxhZw=="] -= 1
                        await recompleted(ctx,author)
                        await ctx.message.delete()
                    else:
                        await refailed(ctx)
                        await ctx.message.delete()
                with open('hello.json', 'w') as outfile:
                        json.dump(weekly, outfile)
        else:
            await ctx.send("Bu komudu kullanmaya yetkiniz yok !")

    @bot.command()
    async def setup(ctx,*args):
        if ctx.message.author.guild_permissions.administrator:
            author = ""
            name=" "
            name = name.join(args)
            if not name.islower():
                await ctx.send("en iyi kullanım için bütün karakterleri küçük yazarak giriş yapın", delete_after=5)
            else:
                flag = 0
                flag2 = 0
                if flag ==0:

                    a = requests.post(f"https://openweathermap.org/data/2.5/find?q={name}&appid=439d4b804bc8187953eb36d2a8c26a02&units=metric")
                    a = json.loads(a.text)
                    if a["cod"] == "200" and a["list"] != []:
                        flag = 1 

                if flag ==1:
                    guild_id = str(ctx.guild.id)
                    if not guild_id in weekly.keys():
                        weekly[guild_id] = {"ZmxhZw==":1,name:[[ctx.channel.id,ctx.author.id]]}
                        await completed(ctx)
                        await oops_log2(bot,ctx.channel,ctx.author,ctx.guild,name)
                        for_log(guild_id,ctx.message.author,ctx.message.channel.name,name)
                        
                    else:
                        if weekly[guild_id]["ZmxhZw=="] != 3:
                            for i in weekly[guild_id][name]:
                                if i[0] == ctx.message.channel.id:
                                    flag2=1
                                    author = i[1]
                            if not name in weekly[guild_id].keys():
                                weekly[guild_id][name] = [[ctx.channel.id,ctx.author.id]]
                                weekly[guild_id]["ZmxhZw=="] += 1
                                await completed(ctx)
                                for_log(guild_id,ctx.message.author,ctx.message.channel.name,name)

                            elif flag2 == 1:
                                await failed(ctx,author)
                                await ctx.message.delete()
                            else:
                                weekly[guild_id][name].append([ctx.channel.id,ctx.author.id])
                                weekly[guild_id]["ZmxhZw=="] += 1
                                await completed(ctx)
                                await oops_log2(bot,ctx.channel,ctx.author,ctx.guild,name)
                                for_log(guild_id,ctx.message.author,ctx.message.channel.name,name)
                        else:
                            now_turkey = get()
                            if len(str(now_turkey.minute)) == 1:
                                minute = "0"+ str(now_turkey.minute)
                            else:
                                minute = now_turkey.minute
                            embed = discord.Embed(title="PREMİUM", colour=discord.Colour(0xA3FFA9))
                            embed.add_field(name="Sunucu limiti‎", value="Özel ayrıcalığa sahip olmadığınız sürece sunucu başına 3 otomatik mesaj oluşturma hakkınız olur", inline=True)
                            embed.add_field(name="‎", value="||‎|| [İLETİŞİME GEÇ !](https://deja-vu1.github.io/) | [Sunucuya ekle](https://discord.com/oauth2/authorize?client_id=829685204641513532&permissions=93184&scope=bot) | [Oy ver](https://top.gg/bot/829685204641513532)", inline=True)
                            embed.set_image(url="https://raw.githubusercontent.com/Deja-Vu1/WeatherBot/main/Img/discordimage-1.png")
                            embed.set_footer(text=footext+" bugün saat "+str(now_turkey.hour)+":"+str(minute),icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")
                            
                            await ctx.message.channel.send(embed=embed)

                    with open('hello.json', 'w') as outfile:
                        json.dump(weekly, outfile)
                    
                else:
                    await ctx.send("Aradığınız şehir bulunamadı!",delete_after=5)
                    await ctx.message.delete()
        else:
            await ctx.send("Bu komudu kullanmaya yetkiniz yok !")


    async def failed(ctx,author):
        embed = discord.Embed(title="Bu istek öneceden gerçekleştirilmiş", colour=discord.Colour(0x72130f), description="Eğer bu işte bir hata olduğunu düşünüyorsanız [server](https://discord.com/invite/2wknBWEQWS)'ımızdaki developerlarımızla iletişime geçebilirsiniz")

        embed.set_thumbnail(url="https://www.zambo.in/assets/quize/wrongs.gif")
        embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        try:
            b = ctx.message.channel
            d = await bot.fetch_user(author)
            embed.add_field(name=":pencil2:", value=d, inline=True)
            embed.add_field(name=":mega:", value=b, inline=True)
        except:
            pass
        
        await ctx.send(embed=embed)

    async def completed(ctx):
        embed = discord.Embed(title="Başarıyla Oluşturuldu", colour=discord.Colour(0x68ad5c), description="Eğer bu işte bir hata olduğunu düşünüyorsanız [server](https://discord.com/invite/2wknBWEQWS)'ımızdaki developerlarımızla iletişime geçebilirsiniz")

        embed.set_thumbnail(url="https://www.buyhosting.xyz/frankyvision/images/done.gif")
        embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        b = ctx.message.channel
        d = ctx.message.author
        embed.add_field(name=":pencil2:", value=d, inline=True)
        embed.add_field(name=":mega:", value=b, inline=True)
     
        await ctx.send(embed=embed)
    
    async def recompleted(ctx,author):
        embed = discord.Embed(title="Kayıtlı aktiviteniz başarıyla silindi", colour=discord.Colour(0x72130f), description="Eğer bu işte bir hata olduğunu düşünüyorsanız [server](https://discord.com/invite/2wknBWEQWS)'ımızdaki developerlarımızla iletişime geçebilirsiniz")

        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/750685247489835089/834095429347049492/delete-animation.gif")
        embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        b = ctx.message.channel
        d = await bot.fetch_user(author)
        embed.add_field(name=":pencil2:", value=d, inline=True)
        embed.add_field(name=":mega:", value=b, inline=True)
     
        await ctx.send(embed=embed)

    async def refailed(ctx):
        embed = discord.Embed(title="Bu şehre ait kayıtlı bilgi yok", colour=discord.Colour(0x72130f), description="Eğer bu işte bir hata olduğunu düşünüyorsanız [server](https://discord.com/invite/2wknBWEQWS)'ımızdaki developerlarımızla iletişime geçebilirsiniz")

        embed.set_thumbnail(url="https://www.zambo.in/assets/quize/wrongs.gif")
        embed.set_author(name=ctx.message.author, icon_url=ctx.author.avatar_url)
        
        await ctx.send(embed=embed)

    def for_log(gid,user,channel,name):
        trtime = get()
        if len(str(trtime.minute)) == 1:
            minute = "0"+ str(trtime.minute)
        else:
            minute = trtime.minute
        print(f"[{trtime.hour}:{minute}:{trtime.second}  {trtime.day}/{trtime.month}/{trtime.year}] {user} created oto message protocol #{channel} city: {name} guild: {gid}")