# -*- coding: utf-8 -*-
import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

from DRFdemo.settings import REGEX_EMAIL
from .models import UserLogs, CmdbGroup
from equipment.serializers import PcSerializer


class CmdbGroupSerializer(serializers.ModelSerializer):
    """
    用户组序列化类
    """
    class Meta:
        model = CmdbGroup
        fields = "__all__"

class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化类
    """
    password = serializers.CharField(style={'input_type': 'password'}, label="密码", write_only=True,
                                     help_text="string密码")
    group = serializers.PrimaryKeyRelatedField(required=True, queryset=CmdbGroup.objects.all())
    group_display = serializers.CharField(source="group.name", read_only=True)

    # pcs = PcSerializer(many=True)

    class Meta:
        model = User
        fields = ("id","username","password","gender","birthday","mobile","email","group","group_display")

class UserRegSerializer(serializers.ModelSerializer):
    """
    用户注册序列化类
    """
    username = serializers.CharField(required=True,
                                     allow_blank=False,
                                     label="用户名",
                                     validators=[UniqueValidator(queryset=User.objects.all(),message="用户已存在")],
                                     help_text="string用户名")

    password = serializers.CharField(style={'input_type':'password'},label="密码",write_only=True,help_text="string密码")

    group = serializers.PrimaryKeyRelatedField(required=True, queryset=CmdbGroup.objects.all())

    def validate_username(self, username):
        """
        验证用户名是邮箱规则
        :param username:
        :return:
        """
        if not re.match(REGEX_EMAIL,username):
            raise serializers.ValidationError("请输入邮箱格式用户名")

        return username

    # 此功能这里注销，由信号量或viewset中来实现
    # def create(self, validated_data):
    #     """
    #     重载create函数,使密码入库
    #     :param validated_data:
    #     :return:
    #     """
    #     user = super(UserRegSerializer,self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate(self, attrs):
        """
        # attrs是字段validate之后返回的总的dict
	    # 注册时提交的username字段是邮箱，这里把email字段也加上
        """
        attrs["email"] = attrs["username"]
        return attrs

    class Meta:
        model = User
        fields = ("username","password","group")

class UserlogoutSerializer(serializers.ModelSerializer):
    """
    用户登出
    """
    class Meta:
        model = User
        fields = ("username",)

class UserLogsSerializer(serializers.ModelSerializer):
    """
    用户操作日志
    """
    class Meta:
        model = UserLogs
        fields = "__all__"