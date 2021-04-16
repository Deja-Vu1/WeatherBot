import discord
import json

ADMINID = [596455467585110016,476010467404546052]
def supervision(bot,weekly):
    @bot.command(hidden=True)
    async def hellojson(ctx):
        if int(ctx.message.author.id) in ADMINID:
            user = await bot.fetch_user(int(ctx.message.author.id))
            await user.send("```json\n"+ json.dumps(weekly,indent=4) +"\n```")
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send("Sshh... kimse görmesin. Bu komudu kullanmaya yetkin yok :/",delete_after=5)
