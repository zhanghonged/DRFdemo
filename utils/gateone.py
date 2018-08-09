# -*- coding: utf-8 -*-
import hashlib
import hmac

import time


def create_signature(secret,*parts):
    '''
    此方法主要用来加密
    '''
    hash = hmac.new(secret, digestmod=hashlib.sha1)
    for part in parts:
        hash.update(part)
    return hash.hexdigest()

def auth(api_key,secret):
    """
    返回连接gateone校验信息
    """
    api_key = api_key.encode('utf8')
    secret = secret.encode('utf8')

    authobj = {
        'api_key': api_key,
        'upn': "gateone".encode('utf8'),
        'timestamp': str(int(time.time() * 1000)).encode('utf8'),
        'signature_method': 'HMAC-SHA1',
        'api_version': '1.0'
    }
    authobj['signature'] = create_signature(secret, authobj['api_key'], authobj['upn'], authobj['timestamp'])
    authobj['api_key'] = authobj['api_key'].decode('utf8')
    authobj['upn'] = authobj['upn'].decode('utf8')
    authobj['timestamp'] = authobj['timestamp'].decode('utf8')

    return authobj
