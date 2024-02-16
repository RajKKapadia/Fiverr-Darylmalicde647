import os
import tempfile
import json

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

FB_PAGE_ACCESS_TOKEN = os.getenv('FB_PAGE_ACCESS_TOKEN')
VERIFY_TOEKN = os.getenv('VERIFY_TOEKN')

ERROR_MESSAGE = 'We are facing an issue at this momemnt, please try after sometime.'

MAPPING_JSON_FILE_PATH = os.path.join(
    tempfile.gettempdir(),
    'mapping_file.json'
)

with open(MAPPING_JSON_FILE_PATH, 'w+') as file:
    print(json.dumps({'mappings': {}}))
    file.write(json.dumps({'mappings': {'key': 'value'}}))
