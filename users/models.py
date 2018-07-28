from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import datetime

class UserProfile(AbstractUser): #继承AbstractUser
    """
    用户表
    """
    GENDER_CHOICES = (
        ("male", u"男"),
        ("female",u"女")
    )
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="female", verbose_name="性别")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="电话")
    email = models.EmailField(max_length=100, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class UserLogs(models.Model):
    """
    用户操作日志
    """
    username = models.CharField(max_length=30, verbose_name='用户名')
    action = models.CharField(max_length=30, verbose_name='动作')
    action_time = models.DateTimeField(default=datetime.datetime.now,verbose_name='操作时间')