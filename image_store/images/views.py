import datetime as dt
import uuid

import pytz
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Image, TempUrl
from .serializers import (BasikImageSerializer, ImageSerializer,
                          PremiumImageSerializer, TempUrlSerializer)


class ImageViewSet(RetrieveModelMixin,
                   ListModelMixin,
                   CreateModelMixin,
                   GenericViewSet):

    account_tiers = {
        'basik': BasikImageSerializer,
        'premium': PremiumImageSerializer,
        'enterprise': ImageSerializer,
    }

    def get_account_tier(self, user_account_tier):
        return self.account_tiers[user_account_tier]

    def get_queryset(self):
        user = self.request.user
        return user.images.all()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return self.account_tiers[self.request.user.account_tier]
        if self.action == 'create':
            return ImageSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = self.account_tiers[
            self.request.user.account_tier
        ](instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            instance_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class TempUrlCreateViewSet(CreateModelMixin, GenericViewSet):
    queryset = TempUrl.objects.all()
    serializer_class = TempUrlSerializer
    http_method_names = ('post',)

    def perform_create(self, serializer):
        url_hash = uuid.uuid4()
        image = get_object_or_404(Image, id=self.kwargs['image_id'])
        serializer.save(
            image=image,
            url_hash=url_hash,
            author=self.request.user,
        )


class TempUrlViewSet(APIView):
    http_method_names = ('get',)

    def get(self, request,  url_hash):
        temporary_link = get_object_or_404(TempUrl, url_hash=url_hash)
        link_end_time = (
                temporary_link.created
                + dt.timedelta(seconds=temporary_link.time_of_existence)
        )
        now_date = pytz.utc.localize(dt.datetime.now())
        if link_end_time > now_date:
            temporary_link.delete()
            return Response('The link has expired')
        serializer = ImageSerializer(temporary_link.image)
        return Response(serializer.data, status=status.HTTP_200_OK,)
