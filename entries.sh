#!/bin/bash

curl -X POST --header 'Content-Type: application/json' -d '{ "title": "My first entry", "content": "This is my first blog entry"}' '127.0.0.1:5000/api/article'
curl -X POST --header 'Content-Type: application/json' -d '{ "title": "My second entry", "content": "This is my second blog entry"}' '127.0.0.1:5000/api/article'
curl -X POST --header 'Content-Type: application/json' -d '{ "title": "My third entry", "content": "This is my third blog entry"}' '127.0.0.1:5000/api/article'