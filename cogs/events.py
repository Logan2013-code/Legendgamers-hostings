import discord
from discord.ext import commands
import os
from datetime import datetime


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild

        welkom_kanaal = discord.utils.find(
            lambda c: c.name in ("welkom", "welcome", "algemeen", "general"),
            guild.text_channels
        )

        if not welkom_kanaal:
            return

        embed = discord.Embed(
            title=f"👋 Welkom, {member.display_name}!",
            description=(
                f"Hey {member.mention}, welkom op **{guild.name}**!\n\n"
                "We zijn blij dat je er bij bent! Hier zijn wat handige commando's om te beginnen:\n\n"
                "`/info` — Over ons\n"
                "`/prijzen` — Bekijk onze hosting pakketten\n"
                "`/games` — Beschikbare games\n"
                "`/faq` — Veelgestelde vragen\n"
                "`/ticket` — Hulp nodig? Open een ticket!"
            ),
            color=0x5865F2
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text=f"LegendGamers Hosting • Lid #{guild.member_count}",
            icon_url=guild.icon.url if guild.icon else None
        )
        embed.timestamp = datetime.now()

        await welkom_kanaal.send(embed=embed)

        log_kanaal_id = int(os.getenv("LOG_CHANNEL_ID", 0))
        if log_kanaal_id:
            log_kanaal = guild.get_channel(log_kanaal_id)
            if log_kanaal:
                log_embed = discord.Embed(
                    title="➕ Nieuw lid",
                    description=f"{member.mention} (`{member}`) heeft de server betreden.",
                    color=0x57F287
                )
                log_embed.add_field(name="Account aangemaakt", value=f"<t:{int(member.created_at.timestamp())}:R>")
                log_embed.set_thumbnail(url=member.display_avatar.url)
                log_embed.timestamp = datetime.now()
                await log_kanaal.send(embed=log_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        log_kanaal_id = int(os.getenv("LOG_CHANNEL_ID", 0))
        if not log_kanaal_id:
            return

        log_kanaal = member.guild.get_channel(log_kanaal_id)
        if not log_kanaal:
            return

        embed = discord.Embed(
            title="➖ Lid verlaten",
            description=f"{member.mention} (`{member}`) heeft de server verlaten.",
            color=0xE74C3C
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.timestamp = datetime.now()
        await log_kanaal.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"✅ Ingelogd als {self.bot.user} (ID: {self.bot.user.id})")
        print(f"📡 Verbonden met {len(self.bot.guilds)} server(s)")

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="🎮 LegendGamers Hosting | /prijzen"
            ),
            status=discord.Status.online
        )


async def setup(bot):
    await bot.add_cog(EventsCog(bot))
