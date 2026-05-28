import discord
from discord.ext import commands
from discord import app_commands
import json
import os


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def laad_prijzen():
    with open(os.path.join(DATA_DIR, 'prijzen.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def laad_games():
    with open(os.path.join(DATA_DIR, 'games.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class HostingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="prijzen", description="Bekijk alle hosting pakketten en prijzen")
    async def prijzen(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = laad_prijzen()
        pakketten = data["pakketten"]

        embed = discord.Embed(
            title="🖥️ LegendGamers Hosting — Pakketten",
            description=(
                "Kies het pakket dat bij jouw server past.\n"
                "Alle pakketten inclusief **DDoS bescherming**, **gratis SSL** en **99.9% uptime garantie**!\n\n"
                "Gebruik `/pakket <naam>` voor meer details over een specifiek pakket."
            ),
            color=0x5865F2
        )

        for p in pakketten:
            sterretje = " ⭐ POPULAIR" if p["populair"] else ""
            waarde = (
                f"💾 RAM: **{p['ram']}** | 🔥 CPU: **{p['cpu']}**\n"
                f"💽 Opslag: **{p['opslag']}**\n"
                f"💰 Vanaf **€{p['prijs_maand']}/maand**"
            )
            embed.add_field(
                name=f"{p['emoji']} {p['naam']}{sterretje}",
                value=waarde,
                inline=True
            )

        embed.add_field(
            name="💡 Kortingen",
            value=(
                f"📅 Kwartaal: **{data['korting']['kwartaal_procent']}% korting**\n"
                f"📅 Jaarlijks: **{data['korting']['jaar_procent']}% korting**"
            ),
            inline=False
        )

        betaal = " | ".join(data["betaalmethoden"])
        embed.set_footer(text=f"Betaalmethoden: {betaal}")
        embed.set_thumbnail(url="https://i.imgur.com/wSTFkRM.png")

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="pakket", description="Bekijk details van een specifiek hosting pakket")
    @app_commands.describe(naam="De naam van het pakket (starter, basic, pro, premium, extreme)")
    async def pakket(self, interaction: discord.Interaction, naam: str):
        await interaction.response.defer()
        data = laad_prijzen()
        pakket = next((p for p in data["pakketten"] if p["id"] == naam.lower()), None)

        if not pakket:
            namen = ", ".join(p["id"] for p in data["pakketten"])
            await interaction.followup.send(
                f"❌ Pakket `{naam}` niet gevonden. Beschikbaar: `{namen}`",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"{pakket['emoji']} {pakket['naam']} Pakket",
            color=pakket["kleur"]
        )

        embed.add_field(name="💾 RAM", value=pakket["ram"], inline=True)
        embed.add_field(name="🔥 CPU", value=pakket["cpu"], inline=True)
        embed.add_field(name="💽 Opslag", value=pakket["opslag"], inline=True)
        embed.add_field(name="👥 Spelers", value=pakket["spelers"], inline=True)
        embed.add_field(name="📦 Backups", value=pakket["backups"], inline=True)
        embed.add_field(name="🗄️ Databases", value=pakket["databases"], inline=True)
        embed.add_field(name="🎮 Geschikt voor", value="\n".join(f"• {g}" for g in pakket["geschikt_voor"]), inline=False)
        embed.add_field(name="🛟 Support", value=pakket["support"], inline=False)

        korting_kwartaal = data["korting"]["kwartaal_procent"]
        korting_jaar = data["korting"]["jaar_procent"]
        embed.add_field(
            name="💰 Prijzen",
            value=(
                f"📆 Maandelijks: **€{pakket['prijs_maand']}/maand**\n"
                f"📅 Kwartaal: **€{pakket['prijs_kwartaal']}/kwartaal** ({korting_kwartaal}% korting)\n"
                f"🗓️ Jaarlijks: **€{pakket['prijs_jaar']}/jaar** ({korting_jaar}% korting)"
            ),
            inline=False
        )

        if pakket["populair"]:
            embed.set_author(name="⭐ MEEST GEKOZEN PAKKET")

        embed.set_footer(text="Gebruik /bestellen om dit pakket te bestellen!")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="games", description="Bekijk alle beschikbare games voor hosting")
    async def games(self, interaction: discord.Interaction):
        await interaction.response.defer()
        data = laad_games()
        games_lijst = data["games"]

        embed = discord.Embed(
            title="🎮 Beschikbare Games voor Hosting",
            description="Wij ondersteunen de volgende games. Mis je een game? Open een ticket!",
            color=0x5865F2
        )

        populaire = [g for g in games_lijst if g["populair"]]
        overige = [g for g in games_lijst if not g["populair"]]

        if populaire:
            tekst = ""
            for g in populaire:
                tekst += f"{g['emoji']} **{g['name']}** — Min. {g['min_ram']} RAM\n"
            embed.add_field(name="⭐ Populaire Games", value=tekst, inline=False)

        if overige:
            tekst = ""
            for g in overige:
                tekst += f"{g['emoji']} **{g['name']}** — Min. {g['min_ram']} RAM\n"
            embed.add_field(name="🎯 Overige Games", value=tekst, inline=False)

        embed.add_field(
            name="❓ Game niet in de lijst?",
            value="Open een **ticket** via `/ticket` en we kijken samen wat we voor je kunnen doen!",
            inline=False
        )
        embed.set_footer(text="Gebruik /game <naam> voor meer info over een specifieke game")

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="game", description="Bekijk details over een specifieke game hosting")
    @app_commands.describe(naam="De naam van de game")
    async def game(self, interaction: discord.Interaction, naam: str):
        await interaction.response.defer()
        data = laad_games()
        zoek = naam.lower().replace(" ", "")
        gevonden = next(
            (g for g in data["games"] if zoek in g["id"] or zoek in g["name"].lower().replace(" ", "")),
            None
        )

        if not gevonden:
            namen = ", ".join(g["name"] for g in data["games"])
            await interaction.followup.send(
                f"❌ Game `{naam}` niet gevonden.\nBeschikbare games: {namen}",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"{gevonden['emoji']} {gevonden['name']} Hosting",
            description=gevonden["beschrijving"],
            color=0x5865F2
        )
        embed.add_field(name="💾 Minimaal RAM", value=gevonden["min_ram"], inline=True)
        embed.add_field(name="📋 Versies", value="\n".join(f"• {v}" for v in gevonden["versies"]), inline=False)

        if gevonden["populair"]:
            embed.set_author(name="⭐ Populaire keuze!")

        embed.set_footer(text="Bekijk /prijzen voor passende pakketten!")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="bestellen", description="Informatie over hoe je een server kunt bestellen")
    async def bestellen(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(
            title="🛒 Hoe bestel je een server?",
            description="In 3 simpele stappen heb jij jouw server online!",
            color=0x57F287
        )

        embed.add_field(name="Stap 1 — Kies je pakket", value="Gebruik `/prijzen` om alle pakketten te bekijken en kies er één die bij je past.", inline=False)
        embed.add_field(name="Stap 2 — Open een ticket", value="Gebruik `/ticket` en geef aan welk pakket en welke game je wilt. We helpen je verder!", inline=False)
        embed.add_field(name="Stap 3 — Betalen & Online!", value="Na betaling is je server **binnen 60 seconden** online. Zo simpel is het!", inline=False)
        embed.add_field(name="💳 Betaalmethoden", value="iDEAL • PayPal • Creditcard • Crypto • Bankoverschrijving", inline=False)
        embed.add_field(name="🛡️ 7-daagse geld-terug garantie", value="Niet tevreden? Geen probleem — we geven je geld terug, geen vragen gesteld.", inline=False)

        embed.set_footer(text="Vragen? Gebruik /ticket voor ondersteuning!")
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="uptime", description="Bekijk de huidige serverstatus en uptime garantie")
    async def uptime(self, interaction: discord.Interaction):
        await interaction.response.defer()
        embed = discord.Embed(title="📊 Serverstatus & Uptime", color=0x57F287)
        embed.add_field(name="✅ Netwerk", value="Operationeel", inline=True)
        embed.add_field(name="✅ Panel", value="Operationeel", inline=True)
        embed.add_field(name="✅ Game Servers", value="Operationeel", inline=True)
        embed.add_field(name="✅ Facturering", value="Operationeel", inline=True)
        embed.add_field(name="✅ DDoS Beveiliging", value="Actief", inline=True)
        embed.add_field(name="✅ Backupsysteem", value="Operationeel", inline=True)
        embed.add_field(name="🏆 Uptime Garantie", value="Wij garanderen **99.9% uptime** voor al onze servers.", inline=False)
        embed.set_footer(text="Status bijgewerkt — LegendGamers Hosting")
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HostingCog(bot))
