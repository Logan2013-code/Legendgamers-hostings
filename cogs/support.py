import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime


def laad_faq():
    pad = os.path.join(os.path.dirname(__file__), '..', 'data', 'faq.json')
    with open(pad, 'r', encoding='utf-8') as f:
        return json.load(f)


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Ticket Sluiten", style=discord.ButtonStyle.danger, custom_id="sluit_ticket")
    async def sluit_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        kanaal = interaction.channel
        if not kanaal.name.startswith("ticket-"):
            await interaction.response.send_message("Dit is geen ticketkanaal.", ephemeral=True)
            return

        embed = discord.Embed(
            title="🔒 Ticket wordt gesloten",
            description=f"Ticket gesloten door {interaction.user.mention}.\nKanaal wordt over 5 seconden verwijderd.",
            color=0xE74C3C
        )
        await interaction.response.send_message(embed=embed)
        await discord.utils.sleep_until(datetime.utcnow().replace(second=datetime.utcnow().second + 5))
        try:
            await kanaal.delete(reason=f"Ticket gesloten door {interaction.user}")
        except discord.NotFound:
            pass


class TicketSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.select(
        placeholder="Kies het type ticket...",
        custom_id="ticket_type",
        options=[
            discord.SelectOption(label="🛒 Nieuwe Bestelling", value="bestelling", description="Ik wil een server bestellen"),
            discord.SelectOption(label="🛟 Technische Support", value="support", description="Ik heb een probleem met mijn server"),
            discord.SelectOption(label="💰 Facturering", value="facturering", description="Vragen over facturen of betalingen"),
            discord.SelectOption(label="🔼 Upgrade / Downgrade", value="upgrade", description="Ik wil mijn pakket aanpassen"),
            discord.SelectOption(label="❓ Overige Vraag", value="overig", description="Ik heb een andere vraag"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        soort = select.values[0]
        guild = interaction.guild
        lid = interaction.user

        bestaand = discord.utils.get(guild.text_channels, name=f"ticket-{lid.name.lower()}")
        if bestaand:
            await interaction.response.send_message(
                f"❌ Je hebt al een open ticket: {bestaand.mention}",
                ephemeral=True
            )
            return

        soort_namen = {
            "bestelling": "🛒 Nieuwe Bestelling",
            "support": "🛟 Technische Support",
            "facturering": "💰 Facturering",
            "upgrade": "🔼 Upgrade / Downgrade",
            "overig": "❓ Overige Vraag"
        }

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            lid: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        admin_rol_id = int(os.getenv("ADMIN_ROLE_ID", 0))
        support_rol_id = int(os.getenv("SUPPORT_ROLE_ID", 0))

        for rol_id in [admin_rol_id, support_rol_id]:
            if rol_id:
                rol = guild.get_role(rol_id)
                if rol:
                    overwrites[rol] = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)

        ticket_categorie = discord.utils.get(guild.categories, name="📋 Tickets")
        kanaal = await guild.create_text_channel(
            name=f"ticket-{lid.name.lower()}",
            overwrites=overwrites,
            category=ticket_categorie
        )

        embed = discord.Embed(
            title=f"🎫 Ticket — {soort_namen[soort]}",
            description=(
                f"Welkom {lid.mention}! Een medewerker helpt je zo snel mogelijk.\n\n"
                f"**Type:** {soort_namen[soort]}\n"
                f"**Aangemaakt door:** {lid.mention}\n"
                f"**Datum:** <t:{int(datetime.now().timestamp())}:F>\n\n"
                "Beschrijf je vraag of probleem zo duidelijk mogelijk.\n"
                "Sluit het ticket via de knop hieronder als alles opgelost is."
            ),
            color=0x5865F2
        )
        embed.set_footer(text="LegendGamers Hosting Support")

        await kanaal.send(embed=embed, view=TicketView())
        await interaction.response.send_message(
            f"✅ Ticket aangemaakt: {kanaal.mention}",
            ephemeral=True
        )


class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ticket", description="Open een support ticket")
    async def ticket(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 Support Ticket",
            description=(
                "Kies hieronder het type van je ticket.\n"
                "Een van onze medewerkers helpt je zo snel mogelijk!\n\n"
                "⏱️ Gemiddelde reactietijd: **< 1 uur**"
            ),
            color=0x5865F2
        )
        embed.set_footer(text="LegendGamers Hosting Support")
        await interaction.response.send_message(embed=embed, view=TicketSelectView(), ephemeral=True)

    @app_commands.command(name="faq", description="Bekijk veelgestelde vragen")
    async def faq(self, interaction: discord.Interaction):
        data = laad_faq()

        embed = discord.Embed(
            title="❓ Veelgestelde Vragen (FAQ)",
            description="Hieronder vind je antwoorden op de meest gestelde vragen.",
            color=0x5865F2
        )

        for item in data["vragen"]:
            embed.add_field(
                name=f"❔ {item['vraag']}",
                value=item["antwoord"],
                inline=False
            )

        embed.set_footer(text="Staat je vraag er niet bij? Gebruik /ticket voor persoonlijke hulp!")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="panel", description="Krijg toegang tot het beheer panel")
    async def panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🖥️ Klantenportaal",
            description=(
                "Beheer al je servers via ons gebruiksvriendelijke panel!\n\n"
                "**Wat kun je allemaal doen in het panel?**\n"
                "• ▶️ Server starten, stoppen en herstarten\n"
                "• 📁 Bestanden beheren via FTP/bestandsbeheer\n"
                "• 📦 Backups aanmaken en terugzetten\n"
                "• 📊 CPU, RAM en netwerk statistieken bekijken\n"
                "• 🗄️ Databases aanmaken en beheren\n"
                "• 🔧 Server instellingen aanpassen\n"
                "• 📋 Console logboeken bekijken\n"
                "• 🕐 Geplande taken instellen\n\n"
                "🔐 Log in met je e-mailadres en wachtwoord die je bij bestelling hebt ontvangen."
            ),
            color=0x5865F2
        )
        embed.set_footer(text="Inloggegevens vergeten? Open een ticket via /ticket")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="info", description="Algemene informatie over LegendGamers Hosting")
    async def info(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🏠 Over LegendGamers Hosting",
            description=(
                "**LegendGamers Hosting** is jouw betrouwbare partner voor game server hosting!\n\n"
                "Wij bieden betaalbare, snelle en stabiele game servers voor de meest populaire games."
            ),
            color=0x5865F2
        )
        embed.add_field(
            name="🚀 Waarom LegendGamers?",
            value=(
                "• **Instant setup** — server in 60 seconden online\n"
                "• **99.9% uptime** garantie\n"
                "• **DDoS bescherming** inbegrepen\n"
                "• **NVMe SSD** opslag voor maximale snelheid\n"
                "• **24/7 support** via Discord tickets\n"
                "• **Vriendelijke prijzen** voor elke budget"
            ),
            inline=False
        )
        embed.add_field(
            name="📍 Locaties",
            value="🇳🇱 Nederland (Amsterdam) • 🇩🇪 Duitsland (Frankfurt)",
            inline=False
        )
        embed.add_field(
            name="🔧 Handige Commando's",
            value=(
                "`/prijzen` — Alle pakketten\n"
                "`/games` — Beschikbare games\n"
                "`/bestellen` — Hoe bestellen\n"
                "`/faq` — Veelgestelde vragen\n"
                "`/ticket` — Support ticket"
            ),
            inline=False
        )
        embed.set_footer(text="LegendGamers Hosting — Gaming op zijn best!")
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(SupportCog(bot))
