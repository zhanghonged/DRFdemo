# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Pc, Server

class PcSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(max_length=32,required=True,
                               validators=[UniqueValidator(queryset=Pc.objects.all(),message="IP已存在")]
                               )
    class Meta:
        model = Pc
        fields = "__all__"

class ServerDetailSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length = 32, style={'input_type':'password'},label='密码')
    # ip = serializers.CharField(max_length=32,required=True,
    #                            validators=[UniqueValidator(queryset=Server.objects.all(),message='IP已存在')])
    password = serializers.CharField(max_length=32, write_only=True, label='密码')
    class Meta:
        model = Server
        fields = "__all__"

class ServerRegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True,max_length=32, style={'input_type': 'password'}, write_only=True, label='密码')
    ip = serializers.CharField(max_length=32, required=True,
                               validators=[UniqueValidator(queryset=Server.objects.all(), message='IP已存在')])
    class Meta:
        model = Server
        fields = ("ip","port","username","password","tag")