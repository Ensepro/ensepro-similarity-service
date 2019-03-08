"""
@project ensepro-embedding-service
@since 08/03/2019
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import os
import sys

sys.path.append(os.path.abspath("../"))

from embedding.service import app, init

if __name__ == '__main__':
    print("loading vec file... ", end="")
    init()
    print("done")
    app.debug = False
    app.run(
        debug=False,
        port=8098
    )
