import uuid

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
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
    original_image = models.ImageField(
        'Image',
        upload_to=image_upload_path
    )
    basik_image = ImageSpecField(
        source='original_image',
        processors=[ResizeToFit(height=200)],
        format='JPEG'
    )
    premium_image = ImageSpecField(
        source='original_image',
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


class TempUrl(models.Model):
    url_hash = models.CharField("Hash", blank=False, max_length=32)
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='image',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='temp_urls',
    )
    created = models.DateTimeField('Created', auto_now_add=True)
    time_of_existence = models.PositiveIntegerField(
        validators=[
            MinValueValidator(300, message='Minimum time in seconds - 300'),
            MaxValueValidator(30000, message='Maximum time in seconds - 30000')
        ],
        help_text=('Enter time of existence the link in seconds '
                   'from 300 to 30000')
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Temporary link'
        verbose_name_plural = 'Temporary links'

    def __str__(self):
        return (f'{self.author} link to image from id - {self.image.id} '
                f'on {self.time_of_existence} second')
