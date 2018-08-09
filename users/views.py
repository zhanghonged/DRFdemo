from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import filters
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView, jwt_response_payload_handler

from .permissions import IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler, JSONWebTokenSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserRegSerializer, UserDetailSerializer, UserlogoutSerializer, UserLogsSerializer
from .models import UserLogs
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.base_user import make_password


from django.dispatch import Signal
import time

#定义信号，在用户登录成功后发出
login_done = Signal(providing_args=['name','content','time'])

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                # 登录验证成功后发出上面定义的信号
                login_done.send(CustomBackend, name=user.username, content='登录成功',time=time.strftime("%Y-%m-%d %H:%M:%S"))
                return user
        except Exception as e:
            return None


class Logpagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

class UserViewset(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    queryset = User.objects.all()
    # 这里验证身份还加上了DRF自带的Session验证，主要是方便我们使用DRF自带WebAPI界面进行测试
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = Logpagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('username', 'gender','mobile')

    def get_serializer_class(self):
        """
        根据self.action来判断，action是mixins提供的功能
        注册动作使用UserRegSerializer
        其他动作使用UserDetailSerializer
        """
        if self.action == 'create':
            return UserRegSerializer
        else:
            return UserDetailSerializer


    def get_permissions(self):
        """
        除了注册用户外，其他动作都需要权限验证:
        """
        if self.action == "create":
            return []
        else:
            return [permissions.IsAuthenticated(),]


    def create(self, request, *args, **kwargs):
        """
        重载CreateModelMixin的create方法，用户注册完成后返回jwt-token
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        重写CreateModelMixin的perform_create方法，对用户提交的密码加密处理，然后在保存
        调用django自带的make_password方法来处理
        """
        password = make_password(serializer.validated_data['password'])
        serializer.validated_data["password"] = password
        return serializer.save()

    # def get_object(self):
    #     return self.request.user


# 用户退出记录log使用
# 原本用户退出前台自己删除token就行，不用通知后台，但这里后台需要记录log，因此多加一个请求。
# 信号量方法实现
logout_done = Signal(providing_args=['name','content','time'])

class UserlogoutViewset(mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UserlogoutSerializer

    # 用户退出只能携带自己的ID
    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)

    def retrieve(self, request, *args, **kwargs):
        """
        重载RetrieveModelMixin的retrieve方法，使发出退出信号量
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logout_done.send(UserlogoutViewset, name= instance.username, content="退出成功", time=time.strftime("%Y-%m-%d %H:%M:%S"))
        return Response(serializer.data)




class UserlogsViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication,authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserLogsSerializer
    pagination_class = Logpagination
    queryset = UserLogs.objects.all()
    filter_backends = (filters.SearchFilter,filters.OrderingFilter)
    search_fields = ('username', 'action', 'action_time')
    ordering_fields = ('action_time',)


class MyJSONWebToken(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    # 重载JSONWebTokenAPIView 的post方法，让返回的数据增加user信息
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_dict={
                'token':token,
                'user':{
                    'id':user.id,
                    'name':user.username
                }

            }
            response = Response(response_dict)
            if api_settings.JWT_AUTH_COOKIE:
                from datetime import datetime
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response