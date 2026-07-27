import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# BOT
# ==========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

CHECK_INTERVAL = 30

# ==========================
# CHANNELS
# ==========================

BREAKING_CHANNEL = os.getenv(
    "BREAKING_CHANNEL",
    "@breakingsportsnews"
)

FOOTBALL_CHANNEL = os.getenv(
    "FOOTBALL_CHANNEL",
    "@footballdnews"
)

WORLD_CHANNEL = os.getenv(
    "WORLD_CHANNEL",
    "@sportworldupdate"
)

REQUIRED_CHANNELS = [
    BREAKING_CHANNEL,
    FOOTBALL_CHANNEL,
    WORLD_CHANNEL,
]

# ==========================
# RSS FEEDS
# ==========================

CHANNEL_FEEDS = {

    BREAKING_CHANNEL: [

        "https://feeds.bbci.co.uk/sport/rss.xml",

        "https://www.espn.com/espn/rss/news",

    ],

    FOOTBALL_CHANNEL: [

        "https://feeds.bbci.co.uk/sport/football/rss.xml",

    ],

    WORLD_CHANNEL: [

        "https://www.nba.com/rss/nba_rss.xml",

        "https://www.atptour.com/en/media/rss-feed/xml",

    ],

}
