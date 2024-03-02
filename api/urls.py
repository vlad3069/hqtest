from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (ProductListView, ProductAccessAPIView,
                       LessonListView, GroupListAPIView)


urls_v1 = [
    path(
        r'products/',
        ProductListView.as_view(),
        name='products',
    ),
    path(
        r'product/<str:name>/',
        ProductAccessAPIView.as_view(),
        name='product-detail',
    ),
    path(
        r'lessons/<str:name>/',
        LessonListView.as_view(),
        name='lessons',
    ),
    path(
        r'groups/',
        GroupListAPIView.as_view(),
        name='groups',
    ),
]

router_v1 = DefaultRouter()


urlpatterns = [
    path(r'auth/', include('djoser.urls.jwt')),
    path(r'v1/', include(urls_v1)),
    path(r'', include(router_v1.urls)),
]