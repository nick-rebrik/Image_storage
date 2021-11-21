from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import Image, TempUrl


class ImageSerializer(serializers.ModelSerializer):
    basik_image = Base64ImageField(read_only=True)
    premium_image = Base64ImageField(read_only=True)

    class Meta:
        model = Image
        fields = (
            'id',
            'title',
            'original_image',
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


class TempUrlSerializer(serializers.ModelSerializer):
    temporary_link = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TempUrl
        fields = ('temporary_link', 'time_of_existence')

    def get_temporary_link(self, temp_url_object):
        return (f"http://{self.context['request'].META['HTTP_HOST']}"
                f"/api/v1/images/{temp_url_object.url_hash}/")
