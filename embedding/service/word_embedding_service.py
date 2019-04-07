"""
@project ensepro-embedding-service
@since 08/03/2019
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

import json

from flask import Flask
from flask import request
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import get_tmpfile

app = Flask(__name__)
wv = None
VEC_FILE = "C:\\Users\\alenc\Documents\\_projetos\\ensepro\\fasttext-s50-m2-sg0.vec"
BINARY = False
GLOVE = False


@app.route('/word-embedding/similarity/', methods=['GET'])
def similarity():
    word1 = request.args.get('word1')
    word2 = request.args.get('word2')

    try:
        score = wv.similarity(word1, word2)
    except Exception as ex:
        score = 0

    return json.dumps({"score": float(str(score))})


@app.route('/word-embedding/n-similarity/', methods=['GET'])
def n_similarity():
    words1 = request.args.getlist('word1')
    words2 = request.args.getlist('word2')

    try:
        score = wv.n_similarity(words1, words2)
    except Exception as ex:
        score = 0

    return json.dumps({"score": float(str(score))})


def init():
    global wv
    if not GLOVE:
        wv = KeyedVectors.load_word2vec_format(VEC_FILE, binary=BINARY)
        return

    if GLOVE:
        tmp_file = get_tmpfile("glove2w2v_")
        glove2word2vec(VEC_FILE, tmp_file)
        wv = KeyedVectors.load_word2vec_format(tmp_file)
        return
