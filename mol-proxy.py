#!/usr/bin/env python3
"""
转发并保存发送给osra的图片
"""
import os
import requests
from flask import Flask, request, Response
import time
from utils.content_type import content_types

OCR_API_URL = 'http://127.0.0.1:5000/image2ctab'
SAVE_DIR = 'images'
if not os.path.isdir(SAVE_DIR):
    os.mkdir(SAVE_DIR)
app = Flask(__name__)


@app.route('/image2ctab', methods=['POST', 'OPTIONS'])
def save_log():
    print(request.headers)
    data = request.data
    if data:
        f_type = content_types.get(request.headers.get('Content-Type', 'x'), 'bin')
        with open('{}/{}.{}'.format(SAVE_DIR, int(time.time()), f_type), 'wb') as f:
            f.write(data)
    headers = dict()
    for name, value in request.headers:
        if not value or name == 'Cache-Control':
            continue
        headers[name] = value
    method = request.method

    r = requests.request(method, OCR_API_URL, data=data, stream=True, headers=headers)
    resp_headers = []
    for name, value in r.headers.items():
        # if name.lower() in ('content-length', 'connection', 'content-encoding'):
        #     continue
        resp_headers.append((name, value))

    print('resp_headers', resp_headers)
    return Response(r, status=r.status_code, headers=resp_headers)


app.run(port=17005, debug=False)
