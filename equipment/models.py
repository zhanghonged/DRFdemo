import datetime

from django.db import models

# Create your models here.

class Pc(models.Model):
    pcuser = models.CharField(max_length=32,verbose_name='使用者')
    ip = models.CharField(max_length=32,verbose_name='IP地址')
    mac = models.CharField(max_length=32,verbose_name='MAC地址',blank=True,null=True)
    cpu = models.CharField(max_length=32,verbose_name='CPU信息',blank=True,null=True)
    disk = models.CharField(max_length=32,verbose_name='硬盘',blank=True,null=True)
    memory = models.CharField(max_length=32, verbose_name='内存',blank=True,null=True)
    display = models.CharField(max_length=32, verbose_name='显示器',blank=True,null=True)
    department = models.CharField(max_length=32,verbose_name='部门',blank=True,null=True)
    note = models.CharField(max_length=32,verbose_name='备注',blank=True,null=True)
    class Meta:
        verbose_name = "PC"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pcuser

class Server(models.Model):

    ip = models.CharField(max_length=32, verbose_name='ip地址')
    port = models.CharField(max_length=16, verbose_name='端口')
    username = models.CharField(max_length = 32, verbose_name='用户名')
    password = models.CharField(max_length = 32, verbose_name='密码')
    status = models.CharField(max_length=32, verbose_name='连接状态', blank=True, null=True)
    sys_type = models.CharField(max_length=32, verbose_name='系统类型',blank=True,null=True)
    sys_version = models.CharField(max_length=32, verbose_name='系统版本',blank=True,null=True)
    cpu = models.CharField(max_length=32, verbose_name='CPU信息',blank=True,null=True)
    disk = models.CharField(max_length=32, verbose_name='硬盘',blank=True,null=True)
    memory = models.CharField(max_length=32, verbose_name='内存',blank=True,null=True)
    hostname = models.CharField(max_length = 32, verbose_name='主机名',blank=True,null=True)
    mac = models.CharField(max_length=32, verbose_name='MAC地址',blank=True,null=True)
    tag = models.CharField(max_length=32, verbose_name='标记', blank=True,null=True)

    class Meta:
        verbose_name = "Server"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hostname

class NetworkEquipment(models.Model):
    type_choices = (
        (1,'路由器'),
        (2,'交换机'),
        (3,'其他设备')
    )
    eq_type = models.CharField(max_length=16,choices=type_choices, verbose_name='设备类型')
    eq_ip = models.CharField(max_length=32, unique=True, verbose_name='设备IP')
    eq_brand = models.CharField(max_length=32 ,blank=True, null=True, verbose_name='设备品牌')
    eq_username = models.CharField(max_length=16, blank=True, null=True, verbose_name='设备登录名')
    eq_password = models.CharField(max_length=32, blank=True, null=True, verbose_name='设备登录密码')
    eq_location = models.CharField(max_length=32, blank=True, null=True, verbose_name='位置')
    eq_wifiname = models.CharField(max_length=32, blank=True, null=True, verbose_name='WIFI名')
    eq_wifipwd = models.CharField(max_length=32, blank=True, null=True, verbose_name='WIFI密码')
    eq_theuser = models.CharField(max_length=32, blank=True, null=True, verbose_name='使用者')
    eq_broadbandname = models.CharField(max_length=16, blank=True, null=True, verbose_name='宽带拨号名')
    eq_broadbandpwd = models.CharField(max_length=16 ,blank=True, null=True, verbose_name='宽带拨号密码')
    eq_mobile = models.CharField(max_length=16 ,blank=True, null=True, verbose_name='绑定电话')
    eq_note = models.CharField(max_length=32, blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.eq_ip

class NetworkTopology(models.Model):
    url = models.ImageField(upload_to='img/network/',verbose_name='拓扑图')
    add_time = models.DateTimeField(default=datetime.datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name= '拓扑图'
        verbose_name_plural = verbose_name