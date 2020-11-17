from django.views import View
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission

from rest_framework import viewsets, status, serializers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from zoorimo.app.models import User, Zoorimo, Quiz, Kospi, Stock
from zoorimo.app.serializer import UserInfoSerializer, SignInSerializer, SignUpSerializer, ZoorimoInfoSerializer, \
    QuizInfoSerializer, KospiInfoSerializer

import requests

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
        z.status = 0
        z.save()
        return Response(UserInfoSerializer(instance=u).data, status.HTTP_201_CREATED)

    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.AllowAny]



class ZoorimoViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Zoorimo.objects.filter(user=self.kwargs.get('user_pk'))

    serializer_class = ZoorimoInfoSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizInfoSerializer


class QuizTrueViewSet(APIView):
    def get(self, request, user_pk, *args, **kwargs):
        zoorimo = Zoorimo.objects.filter(user_id=user_pk).first()
        zoorimo.size += 1
        print(zoorimo.__dict__)
        u = zoorimo.save()

        return Response(ZoorimoInfoSerializer(instance=zoorimo).data, status=status.HTTP_200_OK)


class KospiViewSet(viewsets.ModelViewSet):
    queryset = Kospi.objects.all()
    serializer_class = KospiInfoSerializer


class StockRegisterViewSet(APIView):
    ### stock request를 code:price:count,code:price:count 이런식으로 넘겨받자
    def post(self, request, user_pk, *args, **kwargs):
        stock_string = request.data['stock_list']
        stock_list = stock_string.split(',')
        for i in range(len(stock_list)):
            s = Stock()
            stock_code_price = stock_list[i].split(':')
            stock_code = stock_code_price[0]
            stock_price = stock_code_price[1]
            stock_count = stock_code_price[2]

            s.user = User.objects.get(id=user_pk)
            s.stock_name = stock_code
            s.stock_count = stock_count
            s.average_price = stock_price
            s.save()

        return Response('{detail : stocks are saved}', status=status.HTTP_200_OK)


class CalStatusViewSet(APIView):
    def get(self, request, user_pk, *args, **kwargs):
        user = User.objects.get(id=user_pk)
        stock_list = user.stock_user.all()
        stock_code_list = []
        total_price = 0
        cur_total_price = 0
        if len(stock_list) == 0:
            return Response('{"status" : "0"}', status=status.HTTP_200_OK)

        for i in range(len(stock_list)):
            stock_code_list.append(stock_list[i].stock_name)
            total_price += stock_list[i].stock_count * stock_list[i].average_price

            # Api 보내고 현재 평단가 계산
            URL = 'https://sandbox-apigw.koscom.co.kr/v2/market/stocks/kospi/'+stock_code_list[i]+'/price?apikey=l7xx3c412d920c714a50bcc459a83fca3a04'
            response = requests.get(URL)

            cur_price = response.json()['result']['trdPrc']
            cur_total_price += cur_price * stock_list[i].stock_count

        yield_rate = cur_total_price / total_price
        zoorimo_status = 0
        print(yield_rate)
        if yield_rate >= 2:
            zoorimo_status = 2
        elif yield_rate >= 1.5:
            zoorimo_status = 1
        elif yield_rate >= 1:
            zoorimo_status = 0
        elif yield_rate >= 0.5:
            zoorimo_status = -1
        elif yield_rate > 2:
            zoorimo_status = -2

        return Response('{status : '+str(zoorimo_status)+'}', status=status.HTTP_200_OK)



