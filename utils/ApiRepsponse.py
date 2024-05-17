import json
from typing import Any
    
def sendError(msg: str, data: Any =' ') -> str:
    return json.dumps({
        'status': False,
        'message': msg,
        'data': data
    })

def sendSuccess(msg: str, data: Any ='') -> str:
    return json.dumps({
        'status': True,
        'message': msg,
        'data': data
    })