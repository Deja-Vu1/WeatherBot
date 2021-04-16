import discord
from interfaces.methods.current_tr_time import get

def help_us(bot):
    footext = "Developed by bis ❤️ "
    @bot.command(aliases=['yardim','yardım'])
    async def help(ctx):
        now_turkey = get()
        embed = discord.Embed(title="YARDIM", colour=discord.Colour(0xA3FFA9))
        embed.add_field(name="<:map:832150636228247553>", value="**!weather** ``<şehir>``\nAtlasta bulabildiğim kadar şehrin hava durumunu getirebilirim\n||öyle, değil mi?||", inline=True)
        embed.add_field(name="<:screwdriver:832150872221548564>", value="**!setup** ``<şehir>``\nYazdığınız kanala her gün hava durumu raporu gönderebilirim", inline=True)
        embed.add_field(name="<:track_previous:832152345399525377>", value="**!resetup** ``<şehir>``\nYazdığınız kanala her gün gönderdiğim hava durumu raporunu kaldırabilirim", inline=True)
        embed.add_field(name="‎", value="||‎|| [Sunucuya ekle](https://discord.com/oauth2/authorize?client_id=829685204641513532&permissions=93184&scope=bot) | [Oy ver](https://top.gg/bot/829685204641513532)", inline=True)
        embed.set_image(url="https://raw.githubusercontent.com/Deja-Vu1/WeatherBot/main/Img/discordimage-1.png")
        embed.set_footer(text=footext+" bugün saat "+str(now_turkey.hour)+":"+str(now_turkey.minute),icon_url="https://cdn.discordapp.com/avatars/596455467585110016/b96ac044a4382f62ad36637c6021ef80.png?size=256")
        
        await ctx.message.channel.send(embed=embed)