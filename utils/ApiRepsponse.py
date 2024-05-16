import json
    
def sendError(msg: str, data=''):
    return json.dumps({
        'status': False,
        'message': msg,
        'data': data
    })

def sendSuccess(msg: str, data=''):
    return json.dumps({
        'status': True,
        'message': msg,
        'data': data
    })