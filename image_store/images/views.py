from rest_framework import status
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (BasikImageSerializer, ImageSerializer,
                          PremiumImageSerializer)


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
