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
current_file = {}
current_lang = None
lang_order = []
active_langs = {}


def similarity_words(word1: str, word2: str) -> float:
    for lang in lang_order:
        if not active_langs[lang]:
            continue
        score = similarity_words_lang(word1, word2, lang)
        if score > 0:
            return score
    return 0


def similarity_words_lang(word1: str, word2: str, lang: str) -> float:
    try:
        return vector_files[lang][current_file[lang]].similarity(word1, word2)
    except Exception as ex:
        return 0


def similarity_lists(list_words1: List[str], list_words2: List[str]):
    for lang in lang_order:
        if not active_langs[lang]:
            continue
        result = similarity_lists_lang(list_words1, list_words2, lang)
        if result["score"] > 0:
            return result

    return {
        "score": 0,
        "words1": list_words1,
        "words2": list_words2
    }


def similarity_lists_lang(list_words1: List[str], list_words2: List[str], lang: str):
    score = 0
    count = 0
    while list_words2 and count < 10:
        count += 1
        try:
            score = vector_files[lang][current_file[lang]].n_similarity(list_words1, list_words2)
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


def toggle_lang(lang):
    active_langs[lang] = not active_langs[lang]


def list_langs():
    return [{"ordem": i, "lang": lang, "active": active_langs[lang]} for i, lang in enumerate(lang_order)]


def update_order(new_order):
    global lang_order
    lang_order = [lang for lang in new_order if lang in lang_order]
    lang_order += [lang for lang in vector_files if lang not in lang_order]


def change_vector(new_vector_file, glove, binary, lang, force_reload=False):
    global vector_files
    global current_file

    if lang not in vector_files:
        lang_order.append(lang)
        active_langs[lang] = True
        vector_files[lang] = {}

    if force_reload and new_vector_file in vector_files[lang]:
        del vector_files[lang][new_vector_file]

    load_vector(new_vector_file, glove, binary, lang)


def load_vector(file: str, glove: bool, binary: bool, lang: str):
    global vector_files
    global current_file
    global current_lang

    if str(file) in vector_files[lang]:
        current_file[lang] = str(file)
        current_lang = lang
        return

    current_file[lang] = str(file)
    current_lang = lang
    if not glove:
        current_vector = KeyedVectors.load_word2vec_format(file, binary=binary)
        vector_files[current_lang][current_file[lang]] = current_vector
        return

    if glove:
        tmp_file = get_tmpfile("glove2w2v_")
        glove2word2vec(file, tmp_file)
        current_vector = KeyedVectors.load_word2vec_format(tmp_file)
        vector_files[current_lang][current_file[lang]] = current_vector
        return
