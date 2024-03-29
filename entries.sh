#!/bin/bash

set -ex

PORT=${PORT:-$(grep "app.run" app.py | sed -r s'/.*port=([0-9]{1,5})\)/\1/')}

curl -X POST \
    --header 'Content-Type: application/json' \
    -d '{ "title": "My first entry", "content": "This is my first blog entry"}' \
    "http://127.0.0.1:${PORT}/api/article"
curl -X POST \
    --header 'Content-Type: application/json' \
    -d '{ "title": "My second entry", "content": "This is my second blog entry"}' \
    "http://127.0.0.1:${PORT}/api/article"

curl -X POST \
    --header 'Content-Type: application/json' \
    -d '{ "title": "My third entry", "content": "This is my third blog entry"}' \
    "http://127.0.0.1:${PORT}/api/article"


curl --header 'Content-Type: application/json' "http://127.0.0.1:${PORT}/api/article"