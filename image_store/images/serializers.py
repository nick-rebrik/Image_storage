from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    basik_image = Base64ImageField(read_only=True)
    premium_image = Base64ImageField(read_only=True)

    class Meta:
        model = Image
        fields = (
            'id',
            'title',
            'image',
            'basik_image',
            'premium_image',
            'pub_date'
        )


class BasikImageSerializer(ImageSerializer):

    class Meta:
        model = Image
        fields = (
            'id',
            'title',
            'basik_image',
            'pub_date'
        )


class PremiumImageSerializer(ImageSerializer):

    class Meta:
        model = Image
        fields = (
            'id',
            'title',
            'basik_image',
            'premium_image',
            'pub_date'
        )
