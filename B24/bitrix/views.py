from django.shortcuts import render, redirect
from django.conf import settings

import requests

from datetime import datetime, timezone

from .models import Token


def get_new_token():
    """Функция получения нового токена."""
    refresh_token = Token.objects.latest('create').rfh_token
    params = {
        'grant_type': 'refresh_token',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'refresh_token': refresh_token
    }

    response = requests.get(
        url='https://oauth.bitrix.info/oauth/token/',
        params=params
    ).json()
    acc_token = response.get('access_token')
    rfh_token = response.get('refresh_token')
    Token.objects.create(
        acc_token=acc_token,
        rfh_token=rfh_token
    )

    return acc_token


def index(request):
    """Главная страница."""
    return render(request, 'bitrix/index.html')


def auth_b24(request):
    """Получает запрос от сервера авторизации, записывает токен в БД"""
    code = request.get_full_path().split('=')[1].split('&')[0]
    params = {
        'grant_type': 'authorization_code',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'code': code
    }
    response = requests.get(
        url=f'https://oauth.bitrix.info/oauth/token/',
        params=params
    )
    dat = response.json()
    acc_token = dat.get('access_token')
    rfh_token = dat.get('refresh_token')
    Token.objects.create(
        acc_token=acc_token,
        rfh_token=rfh_token,
    )

    return redirect('bitrix:users')


def show_users(request):
    """Страница отображает всех пользователей в bitrix24"""
    token = Token.objects.latest('create')
    acc_token = token.acc_token
    if ((datetime.now(timezone.utc) - token.create).seconds
            > settings.SECONDS_IN_MINUTE):
        acc_token = get_new_token()
    response_curr_user = requests.get(
        url=f'https://b24-iqhkzt.bitrix24.ru/rest/user.get?auth={acc_token}'
    )
    users = response_curr_user.json().get('result')
    context = {
        "users": users
    }
    return render(request, 'bitrix/user.html', context)
