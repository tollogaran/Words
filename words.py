# -*- coding: utf-8 -*-
# Diccionario
from flask import Flask, request, render_template, jsonify
import requests
import logging

# "/home"
# "/word/<word>"

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/word/<word>")
def words(word):
    params = get_params_for_word(word)
    return render_template("word.html", **params)

@app.route("/api/word/<word>")
def api_words(word):
    params = get_params_for_word(word)
    return render_template("word.html", **params)

def get_params_for_word(word):
    headers = {
    "app_id": "a781b5de",
    "app_key": "e6c86d03a49ff04996a341ddc2a0e95c"
    }

    response = requests.get("https://od-api.oxforddictionaries.com:443/api/v1/entries/es/" +
    word.lower(), headers=headers)

    if response.status_code == 200:
        response_dict = response.json()
        results = response_dict["results"][0]
        lexicalEntries = results["lexicalEntries"]
        definitions = []
        for le in lexicalEntries:
            entries = le["entries"]
            for entry in entries:
                senses = entry["senses"]
                for sense in senses:
                    defs = sense["definitions"]
                    for definition in defs:
                        definitions.append(definition)
        #definitions = [le["entries"]["senses"][0] for le in lexicalEntries]

    else:
        definitions = []
        print("ERROR!!")
    params = {
        "word": word,
        "definitions": definitions
    }
    return params

if __name__ == "__main__":
    app.run(debug=True)
