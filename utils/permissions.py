# -*- coding: utf-8 -*-

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "权限禁止!"

    # 系统级权限，非管理员的POST方法禁止，例如普通用户无法create操作
    def has_permission(self, request, view):
        group_obj = request.user.group
        if request.method != "POST" or group_obj.name == "管理员":
            return True

    # 对象级权限,普通用户只能对自己的资源进行修改、删除操作
    def has_object_permission(self, request, view, obj):
        group_obj = request.user.group
        if request.method in permissions.SAFE_METHODS or group_obj.name == "管理员":
            return True

        return obj.owner == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    除管理员外其他只读权限
    """
    message = "权限禁止!"
    def has_permission(self, request, view):
        group_obj = request.user.group
        if request.method in permissions.SAFE_METHODS or group_obj.name == "管理员":
            return True