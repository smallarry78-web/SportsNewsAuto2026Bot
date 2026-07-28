import html
import re
from urllib.parse import urlparse

from config import (
    BREAKING_CHANNEL,
    FOOTBALL_CHANNEL,
    WORLD_CHANNEL,
)

from news_type import NewsType


class Formatter:

    @staticmethod
    def clean(text: str) -> str:
        """Remove HTML tags and clean text."""

        if not text:
            return ""

        text = html.unescape(text)

        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def get_summary(entry) -> str:
        """Get RSS summary."""

        summary = ""

        if hasattr(entry, "summary"):
            summary = entry.summary

        elif hasattr(entry, "description"):
            summary = entry.description

        summary = Formatter.clean(summary)

        if len(summary) > 250:
            summary = summary[:250].rsplit(" ", 1)[0] + "..."

        return summary

    @staticmethod
    def get_source(link: str) -> str:
        """Detect source website."""

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

        if "goal.com" in domain:
            return "Goal"

        if "skysports" in domain:
            return "Sky Sports"

        return domain.replace("www.", "").title()

    @staticmethod
    def get_footer(channel):

        if channel == BREAKING_CHANNEL:
            return "📡 @breakingsportsnews"

        if channel == FOOTBALL_CHANNEL:
            return "⚽ @footballdnews"

        if channel == WORLD_CHANNEL:
            return "🏀 @sportworldupdate"

        return "🏆 Sports News"

    @staticmethod
    def build_message(channel, entry, hashtags):

        title = Formatter.clean(getattr(entry, "title", ""))

        summary = Formatter.get_summary(entry)

        source = Formatter.get_source(getattr(entry, "link", ""))

        news_type = NewsType.detect(title)

        footer = Formatter.get_footer(channel)

        link = getattr(entry, "link", "")

        message = (
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{news_type}\n\n"
            f"📰 <b>{title}</b>\n\n"
        )

        if summary:
            message += f"📝 {summary}\n\n"

        message += (
            f"📰 <b>Source:</b> {source}\n\n"
            f"🔗 <a href=\"{link}\">Read Full Story</a>\n\n"
            f"{hashtags}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{footer}"
        )

        return message
