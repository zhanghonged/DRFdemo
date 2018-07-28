from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from .serializers import PcSerializer,ServerDetailSerializer,ServerRegSerializer
from .models import Pc,Server
from utils.getmac import IP2MAC
from utils.connectserver import connect_server
import paramiko, time

class Pcpagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class PcViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Pc.objects.all()
    serializer_class = PcSerializer
    pagination_class = Pcpagination
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)


    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    search_fields = ('pcuser', 'ip')
    ordering_fields = ('pcuser','ip')


    def perform_create(self, serializer):
        """
        重载CreateModelMixin的 perform_create 方法，使通过ip自动获取到mac地址
        """
        ip = serializer.validated_data['ip']
        g = IP2MAC()
        mac = g.getMac(ip)
        serializer.validated_data['mac'] = mac
        serializer.save()


    def perform_update(self, serializer):
        """
        重载UpdateModelMixin perform_create 方法，使通过ip自动获取到mac地址
        """
        ip = serializer.validated_data['ip']
        g = IP2MAC()
        mac = g.getMac(ip)
        serializer.validated_data['mac'] = mac
        serializer.save()

class ServerViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    queryset = Server.objects.all()
    # serializer_class = ServerSerializer
    pagination_class = Pcpagination
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.SearchFilter, )
    search_fields = ('ip','username')

    def get_serializer_class(self):
        if self.action == "create":
            return ServerRegSerializer
        else:
            return ServerDetailSerializer

    def perform_create(self, serializer):
        """
        重载CreateModelMixin的 perform_create 方法，通过paramiko获取服务器信息并入库
        """
        ip = serializer.validated_data['ip']
        port = serializer.validated_data['port']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # 连接远程主机
        connect = connect_server(ip,int(port),username,password)
        if connect['status'] == 'success':
            trans = connect['data']
            # 用于文件上传和下载的sftp服务
            sftp = paramiko.SFTPClient.from_transport(trans)
            # 远程执行命令服务
            ssh = paramiko.SSHClient()
            ssh._transport = trans
            # 创建目录
            stdin,stdout,stderr = ssh.exec_command('mkdir CMDBClient')
            time.sleep(1)
            # 上传文件
            sftp.put('utils/sftpDir/getData.py','CMDBClient/getData.py')
            sftp.put('utils/sftpDir/sendData.py', 'CMDBClient/sendData.py')
            sftp.put('utils/sftpDir/getJwt.py', 'CMDBClient/getJwt.py')
            sftp.put('utils/sftpDir/main.py', 'CMDBClient/main.py')
            # 这里不自动调用脚本，改为手动调用
            # stdin,stdout,stderr = ssh.exec_command('python CMDBClient/main.py')
            trans.close()
            # 连接成功状态记录到数据库
            status = True
        else:
            status = False
        serializer.validated_data['status'] = status
        serializer.save()

    def retrieve(self, request, *args, **kwargs):
        """
        重载RetrieveModelMixin的retrieve方法，触发远程调用server脚本
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        ip = instance.ip
        port = instance.port
        username = instance.username
        password = instance.password
        # 连接远程主机
        connect = connect_server(ip,int(port),username,password)
        if connect['status'] == 'success':
            trans = connect['data']
            # 远程执行命令服务
            ssh = paramiko.SSHClient()
            ssh._transport = trans
            # 调用客户端脚本，脚本获取配置后通过patch方法更新server配置信息
            stdin,stdout,stderr = ssh.exec_command('python CMDBClient/main.py')
            trans.close()
        return Response(serializer.data)