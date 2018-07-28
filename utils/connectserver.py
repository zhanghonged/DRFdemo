# -*- coding: utf-8 -*-
import paramiko
def connect_server(ip,port,user,password):
    '''
    通过paramiko检测服务器是否可以连通，是的话返回连接对象
    :param ip:
    :param port:
    :param user:
    :param password:
    :return:返回连接对象
    '''
    result = {'status':'error','data':''}
    try:
        trans = paramiko.Transport(ip,port)
        trans.connect(username = user, password = password)
    except Exception as e:
        result['data'] = str(e)
    else:
        result['status'] = 'success'
        result['data'] = trans
    finally:
        return result