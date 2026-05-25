import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class LegendBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        cogs = ["hosting", "support", "admin", "events"]
        for cog in cogs:
            try:
                await self.load_extension(f"cogs.{cog}")
                print(f"✅ Cog geladen: {cog}")
            except Exception as e:
                print(f"❌ Fout bij laden van {cog}: {e}")

        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            print(f"📋 {len(synced)} commando's gesynchroniseerd (guild-specifiek)")
        else:
            synced = await self.tree.sync()
            print(f"🌐 {len(synced)} commando's gesynchroniseerd (globaal)")

    async def on_command_error(self, ctx, error):
        pass


async def main():
    if not TOKEN:
        print("❌ DISCORD_TOKEN niet gevonden in .env bestand!")
        print("📝 Kopieer .env.example naar .env en vul je token in.")
        return

    bot = LegendBot()
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
