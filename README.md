# LegendGamers Hosting — Discord Bot

Discord bot voor LegendGamers Hosting met slash commands voor prijzen, games, tickets en meer.

## Installatie

```bash
pip install -r requirements.txt
cp .env.example .env
# Vul je gegevens in .env in
python main.py
```

## .env instellen

| Variable | Beschrijving |
|---|---|
| `DISCORD_TOKEN` | Je bot token (van Discord Developer Portal) |
| `GUILD_ID` | Je server ID (voor snelle command sync, optioneel) |
| `SUPPORT_CHANNEL_ID` | Kanaal voor ticket notificaties |
| `LOG_CHANNEL_ID` | Kanaal voor logs (join/leave events) |
| `ADMIN_ROLE_ID` | Rol ID voor admins |
| `SUPPORT_ROLE_ID` | Rol ID voor support medewerkers |

## Commando's

| Commando | Beschrijving |
|---|---|
| `/prijzen` | Overzicht van alle hosting pakketten |
| `/pakket <naam>` | Details van een specifiek pakket |
| `/games` | Alle ondersteunde games |
| `/game <naam>` | Details van een specifieke game |
| `/bestellen` | Uitleg over hoe bestellen werkt |
| `/uptime` | Serverstatus |
| `/info` | Info over LegendGamers Hosting |
| `/faq` | Veelgestelde vragen |
| `/ticket` | Open een support ticket |
| `/panel` | Info over het klantenportaal |

### Admin commando's
| Commando | Beschrijving |
|---|---|
| `/aankondiging` | Stuur een aankondiging |
| `/onderhoud` | Onderhoudsmodus aan/uit |
| `/welkom_setup` | Stuur het welkomstpaneel |
| `/prijs_update` | Pas een pakketprijs aan |
| `/sync` | Herlaad slash commands |

## Structuur

```
├── main.py              # Hoofdbot
├── cogs/
│   ├── hosting.py       # Prijzen, games, bestellen
│   ├── support.py       # Tickets, FAQ, panel
│   ├── admin.py         # Admin commando's
│   └── events.py        # Welkom/log events
└── data/
    ├── prijzen.json     # Pakket prijzen en details
    ├── games.json       # Ondersteunde games
    └── faq.json         # FAQ vragen en antwoorden
```
