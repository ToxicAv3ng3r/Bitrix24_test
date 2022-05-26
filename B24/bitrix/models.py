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


class Bitrix(models.Model):
    #  в качестве name рекомендуется использовать имя
    #  понятное для каких именно задач будет использоваться объект
    #  например dev или prod
    name = models.CharField(
        max_length=150,
        null=False,
        verbose_name='имя объекта'
    )
    client_id = models.CharField(
        max_length=150,
        null=False,
        verbose_name='client_id'
    )
    client_secret = models.CharField(
        max_length=150,
        null=False,
        verbose_name='client_secret'
    )
    domain = models.CharField(
        max_length=150,
        null=False,
        verbose_name='domain_in_bitrix'
    )
