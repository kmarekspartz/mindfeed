from collections import Counter, defaultdict
from math import sqrt

import HTMLParser
import feedparser


class Post(object):
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.id_ = kwargs.get('id_', '')
        self.published = kwargs.get('published', None)
        self.links = kwargs.get('links', Counter())
        self.words = kwargs.get('words', Counter())
        self.images = kwargs.get('images', Counter())
        self.blockquotes = kwargs.get('blockquotes', 0)

    def similarity(self, other):
        # cosine
        words = set(self.words.keys() + other.words.keys())
        numerator = sum(self.words[w] * other.words[w] for w in words)
        def denominator_part(ws, counter):
            return sqrt(sum(counter[w] ** 2 for w in ws))
        denominator = denominator_part(words, self.words) * denominator_part(words, other.words)
        return numerator / denominator

    def insert_words(self, text):
        self.words = Counter()
        # nltk tokenizer?
        words = text.lower().split()
        # punctuation
        # stop words
        # numbers
        # code?
        for word in words:
            self.words[word] += 1


    def similar_posts(self, posts, n=10):
        return sorted(
            (p for p in posts if p is not self),
            key=lambda p: p.similarity(self)
        )[-n:]


class PostCollection(object):
    def __init__(self, posts):
        self.posts = posts

    @property
    def total_words(self):
        tw = Counter()
        for p in self.posts:
            tw.update(p.words)
        return tw

    def group_by(self, key):
        grouped = defaultdict(lambda: PostCollection([]))
        for p in self.posts:
            grouped[key(p)].posts.append(p)
        return grouped

    @property
    def group_by_month(self):
        for ym, posts in self.group_by(lambda p: (p.published.tm_year, p.published.tm_mon)).iteritems():
            year, month = ym
            yield year, month, posts

    @property
    def group_by_year(self):
        for year, posts in self.group_by(lambda p: p.published.tm_year).iteritems():
            yield year, posts

    def __len__(self):
        return len(self.posts)

    # https://en.wikipedia.org/wiki/Tf%E2%80%93idf

    @property
    def number_of_words(self):
        return sum(self.total_words.values())

    @property
    def words_per_post(self):
        return float(self.number_of_words) / len(self)

    @property
    def posts_per_month(self):
        for year, month, posts in self.group_by_month:
            yield year, month, len(posts)

    @property
    def posts_per_year(self):
        for year, posts in self.group_by_year:
            yield year, len(posts)

    @property
    def words_per_month(self):
        for year, month, posts in self.group_by_month:
            yield year, month, len(posts.total_words)

    @property
    def words_per_post_by_month(self):
        for year, month, posts in self.group_by_month:
            yield year, month, posts.words_per_post

    @property
    def words_per_post_by_year(self):
        for year, posts in self.group_by_year:
            yield year, posts.words_per_post


class PostExtractor(HTMLParser.HTMLParser):
    def __init__(self, entry):
        self.reset()
        self.fed = []
        self.post = Post(title=entry.title, id=entry.id, published=entry.published_parsed)
        self.feed(entry.summary)
        self.post.insert_words(''.join(self.fed))

    def handle_data(self, d):
        self.fed.append(d)

    def get_post(self):
        return self.post

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    self.post.links[value] += 1


def parse_entry(entry):
    s = PostExtractor(entry)
    return s.get_post()

def parse_file(fn):
    feed = feedparser.parse(fn)
    return PostCollection(map(parse_entry, feed.entries))

def main():
    feed = parse_file('file:///Users/kmarekspartz/src/other/kyle.marek-spartz.org/_site/atom-all.xml')

    for year, wpp in sorted(feed.words_per_post_by_year):
        print year, wpp

if __name__ == '__main__':
    main()
