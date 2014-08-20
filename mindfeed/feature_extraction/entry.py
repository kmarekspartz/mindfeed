import math
from collections import defaultdict

from mindfeed.feature_extraction.nlp import feature_extractor


class Entry(object):
    link = None
    title = None
    summary = None
    published = None
    _features = {}
    _headers = set()
    _new_words = {}

    def __init__(self, **kwargs):
        self.link = kwargs['link']
        self.title = kwargs['title']
        self.summary = kwargs['summary']
        self.published = kwargs['published']

    @classmethod
    def from_feedparser_entry(cls, feedparser_entry):
        return cls(**feedparser_entry)

    @property
    def features(self):
        if not self._features:
            self.extract_features()
        return self._features

    def extract_features(self):
        summary_without_tags = strip_html(self.summary)
        self._features = feature_extractor(summary_without_tags)

    @property
    def bag_of_words(self):
        return self.features['types_to_counts']

    def new_words(self, previous_entries):
        previous_bag_of_words = defaultdict(default=0)
        for previous_entry in previous_entries:
            for word, count in previous_entry.bag_of_words:
                previous_bag_of_words[word] += count
        self._new_words = {
            word: count
            for word, count in self.bag_of_words.iteritems()
            if word not in previous_bag_of_words.keys()
        }
        return self._new_words

    def uniqueness(self, previous_entries):
        new_words = self.new_words(previous_entries)
        min_cos_distance = (
            1 - max([
                self.similarity(previous_entry)
                for previous_entry in previous_entries
            ])
        )
        self._features.update(
            new_words=new_words,
            number_of_new_types=len(new_words.keys()),
            number_of_new_tokens=sum(new_words.values()),
            min_cos_distance=min_cos_distance
        )

        def similarity(this, other):
            def sqrt_sum_squared(seq):
                return math.sqrt(sum([count ** 2 for count in seq]))

            def dot_product(a, b):
                words = set(a.keys() + b.keys())
                return sum(
                    a[word] * b[word]
                    for word in words
                )

            numerator = 1.0 * dot_product(
                this.bag_of_words,
                other.bag_of_words
            )
            denominator = (
                sqrt_sum_squared(this.bag_of_words) *
                sqrt_sum_squared(other.bag_of_words)
            )
            return numerator / denominator
