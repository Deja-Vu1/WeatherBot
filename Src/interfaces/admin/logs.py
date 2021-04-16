import discord

ADMINID = [596455467585110016,476010467404546052]
async def oops_log(bot,cid,uid,name):
    embed = discord.Embed(title="**ERR 1.0**", colour=discord.Colour(0xd0021b), description="\n**Channel id:** " + str(cid) + "\n**User id:** " + str(uid) + "\n**City:** " + str(name))

    embed.set_footer(text="Information Service")
    embed.set_author(name="Otomatikleştirilmiş mesaj hatası", icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")
    for i in ADMINID:
        user = await bot.fetch_user(i)
        await user.send(embed=embed)

async def oops_log2(bot,channel,user,guild,name):
    embed = discord.Embed(title="**YENİ HABER !**", colour=discord.Colour(0x4aff00), description="\n**Guild id/name:** "+str(guild.id) + "/" + str(guild.name)+"\n**Channel id/name:** " + str(channel.id) + "/" + str(channel.name) + "\n**User id:** " + str(user.id) + "\n**City:** " + str(name))
    embed.set_footer(text="Otomatikleştirilmiş mesaj oluşturma")
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    embed.set_thumbnail(url=guild.icon_url)

    for i in ADMINID:
        user = await bot.fetch_user(i)
        await user.send(embed=embed)