import json

import config


def get_thread_id_from_recipient_id(recipient_id: str) -> str | None:
    with open(config.MAPPING_JSON_FILE_PATH, 'r') as file:
        mapping_data = dict(json.loads(file.read()))
    thread_id = mapping_data['mappings'].get(recipient_id)
    return thread_id


def update_thread_id_from_recipient_id(recipient_id: str, thread_id: str) -> None:
    with open(config.MAPPING_JSON_FILE_PATH, 'w') as file:
        mapping_data = dict(json.loads(file.read()))
    mapping_data['mappings'].update({recipient_id: thread_id})
    return None
