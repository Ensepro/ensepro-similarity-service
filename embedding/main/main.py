"""
@project ensepro-embedding-service
@since 08/03/2019
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import os
import sys

sys.path.append(os.path.abspath("../"))

from embedding.service import app, load_vector

DEFAULT_VEC_FILE = "C:\\_a\\ensepro\\ensepro-core\\arquivos\\fasttext-s50-m2-sg0.vec"
DEFAULT_BINARY = False
DEFAULT_GLOVE = False

if __name__ == '__main__':
    print("loading vec file... ", end="")
    load_vector(DEFAULT_VEC_FILE, DEFAULT_GLOVE, DEFAULT_GLOVE)
    print("done")
    app.debug = False
    app.run(
        debug=False,
        port=8098
    )
