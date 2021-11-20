from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    PLANS_TIER = [
        ('basik', 'Basik'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    account_tier = models.CharField(
        max_length=20,
        choices=PLANS_TIER,
        default='basik',
    )

    def __str__(self):
        return self.username
