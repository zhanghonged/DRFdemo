# -*- coding: utf-8 -*-
import time
from django.dispatch import Signal
from django.http import HttpResponse
from django_validator.decorators import GET
from import_export import resources
from .models import Pc


def attachment_response(export_data, filename='download.xls', content_type='application/vnd.ms-excel'):
    try:
        response = HttpResponse(export_data, content_type=content_type)
    except TypeError:
        response = HttpResponse(export_data, mimetype=content_type)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response


#定义导出PC表信号
export_done = Signal(providing_args=['user','content','time'])
class ExportMixin:
    @GET('filename', type='string', default='pc.xls')
    @GET('format', type='string', default='xls')
    @GET('empty', type='bool', default=False)
    def get(self, request, format, filename, empty):
        queryset = None
        if not empty:
            queryset = self.filter_queryset(self.get_queryset())
        resourse = self.resource_class()
        export_data = resourse.export(queryset, empty)

        # 发送导出PC表的信号
        user = request._request.GET.get('name')
        export_done.send(ExportMixin, user=user,content='导出PC表', time=time.strftime("%Y-%m-%d %H:%M:%S"))
        return attachment_response(getattr(export_data, format), filename=filename)



class PcResource(resources.ModelResource):
    def get_export_headers(self):
        return ['ID','用户','IP','MAC','CPU','硬盘','内存','显示器','部门','备注']

    class Meta:
        model = Pc