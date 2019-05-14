"""
@project ensepro-embedding-service
@since 08/03/2019
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import re
from typing import List

from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import get_tmpfile

vector_files = {}
current_file = None


def similarity_words(word1: str, word2: str) -> float:
    try:
        return vector_files[current_file].similarity(word1, word2)
    except Exception as ex:
        return 0


def similarity_lists(list_words1: List[str], list_words2: List[str]):
    score = 0
    count = 0
    while list_words2 and count < 10:
        count += 1
        try:
            score = vector_files[current_file].n_similarity(list_words1, list_words2)
            break
        except KeyError as ex:
            list_words2.remove(re.search("'(.*)'", str(ex)).group(1))
            continue
        except Exception as ex:
            break

    return {
        "score": score,
        "words1": list_words1,
        "words2": list_words2
    }


def change_vector(new_vector_file, glove, binary, force_reload=False):
    global vector_files
    global current_file

    if force_reload and current_file in vector_files:
        del vector_files[current_file]

    load_vector(new_vector_file, glove, binary)


def load_vector(file: str, glove: bool, binary: bool):
    global vector_files
    global current_file

    if str(file) in vector_files:
        current_file = str(file)
        return

    current_file = str(file)
    if not glove:
        current_vector = KeyedVectors.load_word2vec_format(file, binary=binary)
        vector_files[current_file] = current_vector
        return

    if glove:
        tmp_file = get_tmpfile("glove2w2v_")
        glove2word2vec(file, tmp_file)
        current_vector = KeyedVectors.load_word2vec_format(tmp_file)
        vector_files[current_file] = current_vector
        return
