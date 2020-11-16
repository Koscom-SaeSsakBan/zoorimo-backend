from rest_framework.decorators import action
from rest_framework.permissions import BasePermission

from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from zoorimo.app.models import User, Zoorimo
from zoorimo.app.serializer import UserInfoSerializer, SignInSerializer, SignUpSerializer, ZoorimoInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    class UserPermissionClass(BasePermission):
        def has_permission(self, request, view):
            return True

        def has_object_permission(self, request, view, obj):
            return request.user == obj

    @action(methods=['POST'], detail=False)
    def signin(self, request, *args, **kwargs):
        s = SignInSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        u = User.objects.get(username=request.data.get('username'))
        return Response(UserInfoSerializer(instance=u).data, status.HTTP_200_OK)

    @action(methods=['POST'], detail=False)
    def signup(self, request, *args, **kwargs):
        s = SignUpSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        u = s.save()
        z = Zoorimo()
        z.user = u
        z.size = 10
        z.save()
        return Response(UserInfoSerializer(instance=u).data, status.HTTP_201_CREATED)

    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.AllowAny]


class ZoorimoViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Zoorimo.objects.filter(user=self.kwargs.get('user_pk'))

    serializer_class = ZoorimoInfoSerializer
