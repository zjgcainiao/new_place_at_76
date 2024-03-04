
import pathlib
import textwrap
import os
from decouple import config
import google.generativeai as genai
import logging
from IPython.display import display
from IPython.display import Markdown

logger = logging.getLogger('external_api')


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


GOOGLE_GEMINI_API_KEY = config('GOOGLE_GEMINI_API_KEY', default=None)
if not GOOGLE_GEMINI_API_KEY:
    raise Exception('GOOGLE_GEMINI_API_KEY NOT set')
else:
    logger.info('GOOGLE_GEMINI_API_KEY is set')
    genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
