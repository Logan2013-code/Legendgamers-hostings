import sys
import os
import types

# Inject audioop stub for Python 3.13+ (audioop was removed from stdlib)
if 'audioop' not in sys.modules:
    _audioop = types.ModuleType('audioop')
    _noop = lambda *a, **k: b''
    for _fn in ['bias','mul','tostereo','tomono','ratecv','lin2lin','ulaw2lin',
                'lin2ulaw','alaw2lin','lin2alaw','add','reverse','cross','avg',
                'avgpp','max','maxpp','minmax','rms','findfactor','findfit',
                'findmax','getsample']:
        setattr(_audioop, _fn, _noop)
    sys.modules['audioop'] = _audioop

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

    async def on_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        print(f"❌ Fout in commando: {error}")
        import traceback
        traceback.print_exc()
        try:
            await interaction.response.send_message(f"❌ Er ging iets mis: `{error}`", ephemeral=True)
        except Exception:
            try:
                await interaction.followup.send(f"❌ Er ging iets mis: `{error}`", ephemeral=True)
            except Exception:
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
