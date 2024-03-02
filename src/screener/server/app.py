import os
import json
import streamlit as st
import logging
import logging.config

with open(os.path.join(os.path.dirname(__file__), 'logging.json'), 'r', encoding='utf-8') as f:
    j = json.load(f)
    logging.config.dictConfig(j)

__logger = logging.getLogger(__name__)

