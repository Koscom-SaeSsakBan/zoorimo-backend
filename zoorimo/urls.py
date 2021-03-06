from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_nested import routers

from django.conf.urls.static import static
from django.conf import settings

from zoorimo.app import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

user_router = routers.NestedDefaultRouter(router, r'users', lookup='user')
user_router.register(r'zoorimo', views.ZoorimoViewSet, basename='zoorimo')
user_router.register(r'quiz', views.QuizViewSet, basename='quiz')
user_router.register(r'kospi', views.KospiViewSet, basename='kospi')

# user_router.register(r'quiz/false', views.QuizViewSet, basename='quiz')

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path(r'api/v1/', include(router.urls)),
    path(r'api/v1/', include(user_router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url('api/v1/users/(?P<user_pk>[0-9]+)/quiz/true', views.QuizTrueViewSet.as_view()),
    url('api/v1/users/(?P<user_pk>[0-9]+)/stock/register', views.StockRegisterViewSet.as_view()),
    url('api/v1/users/(?P<user_pk>[0-9]+)/status', views.CalStatusViewSet.as_view()),
    url('api/v1/users/(?P<user_pk>[0-9]+)/stock/status', views.StockStatusViewSet.as_view()),

]
