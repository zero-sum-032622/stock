import os
from fastapi import FastAPI
import logging
import json
import logging.config

print(os.path.dirname(__file__))
with open(os.path.join(os.path.dirname(__file__), 'logging.json'), 'r', encoding='utf-8') as f:
    j = json.load(f)
    logging.config.dictConfig(j)
    print(j)


app = FastAPI()

@app.get("/")
async def root():
    logging.getLogger(__name__).debug('Hello world')
    return { "message": "Hello World!!" }