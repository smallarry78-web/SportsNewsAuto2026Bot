import hashlib
import feedparser
import html
from database import db
from config import CHANNEL_FEEDS


class RSSFetcher:

    @staticmethod
    def article_id(link: str):
        return hashlib.md5(link.encode()).hexdigest()

    @staticmethod
    def hashtags(title: str):

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
    def clean(text):

        if not text:
            return ""

        text = html.unescape(text)

        return text.strip()

    @staticmethod
    def build_message(entry):

        title = RSSFetcher.clean(entry.title)

        link = entry.link

        tags = RSSFetcher.hashtags(title)

        return f"""🏆 <b>SPORTS NEWS</b>

📰 <b>{title}</b>

👉 <a href="{link}">Read Full Story</a>

{tags}
"""

    @staticmethod
    def fetch_new_articles():

        articles = []

        for channel, feeds in CHANNEL_FEEDS.items():

            for feed in feeds:

                try:

                    rss = feedparser.parse(feed)

                    if not rss.entries:
                        continue

                    for entry in rss.entries[:10]:

                        uid = RSSFetcher.article_id(entry.link)

                        if db.is_posted(uid, channel):
                            continue

                        articles.append({
                            "channel": channel,
                            "id": uid,
                            "message": RSSFetcher.build_message(entry)
                        })

                except Exception as e:

                    print(e)

        return articles
