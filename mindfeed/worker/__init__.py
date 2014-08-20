import time

from mindfeed.db import Feed, FeedFetcher
from mindfeed.email import MailService

mail_service = MailService()


def main():
    while True:
        feed = Feed.oldest_outdated()
        if feed:
            feed_fetcher = FeedFetcher(feed)
            feed_fetcher.fetch()
            mail_service.send_fetch_report(feed_fetcher)
        else:
            time.sleep(5)
