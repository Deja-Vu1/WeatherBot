import discord
from discord.ext import menus

def multi(embeds):
    class MultiPageEmbed(menus.ListPageSource):
        async def format_page(self, menu, entry):
            return entry
    menu = menus.MenuPages(MultiPageEmbed(embeds, per_page=1))
    return menu