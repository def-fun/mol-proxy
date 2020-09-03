#!/usr/bin/env python3
"""
http proxy
"""
from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.before_request
def proxy():
    headers = {h[0]: h[1] for h in request.headers}
    url = request.url
    headers['x-token'] = '***'
    return requests.request(request.method, url, data=request.json, headers=headers).content


if __name__ == "__main__":
    app.run()
