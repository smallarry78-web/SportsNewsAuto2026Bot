import html
from urllib.parse import urlparse

from config import (
    BREAKING_CHANNEL,
    FOOTBALL_CHANNEL,
    WORLD_CHANNEL,
)


class Formatter:

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        text = html.unescape(text)

        text = text.replace("<p>", "")
        text = text.replace("</p>", "")
        text = text.replace("<br>", "")
        text = text.replace("<br/>", "")
        text = text.replace("<br />", "")

        return text.strip()

    @staticmethod
    def summary(entry) -> str:

        summary = ""

        if hasattr(entry, "summary"):
            summary = entry.summary

        elif hasattr(entry, "description"):
            summary = entry.description

        summary = Formatter.clean(summary)

        if len(summary) > 220:
            summary = summary[:220].rsplit(" ", 1)[0] + "..."

        return summary

    @staticmethod
    def source(link: str) -> str:

        domain = urlparse(link).netloc.lower()

        if "bbc" in domain:
            return "BBC Sport"

        if "espn" in domain:
            return "ESPN"

        if "reuters" in domain:
            return "Reuters"

        if "nba.com" in domain:
            return "NBA"

        if "atptour" in domain:
            return "ATP Tour"

        return domain.replace("www.", "").title()

    @staticmethod
    def channel_brand(channel):

        if channel == BREAKING_CHANNEL:
            return {
                "header": "🚨 BREAKING SPORTS",
                "footer": "📡 @breakingsportsnews"
            }

        if channel == FOOTBALL_CHANNEL:
            return {
                "header": "⚽ FOOTBALL DAILY",
                "footer": "⚽ @footballdnews"
            }

        if channel == WORLD_CHANNEL:
            return {
                "header": "🏆 SPORTS WORLD",
                "footer": "🏆 @sportworldupdate"
            }

        return {
            "header": "🏆 SPORTS NEWS",
            "footer": ""
        }

    @staticmethod
    def build(channel, entry, hashtags):

        brand = Formatter.channel_brand(channel)

        title = Formatter.clean(entry.title)

        summary = Formatter.summary(entry)

        source = Formatter.source(entry.link)

        message = (
            f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{brand['header']}\n\n"
            f"📰 <b>{title}</b>\n\n"
        )

        if summary:
            message += f"📝 {summary}\n\n"

        message += (
            f"📰 <b>Source:</b> {source}\n\n"
            f"🔗 <a href=\"{entry.link}\">Read Full Story</a>\n\n"
            f"{hashtags}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{brand['footer']}"
        )

        return message
