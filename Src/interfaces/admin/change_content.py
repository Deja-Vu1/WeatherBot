import discord
import json

ADMINID = [596455467585110016,476010467404546052]
def security(bot,weekly):
    @bot.command(hidden=True)
    async def change_content(ctx,*,content):
        
        if int(ctx.message.author.id) in ADMINID:
            content = content.replace("```json","")
            content = content.replace("```","")
            weekly = json.loads(content)
            with open('hello.json', 'w') as outfile:
                json.dump(weekly, outfile)
            for i in ADMINID:
                user = await bot.fetch_user(i)
                await user.send(f"{ctx.message.author} hello.json'un içeriğini değiştirdi\n```json\n"+ json.dumps(weekly,indent=4) +"\n```")
        else:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.send("Sshh... kimse görmesin. Bu komudu kullanmaya yetkin yok :/",delete_after=5)
