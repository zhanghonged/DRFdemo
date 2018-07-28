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

    class Meta:
        verbose_name = "Server"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hostname
