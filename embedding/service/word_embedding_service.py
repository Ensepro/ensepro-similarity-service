"""
@project ensepro-embedding-service
@since 08/03/2019
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json
import re

from flask import Flask, request, jsonify
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import get_tmpfile

vector_files = {}
current_file = None
app = Flask(__name__)


@app.route('/word-embedding/similarity/', methods=['GET', 'POST'])
def similarity():
    data = request.json
    word1 = data["word1"]
    word2 = data["word2"]

    try:
        score = vector_files[current_file].similarity(word1, word2)
    except Exception as ex:
        score = 0

    return json.dumps({"score": float(str(score))})


@app.route('/word-embedding/n-similarity/', methods=['GET', 'POST'])
def n_similarity():
    data = request.json
    words1 = data["words1"]
    words2 = data["words2"]

    score = 0
    count = 0
    while words2 and count < 10:
        count += 1
        try:
            score = vector_files[current_file].n_similarity(words1, words2)
            break
        except KeyError as ex:
            words2.remove(re.search("'(.*)'", str(ex)).group(1))
            continue
        except Exception as ex:
            break

    return json.dumps({"score": float(str(score))})


@app.route('/word-embedding/vector/update', methods=['GET', 'POST'])
def update_file():
    body = request.json
    headers = request.headers

    force_reload = headers.get("force-reload", "false")
    new_vector_file = body.get("vector", None)
    glove = body.get("glove", False)
    binary = body.get("binary", False)

    if not new_vector_file:
        from flask import abort
        return abort(400)

    global vector_files
    global current_file

    if force_reload == "true":
        del vector_files[current_file]

    load_vector(new_vector_file, glove, binary)

    return jsonify(success=True)


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
