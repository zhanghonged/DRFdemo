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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip,port=port,username=user,password=password,timeout=1)

    except Exception as e:
        result['data'] = str(e)
    else:
        result['status'] = 'success'
        result['data'] = ssh
    finally:
        return result