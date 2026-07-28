import hashlib
import feedparser

from config import CHANNEL_FEEDS, MAX_ARTICLES_PER_FEED
from database import db
from formatter import Formatter


class RSSFetcher:

    @staticmethod
    def article_id(link: str) -> str:
        return hashlib.md5(link.encode("utf-8")).hexdigest()

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
            "man city",
            "man united",
            "real madrid",
            "barcelona",
            "goal",
            "fifa",
            "uefa",
            "tottenham",
            "newcastle",
            "psg",
            "inter",
            "milan",
            "juventus",
        ]

        nba = [
            "nba",
            "basketball",
            "lakers",
            "warriors",
            "celtics",
            "bucks",
            "heat",
            "knicks",
            "bulls",
        ]

        tennis = [
            "tennis",
            "wimbledon",
            "atp",
            "wta",
            "us open",
            "roland garros",
            "australian open",
        ]

        formula = [
            "formula",
            "formula 1",
            "f1",
            "grand prix",
            "verstappen",
            "hamilton",
            "ferrari",
            "mclaren",
            "mercedes",
            "red bull",
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
    def fetch_new_articles():

        articles = []

        for channel, feeds in CHANNEL_FEEDS.items():

            for feed in feeds:

                try:

                    rss = feedparser.parse(feed)

                    if not rss.entries:
                        continue

                    for entry in rss.entries[:MAX_ARTICLES_PER_FEED]:

                        if not hasattr(entry, "title"):
                            continue

                        if not hasattr(entry, "link"):
                            continue

                        uid = RSSFetcher.article_id(entry.link)

                        if db.is_posted(uid, channel):
                            continue

                        hashtags = RSSFetcher.hashtags(entry.title)

                        message = Formatter.build_message(
                            channel=channel,
                            entry=entry,
                            hashtags=hashtags
                        )

                        articles.append(
                            {
                                "channel": channel,
                                "id": uid,
                                "message": message,
                            }
                        )

                except Exception as e:

                    print(f"RSS Error ({feed}): {e}")

        return articles
