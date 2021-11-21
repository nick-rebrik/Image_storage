from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ImageViewSet, TempUrlViewSet, TempUrlCreateViewSet

router_v1 = DefaultRouter()
router_v1.register('images', ImageViewSet, basename='Images')
router_v1.register(
    'images/(?P<image_id>[0-9]+)/temp_url',
    TempUrlCreateViewSet,
    basename='Temp_Url'
)

urlpatterns = [
    path(
        'v1/images/<uuid:url_hash>/',
        TempUrlViewSet.as_view(),
        name='temp_url',
    ),
    path('v1/', include(router_v1.urls))
]