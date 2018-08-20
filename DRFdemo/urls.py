"""DRFdemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
from users.views import UserViewset, UserlogoutViewset, UserlogsViewset, CmdbGroupViewset
from equipment.views import PcViewset, ServerViewset, PcExportView, ConnectServerView, NetworkEquipmentViewset, NetworkTopologyViewset

from dashboard.views import PcWeight
from users.views import MyJSONWebToken

from django.views.static import serve
from DRFdemo.settings import MEDIA_ROOT

router = DefaultRouter()
router.register(r'groups', CmdbGroupViewset, base_name='groups')
router.register(r'users',UserViewset,base_name='users')
router.register(r'pc', PcViewset, base_name='pc')
router.register(r'servers',ServerViewset, base_name='servers')
router.register(r'logout', UserlogoutViewset, base_name='logout')
router.register(r'logs', UserlogsViewset, base_name='logs')
router.register(r'networks', NetworkEquipmentViewset, base_name='networks')
router.register(r'topology', NetworkTopologyViewset, base_name='topology')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'docs/', include_docs_urls(title="API文档")),
    url(r'^', include(router.urls)),
    # JWT验证
    # url(r'^login/', obtain_jwt_token),
    url(r'^login/',MyJSONWebToken.as_view(),name="login"),
    url(r'^pcweight/', PcWeight.as_view(), name='pcweight'),
    url('^export/', PcExportView.as_view()),
    url(r'gateone/', ConnectServerView.as_view()),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

    # drf 自带的token授权登录，获取token需要向该地址post数据
    url(r'^api-token-auth/',views.obtain_auth_token)
]