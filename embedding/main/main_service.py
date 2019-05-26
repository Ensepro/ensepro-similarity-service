# -*- coding: utf-8 -*-

import json
from collections import deque

from flask import Flask, request, jsonify

from embedding.bert import bert_service
from embedding.word_embedding import word_embedding_service

app = Flask(__name__)

EMBEDDING = "EMBEDDING"
BERT = "BERT"

methods = deque([
    {"name": EMBEDDING, "service": word_embedding_service},
    {"name": BERT, "service": bert_service}
])


def current_service():
    return methods[0]["service"]


@app.route('/similarity/', methods=['GET', 'POST'])
def similarity_words():
    data = request.json
    word1 = data["word1"]
    word2 = data["word2"]

    score = current_service().similarity_words(word1, word2)

    return json.dumps({"score": float(str(score))})


@app.route('/n-similarity/', methods=['GET', 'POST'])
def similarity_lists():
    data = request.json
    words1 = data["words1"]
    words2 = data["words2"]

    result = current_service().similarity_lists(words1, words2)

    return json.dumps({
        "score": float(result["score"]),
        "words1": result["words1"],
        "words2": result["words2"]
    })


@app.route('/word-embedding/vector/update', methods=['GET', 'POST'])
def update_file():
    body = request.json
    headers = request.headers

    force_reload = headers.get("force-reload", "false") == "true"
    new_vector_file = body.get("vector", None)
    glove = body.get("glove", False)
    binary = body.get("binary", False)
    lang = body.get("lang", False)

    if not new_vector_file or not lang:
        return bad_request()

    word_embedding_service.change_vector(new_vector_file, glove, binary, lang, force_reload=force_reload)

    return jsonify(success=True)


@app.route('/similarity/method/switch', methods=['GET'])
def change_method():
    methods.rotate(1)

    return json.dumps({
        "changed_to": methods[0]["name"]
    })


@app.route('/similarity/method/current', methods=['GET'])
def current_method():
    return json.dumps({
        "method": methods[0]["name"]
    })


@app.route('/word-embedding/langs', methods=['GET'])
def get_langs():
    return json.dumps({
        "langs": word_embedding_service.list_langs()
    })


@app.route('/word-embedding/langs/order', methods=['GET', 'POST'])
def update_lang_order():
    body = request.json
    new_order = body["langs"]
    if not new_order:
        return bad_request()

    word_embedding_service.update_order(new_order)
    return get_langs()


@app.route('/word-embedding/vectors', methods=['GET'])
def list_vectors():
    result = {}
    for lang in word_embedding_service.vector_files:
        result[lang] = {}
        result[lang]["current"] = word_embedding_service.current_file[lang]
        result[lang]["vectors"] = [file for file in word_embedding_service.vector_files[lang]]
    return json.dumps(result)


def bad_request():
    from flask import abort
    return abort(400)
