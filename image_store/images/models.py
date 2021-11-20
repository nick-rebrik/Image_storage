import uuid

from django.contrib.auth import get_user_model
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


User = get_user_model()


def image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    author_name = instance.author.username
    return f'{author_name}/{filename}'


class Image(models.Model):
    title = models.CharField('Titile', max_length=100)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images',
    )
    image = models.ImageField(
        'Image',
        upload_to=image_upload_path
    )
    basik_image = ImageSpecField(
        source='image',
        processors=[ResizeToFit(height=200)],
        format='JPEG'
    )
    premium_image = ImageSpecField(
        source='image',
        processors=[ResizeToFit(height=400)],
        format='JPEG'
    )
    pub_date = models.DateTimeField('Date of publication', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.title
