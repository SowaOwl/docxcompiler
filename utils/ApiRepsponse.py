import json
    
def sendError(msg, data=''):
    return json.dumps({
        'status': False,
        'message': msg,
        'data': data
    })

def sendSuccess(msg, data=''):
    return json.dumps({
        'status': True,
        'message': msg,
        'data': data
    })