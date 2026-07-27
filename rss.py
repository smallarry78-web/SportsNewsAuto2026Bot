import hashlib
import html
import feedparser

from database import db
from config import (
    CHANNEL_FEEDS,
    POST_TITLE,
    MAX_ARTICLES_PER_FEED,
)


class RSSFetcher:

    @staticmethod
    def article_id(link: str) -> str:
        return hashlib.md5(link.encode("utf-8")).hexdigest()

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        return html.unescape(text).strip()

    @staticmethod
    def hashtags(title: str) -> str:

        title = title.lower()

        tags = []

        football = [
            "football",
            "premier league",
            "champions league",
            "arsenal",
            "chelsea",
            "liverpool",
            "manchester",
            "barcelona",
            "real madrid",
            "goal",
            "fifa",
            "uefa",
        ]

        nba = [
            "nba",
            "basketball",
            "lakers",
            "warriors",
            "celtics",
            "bucks",
        ]

        tennis = [
            "tennis",
            "wimbledon",
            "atp",
            "wta",
            "us open",
            "roland garros",
        ]

        formula = [
            "formula",
            "f1",
            "grand prix",
            "verstappen",
            "hamilton",
        ]

        if any(word in title for word in football):
            tags.append("#Football")

        if any(word in title for word in nba):
            tags.append("#NBA")

        if any(word in title for word in tennis):
            tags.append("#Tennis")

        if any(word in title for word in formula):
            tags.append("#Formula1")

        if not tags:
            tags.append("#Sports")

        return " ".join(tags)

    @staticmethod
    def build_message(entry):

        title = RSSFetcher.clean(entry.title)
        link = entry.link

        return (
            f"🏆 <b>{POST_TITLE}</b>\n\n"
            f"📰 <b>{title}</b>\n\n"
            f"👉 <a href=\"{link}\">Read Full Story</a>\n\n"
            f"{RSSFetcher.hashtags(title)}"
        )

    @staticmethod
    def fetch_new_articles():

        articles = []

        for channel, feeds in CHANNEL_FEEDS.items():

            for feed in feeds:

                try:

                    rss = feedparser.parse(feed)

                    if not rss.entries:
                        continue

                    for entry in rss.entries[:MAX_ARTICLES_PER_FEED]:

                        if not getattr(entry, "title", None):
                            continue

                        if not getattr(entry, "link", None):
                            continue

                        uid = RSSFetcher.article_id(entry.link)

                        if db.is_posted(uid, channel):
                            continue

                        articles.append(
                            {
                                "channel": channel,
                                "id": uid,
                                "message": RSSFetcher.build_message(entry),
                            }
                        )

                except Exception as e:

                    print(f"RSS Error: {e}")

        return articles
