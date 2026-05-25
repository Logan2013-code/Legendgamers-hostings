import discord
from discord.ext import commands
from discord import app_commands
import json
import os


def is_admin():
    async def predicate(interaction: discord.Interaction) -> bool:
        owner_id = int(os.getenv("OWNER_ID", 0))
        if owner_id and interaction.user.id == owner_id:
            return True
        admin_rol_id = int(os.getenv("ADMIN_ROLE_ID", 0))
        if admin_rol_id:
            rol = interaction.guild.get_role(admin_rol_id)
            if rol and rol in interaction.user.roles:
                return True
        return interaction.user.guild_permissions.administrator
    return app_commands.check(predicate)


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="aankondiging", description="Stuur een aankondiging [Admin only]")
    @app_commands.describe(
        titel="Titel van de aankondiging",
        bericht="Inhoud van de aankondiging",
        kleur="Kleur van de embed (rood/groen/blauw/geel/paars)"
    )
    @is_admin()
    async def aankondiging(
        self,
        interaction: discord.Interaction,
        titel: str,
        bericht: str,
        kleur: str = "blauw"
    ):
        kleuren = {
            "rood": 0xE74C3C,
            "groen": 0x57F287,
            "blauw": 0x5865F2,
            "geel": 0xF1C40F,
            "paars": 0x9B59B6
        }
        kleur_code = kleuren.get(kleur.lower(), 0x5865F2)

        embed = discord.Embed(
            title=f"📢 {titel}",
            description=bericht,
            color=kleur_code
        )
        embed.set_footer(text=f"Aankondiging door {interaction.user.display_name} • LegendGamers Hosting")

        await interaction.response.send_message("✅ Aankondiging verstuurd!", ephemeral=True)
        await interaction.channel.send(embed=embed)

    @app_commands.command(name="onderhoud", description="Zet onderhoudsmodus aan/uit [Admin only]")
    @app_commands.describe(status="aan of uit", reden="Reden voor onderhoud")
    @is_admin()
    async def onderhoud(self, interaction: discord.Interaction, status: str, reden: str = "Gepland onderhoud"):
        if status.lower() == "aan":
            embed = discord.Embed(
                title="🔧 Onderhoud — Actief",
                description=(
                    f"**Reden:** {reden}\n\n"
                    "Onze servers ondergaan momenteel onderhoud.\n"
                    "We doen ons best om zo snel mogelijk weer online te zijn.\n"
                    "Excuses voor het ongemak!"
                ),
                color=0xF1C40F
            )
            embed.set_footer(text="LegendGamers Hosting — We zijn zo terug!")
        else:
            embed = discord.Embed(
                title="✅ Onderhoud — Voltooid",
                description=(
                    "Het onderhoud is afgerond!\n"
                    "Alle servers zijn weer volledig operationeel.\n"
                    "Bedankt voor je geduld!"
                ),
                color=0x57F287
            )
            embed.set_footer(text="LegendGamers Hosting — Terug online!")

        await interaction.response.send_message("✅ Status bijgewerkt!", ephemeral=True)
        await interaction.channel.send(embed=embed)

    @app_commands.command(name="welkom_setup", description="Stuur het welkomstpaneel [Admin only]")
    @is_admin()
    async def welkom_setup(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="👋 Welkom bij LegendGamers Hosting!",
            description=(
                "Welkom op de **officiële Discord** van LegendGamers Hosting!\n\n"
                "Hier vind je alle informatie over onze diensten, kun je support aanvragen "
                "en blijf je op de hoogte van het laatste nieuws.\n\n"
                "**Gebruik de knoppen of commando's hieronder om te beginnen!**"
            ),
            color=0x5865F2
        )

        embed.add_field(
            name="🚀 Snel Starten",
            value=(
                "`/prijzen` — Bekijk onze pakketten\n"
                "`/games` — Welke games supporten we?\n"
                "`/bestellen` — Hoe bestel ik een server?\n"
                "`/faq` — Veelgestelde vragen\n"
                "`/ticket` — Hulp nodig?"
            ),
            inline=True
        )

        embed.add_field(
            name="✨ Waarom LegendGamers?",
            value=(
                "⚡ Instant setup\n"
                "🛡️ DDoS bescherming\n"
                "💾 NVMe SSD opslag\n"
                "📊 99.9% uptime\n"
                "💰 Eerlijke prijzen"
            ),
            inline=True
        )

        embed.set_footer(text="LegendGamers Hosting — Gaming op zijn best! 🎮")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="prijs_update", description="Update de prijs van een pakket [Admin only]")
    @app_commands.describe(
        pakket="Pakket ID (starter/basic/pro/premium/extreme)",
        prijs_maand="Nieuwe maandprijs in euro's"
    )
    @is_admin()
    async def prijs_update(self, interaction: discord.Interaction, pakket: str, prijs_maand: float):
        pad = os.path.join(os.path.dirname(__file__), '..', 'data', 'prijzen.json')

        with open(pad, 'r', encoding='utf-8') as f:
            data = json.load(f)

        gevonden = False
        for p in data["pakketten"]:
            if p["id"] == pakket.lower():
                oude_prijs = p["prijs_maand"]
                p["prijs_maand"] = prijs_maand
                gevonden = True

                embed = discord.Embed(
                    title="✅ Prijs bijgewerkt",
                    color=0x57F287
                )
                embed.add_field(name="Pakket", value=p["naam"], inline=True)
                embed.add_field(name="Oude prijs", value=f"€{oude_prijs}/maand", inline=True)
                embed.add_field(name="Nieuwe prijs", value=f"€{prijs_maand}/maand", inline=True)
                break

        if not gevonden:
            await interaction.response.send_message(f"❌ Pakket `{pakket}` niet gevonden.", ephemeral=True)
            return

        with open(pad, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="sync", description="Synchroniseer slash commands [Admin only]")
    @is_admin()
    async def sync(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        synced = await self.bot.tree.sync()
        await interaction.followup.send(f"✅ {len(synced)} commando's gesynchroniseerd!", ephemeral=True)

    @aankondiging.error
    @onderhoud.error
    @welkom_setup.error
    @prijs_update.error
    @sync.error
    async def admin_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(
                "❌ Je hebt geen toestemming voor dit commando.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
