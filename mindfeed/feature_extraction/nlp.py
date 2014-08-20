import math
from collections import defaultdict

from nltk import sent_tokenize, word_tokenize
import lxml.html
import readability


def strip_html(text):
    return lxml.html.fromstring(text).text_content()


def mean_length(items):
    return sum(map(len, items)) * 1.0 / len(items)


def readability_index(sents):
    return readability.getmeasures(sents)


def feature_extractor(text):
    sents = sent_tokenize(text)
    tokens = word_tokenize(text)
    types = set(tokens)
    types_to_counts = defaultdict(0)
    for token in tokens:
        types_to_counts[token] += 1
    return {
        "tokens": tokens,
        "types": types,
        "types_to_counts": types_to_counts,
        "shannon_index": shannon_index(types_to_counts),
        "number_of_tokens": len(tokens),
        "number_of_types": len(types),
        "mean_length_of_tokens": mean_length(tokens),
        "mean_lenght_of_types": mean_length(types),
        "readability_index": readability_index(sents)
    }


def shannon_index(types_to_counts):
    total = sum(types_to_counts.values())
    types_to_proportions = {
        _type: count * 1.0 / total
        for _type, count
        in types_to_counts.iteritems()
    }
    return -sum([
        p * math.log(p)
        for _type, p
        in types_to_proportions.iteritems()
    ])
