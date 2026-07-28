import html
import re
from urllib.parse import urlparse

from config import (
    BREAKING_CHANNEL,
    FOOTBALL_CHANNEL,
    WORLD_CHANNEL,
)

from news_type import NewsType
from team_detector import TeamDetector
from league_detector import LeagueDetector


class Formatter:

    @staticmethod
    def clean(text: str):

        if not text:
            return ""

        text = html.unescape(text)

        text = re.sub(r"<[^>]+>", "", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def get_summary(entry):

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
    def get_source(link):

        domain = urlparse(link).netloc.lower()

        if "bbc" in domain:
            return "BBC Sport"

        if "espn" in domain:
            return "ESPN"

        if "nba.com" in domain:
            return "NBA"

        if "atptour" in domain:
            return "ATP Tour"

        if "reuters" in domain:
            return "Reuters"

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
            return "🏆 @sportworldupdate"

        return "🏆 Sports News"

    @staticmethod
    def build_message(channel, entry, hashtags):

        title = Formatter.clean(
            getattr(entry, "title", "")
        )

        summary = Formatter.get_summary(entry)

        source = Formatter.get_source(
            getattr(entry, "link", "")
        )

        link = getattr(entry, "link", "")

        news_type = NewsType.detect(title)

        teams = TeamDetector.detect(title)

        leagues = LeagueDetector.detect(title)

        footer = Formatter.get_footer(channel)

        message = (
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{news_type}\n\n"
            f"📰 <b>{title}</b>\n\n"
        )

        if summary:

            message += (
                f"📝 {summary}\n\n"
            )

        if leagues:

            message += (
                "🏆 <b>Competition</b>\n"
                f"{', '.join(leagues)}\n\n"
            )

        if teams:

            message += (
                "👥 <b>Teams</b>\n"
                f"{' • '.join(teams)}\n\n"
            )

        message += (
            f"📰 <b>Source</b>\n"
            f"{source}\n\n"
            f"🔗 <a href=\"{link}\">Read Full Story</a>\n\n"
            f"{hashtags}\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{footer}"
        )

        return message
