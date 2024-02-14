import openai

import config

openai.api_key = config.OPENAI_API_KEY


def chat_completion(messages: list[dict]) -> str:
    try:
        completion = openai.chat.completions.create(
            model=config.GPT_MODEL,
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        print('Error at chat_completion...')
        print(e)
        return config.ERROR_MESSAGE
