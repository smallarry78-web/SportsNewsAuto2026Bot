import os
from dotenv import load_dotenv

load_dotenv()

# =====================================================
# BOT CONFIGURATION
# =====================================================

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

ADMIN_ID = int(os.getenv("ADMIN_ID", "8856521475"))

CHECK_INTERVAL = 30

# =====================================================
# TELEGRAM CHANNELS
# =====================================================

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

# =====================================================
# RSS FEEDS
# =====================================================

CHANNEL_FEEDS = {

    # GENERAL SPORTS NEWS
    BREAKING_CHANNEL: [

        "https://feeds.bbci.co.uk/sport/rss.xml",

    ],

    # FOOTBALL ONLY
    FOOTBALL_CHANNEL: [

        "https://feeds.bbci.co.uk/sport/football/rss.xml",

    ],

    # NBA + TENNIS + OTHER SPORTS
    WORLD_CHANNEL: [

        "https://www.nba.com/rss/nba_rss.xml",

        "https://www.atptour.com/en/media/rss-feed/xml",

    ],
}

# =====================================================
# MESSAGE SETTINGS
# =====================================================

POST_TITLE = "🏆 SPORTS NEWS"

ENABLE_PREVIEW = True

MAX_ARTICLES_PER_FEED = 10

REQUEST_TIMEOUT = 15
