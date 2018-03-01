#!/usr/bin/env python3

import flask
import requests
import json
import urllib

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

@app.route('/')
def serveIndex():
    return render_template('index.html')
@app.route('/search/')
def search():
    # search_term = "grand canyon"

    search_term = request.args.get('search_term')

    params={"fo": "json",
            "c": "1",
            "q": urllib.parse.quote_plus(search_term),
            "at": "results"}
    params_string = [ key+"="+val for key, val in params.items() ]
    page="https://www.loc.gov/photos/?"+ "&".join(params_string)

    r = requests.get(page)

    print(json.dumps(r.json()["results"][0],
                     indent=2))

    image_url = None
    try:
        image_url = r.json()["results"][0]["image_url"][-1]
    except (KeyError, IndexError):
        return ("No image url found")
    else:
        return ("<img src=\"http:"+image_url+"\">")
