from django.db import models


class Token(models.Model):
    acc_token = models.CharField(
        max_length=150,
        verbose_name='access_token'
    )
    rfh_token = models.CharField(
        max_length=150,
        verbose_name='refresh_token'
    )
    create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания пары токенов'
    )
