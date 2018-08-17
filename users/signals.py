# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from crequest.middleware import CrequestMiddleware
from users.views import login_done, logout_done
from users.views import CustomBackend, UserlogoutViewset
from equipment.views import ConnectServerView
from equipment.views import connect_done

from users.models import UserProfile, UserLogs
from equipment.models import Pc, Server, NetworkEquipment, NetworkTopology
from equipment.export import ExportMixin, export_done
import time

def createlogs(username,action):
    action_time = time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        UserLogs.objects.create(username= username, action = action)
    except Exception as e:
        print(str(e))
    else:
        print(username + action + "时间" + action_time)

# 添加、编辑用户成功
@receiver(post_save,sender=UserProfile)
def adduser(sender,instance=None,created=False,**kwargs):
    current_request = CrequestMiddleware.get_request()
    if created:
        # 用户密码加密此处注销，有viewset来实现
        # password = instance.password
        # instance.set_password(password)
        # instance.save()

        action = "添加用户:" + instance.username
        createlogs(username=current_request.user.username,action=action)
    else:
        action = "编辑用户:" + instance.username
        createlogs(username=current_request.user.username, action=action)

# 删除用户成功
@receiver(post_delete, sender=UserProfile)
def deluser(sender,instance=None,**kwargs):
    current_request = CrequestMiddleware.get_request()
    action = "删除用户:" + instance.username
    createlogs(username=current_request.user.username,action=action)

# 用户登录成功信号量
@receiver(login_done, sender=CustomBackend)
def sign(sender, **kwargs):
    createlogs(kwargs['name'],kwargs['content'])

# 用户退出成功信号量
@receiver(logout_done, sender=UserlogoutViewset)
def sigout(sender,**kwargs):
    createlogs(kwargs['name'], kwargs['content'])

# 添加编辑PC
@receiver(post_save,sender=Pc)
def addpc(sender, instance=None,created=False,**kwargs):
    current_request = CrequestMiddleware.get_request()
    if created:
        action = '添加PC:' + instance.ip
        createlogs(username=current_request.user.username,action=action)
    else:
        action = '编辑PC:' + instance.ip
        createlogs(username=current_request.user.username,action=action)


# 删除PC
@receiver(post_delete, sender=Pc)
def delpc(sender, instance=None, **kwargs):
    current_request = CrequestMiddleware.get_request()
    action = '删除PC:' + instance.ip
    createlogs(username=current_request.user.username,action=action)

# 添加编辑Server
@receiver(post_save,sender=Server)
def addserver(sender, instance=None,created=False,**kwargs):
    current_request = CrequestMiddleware.get_request()
    if created:
        action = '添加Server:' + instance.ip
        createlogs(username=current_request.user.username,action=action)
    else:
        action = '更新Server:' + instance.ip
        createlogs(username=current_request.user.username,action=action)

# 连接Server
@receiver(connect_done, sender=ConnectServerView)
def connectserver(sender, **kwargs):
    current_request = CrequestMiddleware.get_request()
    createlogs(username=current_request.user.username,action=kwargs['content'])

# 导出PC表
@receiver(export_done, sender=ExportMixin)
def exportpc(sender, **kwargs):
    createlogs(username=kwargs['user'], action=kwargs['content'])

# 添加编辑网络设备
@receiver(post_save,sender=NetworkEquipment)
def addnetwork(sender, instance=None, created=False, **kwargs):
    current_request = CrequestMiddleware.get_request()
    if created:
        action = '添加网络设备:' + instance.eq_ip
    else:
        action = '编辑网络设备:' + instance.eq_ip
    createlogs(username=current_request.user.username,action=action)

# 删除网络设备
@receiver(post_delete,sender=NetworkEquipment)
def delnetwork(sender, instance=None, **kwargs):
    current_request = CrequestMiddleware.get_request()
    action = '删除网络设备:' + instance.eq_ip
    createlogs(username=current_request.user.username,action=action)

# 添加网络拓扑图
@receiver(post_save, sender=NetworkTopology)
def addtopology(sender, instance=None, created=False, **kwargs):
    current_request = CrequestMiddleware.get_request()
    if created:
        url = str(instance.url)
        img = url.rsplit('/',1)[1]
        action = '添加拓扑图' + img
        createlogs(username=current_request.user.username,action=action)