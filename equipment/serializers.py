# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Pc, Server, NetworkEquipment, NetworkTopology

class PcSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(max_length=32,required=True,
                               validators=[UniqueValidator(queryset=Pc.objects.all(),message="IP已存在")]
                               )
    ownername = serializers.CharField(source="owner.username",read_only=True)
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

class NetworkEquipmentSerializer(serializers.ModelSerializer):
    eq_ip = serializers.CharField(max_length=32, required=True,
                               validators=[UniqueValidator(queryset=NetworkEquipment.objects.all(),message='设备已存在')],label='设备IP')
    # eq_password = serializers.CharField(max_length=32, style={'input_type':'password'},label='设备登录密码')

    class Meta:
        model = NetworkEquipment
        fields = "__all__"

class NetworkTopologySerializer(serializers.ModelSerializer):
    url = serializers.ImageField()
    class Meta:
        model = NetworkTopology
        fields = "__all__"