"""
@project ensepro-embedding-service
@since 08/03/2019
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
import os
import sys

sys.path.append(os.path.abspath("../"))

from embedding.main.main_service import app

if __name__ == '__main__':
    app.debug = False
    app.run(
        host='0.0.0.0',
        debug=False,
        port=8098
    )
