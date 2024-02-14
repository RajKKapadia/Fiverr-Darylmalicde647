from datetime import datetime
import threading

from flask import Flask, request

from database_api import create_user, update_messages, get_user
from utils import generate_messages
from openai_api import chat_completion
from fb_graph_api import send_message_to_fb_messenger
import config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return 'OK', 200


@app.route('/facebook', methods=['GET'])
def facebook_get():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    print(config.VERIFY_TOEKN)
    try:
        if mode == 'subscribe' and token == config.VERIFY_TOEKN:
            print('WEBHOOK_VERIFIED')
            return challenge
        else:
            return 403
    except:
        return 403


@app.route('/facebook', methods=['POST'])
def facebook_post():
    try:
        print('A new Facebook Messenger request...')
        body = request.get_json()
        recipient_id = body['entry'][0]['messaging'][0]['sender']['id']
        query = body['entry'][0]['messaging'][0]['message']['text']
        user = get_user(recipient_id)
        if user:
            messages = generate_messages(user['messages'][-3:], query)
        else:
            messages = generate_messages([], query)
        print(query)
        print(recipient_id)
        print(messages)
        message_text = chat_completion(messages)
        print(message_text)
        if user:
            update_messages(recipient_id, query, recipient_id,
                            user['messageCount'])
        else:
            message = {
                'query': query,
                'response': recipient_id,
                'createdAt': datetime.now().strftime('%d/%m/%Y, %H:%M')
            }
            user = {
                'senderId': recipient_id,
                'messages': [message],
                'messageCount': 1,
                'mobile': '',
                'channel': 'WhatsApp',
                'is_paid': False,
                'created_at': datetime.now().strftime('%d/%m/%Y, %H:%M')
            }
            create_user(user)
        threading.Thread(target=send_message_to_fb_messenger,
                         args=(recipient_id, message_text)).start()
        print('Request success.')
    except:
        print('Request failed.')
        pass
    return 'OK', 200
