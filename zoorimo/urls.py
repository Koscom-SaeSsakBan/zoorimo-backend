from django.urls import include, path
from rest_framework import routers
from app import views
from django.contrib import admin


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'users/'r'detail', views.UserDetailViewSet)
router.register(r'fuck', views.UserDetailViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]