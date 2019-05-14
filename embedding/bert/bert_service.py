# -*- coding: utf-8 -*-

from typing import List

import numpy
from bert_serving.client import BertClient

IP = "127.0.0.1"
bc = BertClient(ip=IP)


def similarity_words(word1: str, word2: str) -> float:
    word1_vecs = bc.encode([word1])
    word2_vecs = bc.encode([word2])

    array_with_score = numpy.sum(word1_vecs * word2_vecs, axis=1) / numpy.linalg.norm(word1_vecs, axis=1)
    return array_with_score[0]


def similarity_lists(list_words1: List[str], list_words2: List[str]):
    words1_vecs = bc.encode([' '.join(list_words1)])
    words2_vecs = bc.encode([' '.join(list_words2)])

    array_with_score = numpy.sum(words1_vecs * words2_vecs, axis=1) / numpy.linalg.norm(words1_vecs, axis=1)
    return {
        "score": array_with_score[0],
        "words1": list_words1,
        "words2": list_words2
    }
