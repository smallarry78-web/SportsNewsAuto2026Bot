import hashlib
import feedparser

from config import CHANNEL_FEEDS, MAX_ARTICLES_PER_FEED
from database import db
from formatter import Formatter
from hashtags import Hashtags


class RSSFetcher:

    @staticmethod
    def article_id(title: str, link: str) -> str:
        """
        Create a unique ID using both the title and link.
        This helps reduce reposts if a publisher changes a URL.
        """

        text = (
            title.strip().lower()
            + "|"
            + link.strip().lower()
        )

        return hashlib.md5(text.encode("utf-8")).hexdigest()

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

                        title = entry.title.strip()
                        link = entry.link.strip()

                        uid = RSSFetcher.article_id(
                            title,
                            link
                        )

                        if db.is_posted(uid, channel):
                            continue

                        hashtags = Hashtags.generate(title)

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
