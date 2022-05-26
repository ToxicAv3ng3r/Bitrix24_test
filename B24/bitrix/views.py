from django.shortcuts import render, redirect
from django.conf import settings

import requests

from datetime import datetime, timezone

from .models import Token, Bitrix


def get_new_token():
    """Функция получения нового токена."""
    refresh_token = Token.objects.latest('create').rfh_token
    bitrix = Bitrix.objects.get(name=settings.NAME)
    params = {
        'grant_type': 'refresh_token',
        'client_id': bitrix.client_id,
        'client_secret': bitrix.client_secret,
        'refresh_token': refresh_token
    }

    response = requests.get(
        url='https://oauth.bitrix.info/oauth/token/',
        params=params,
        verify=False
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


def auth_redir(request):
    """Редирект на авторизацию"""
    bitrix = Bitrix.objects.get(name=settings.NAME)
    url = f'{bitrix.domain}/oauth/authorize/?client_id={bitrix.client_id}&response_type=code'
    return redirect(url)


def auth_b24(request):
    """Получает запрос от сервера авторизации, записывает токен в БД"""
    code = request.get_full_path().split('=')[1].split('&')[0]
    bitrix = Bitrix.objects.get(name=settings.NAME)
    params = {
        'grant_type': 'authorization_code',
        'client_id': bitrix.client_id,
        'client_secret': bitrix.client_secret,
        'code': code
    }
    response = requests.get(
        url=f'https://oauth.bitrix.info/oauth/token/',
        params=params,
        verify=False
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
    bitrix = Bitrix.objects.get(name=settings.NAME)
    if ((datetime.now(timezone.utc) - token.create).seconds
            > settings.SECONDS_IN_MINUTE):
        acc_token = get_new_token()
    response_curr_user = requests.get(
        url=f'{bitrix.domain}/rest/user.get?ACTIVE=true&auth={acc_token}',
        verify=False
    )
    users = response_curr_user.json().get('result')
    context = {
        "users": users
    }
    return render(request, 'bitrix/user.html', context)
