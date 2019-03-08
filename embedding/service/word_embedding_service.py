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
VEC_FILE = "C:\\_a\ensepro\\ensepro-core\\arquivos\\fasttext-s50-m2-sg0.vec"
BINARY = False
GLOVE = False


@app.route('/word-embedding/similarity/', methods=['GET'])
def analisarFrase():
    word1 = request.args.get('word1')
    word2 = request.args.get('word2')

    score = similarity_score(word1, word2)
    # print(word1, word2, score)
    return json.dumps({"score": float(str(score))})


def similarity_score(word1, word2):
    try:
        result = wv.similarity(word1, word2)
        return result
    except Exception as ex:
        # print("erro: ", ex)
        return 0


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
