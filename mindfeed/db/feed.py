class Feed(object):
    @classmethod
    def oldest_outdated(cls):
        return None

    @property
    def subscriber_emails(self):
        return []


class FeedFetcher(object):
    def __init__(self, feed):
        self.feed = feed

    def fetch(self):
        self.extract_features()

    def extract_features(self):
        pass

    def report(self):
        pass
