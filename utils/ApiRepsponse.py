import json
from typing import Any
    
def send_error(msg: str, data: Any = '') -> str:
    return json.dumps({
        'status': False,
        'message': msg,
        'data': data
    })

def send_success(msg: str, data: Any = '') -> str:
    return json.dumps({
        'status': True,
        'message': msg,
        'data': data
    })