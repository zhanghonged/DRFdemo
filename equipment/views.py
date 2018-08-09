from django.http import JsonResponse
from collections import OrderedDict

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import authentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from .serializers import PcSerializer,ServerDetailSerializer,ServerRegSerializer
from .models import Pc,Server
from utils.getmac import IP2MAC
from utils.connectserver import connect_server
import paramiko, time
from utils.gateone import auth

from .export import ExportMixin, PcResource

class Pcpagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class Serverpagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    # 重载PageNumberPagination类的get_paginated_response方法，让返回的数据增加page_size，前端分页需要用到
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('page_size',self.page_size),
            ('results', data)
        ]))

class PcViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Pc.objects.all()
    serializer_class = PcSerializer
    pagination_class = Pcpagination
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)


    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    search_fields = ('pcuser', 'ip','mac','cpu','memory','disk','display','department','note')
    ordering_fields = ('pcuser','ip')


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # result = {}
            # result['page_size'] = Pcpagination.page_size
            # result['data'] = serializer.data
            # return self.get_paginated_response(result)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
    pagination_class = Serverpagination

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
        id = instance.id
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
            cmd = 'python CMDBClient/main.py ' + str(id)
            print(cmd)
            stdin,stdout,stderr = ssh.exec_command(cmd)
            trans.close()
        return Response(serializer.data)


class PcExportView(ExportMixin,GenericAPIView):
    """
    PC导出excel功能，由于前端angular下载比较麻烦，取消认证
    """

    serializer_class = Pc
    queryset = Pc.objects.all()
    resource_class = PcResource
    filter_backends = (filters.SearchFilter,)
    search_fields = ('pcuser', 'ip', 'mac', 'cpu', 'memory', 'disk', 'display', 'department', 'note')


class ConnectServerView(APIView):
    """
    连接gateone实现web ssh
    """
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        gateone_server = 'https://192.168.1.32:443'
        api_key = 'MzAzOWE5YTIxYTk0NDQzOGIxNmJmNjRkMTM1MTk0MTJkM'
        secret = 'MjcyMmYwMzQ3ODVmNDM3M2JmZDlmY2U4ZmM1ZWY0ZmZmN'
        authobj = auth(api_key,secret)

        auth_info_and_server = {"url": gateone_server, "auth": authobj}
        return JsonResponse(auth_info_and_server)