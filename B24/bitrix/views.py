from django.shortcuts import render, redirect

import requests

from datetime import datetime, timezone

from .models import Token


def get_new_token():
    """Функция получения нового токена."""
    refresh_token = Token.objects.latest('create').rfh_token
    data = {
        'grant_type': 'refresh_token',
        'client_id': 'local.628bbf7e970412.73001540',
        'client_secret': 'xOfsk9ubJZdFv60WK6nCtEUgEhl5xG2vVyTG0Lz25zwcMFGHPg',
        'refresh_token': refresh_token
    }

    response = requests.get(
        url='https://oauth.bitrix.info/oauth/token/',
        data=data
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
    data = {
        'grant_type': 'authorization_code',
        'client_id': 'local.628bbf7e970412.73001540',
        'client_secret': 'xOfsk9ubJZdFv60WK6nCtEUgEhl5xG2vVyTG0Lz25zwcMFGHPg',
        'code': code
    }
    response = requests.get(
        url=f'https://oauth.bitrix.info/oauth/token/',
        data=data
    )
    dat = response.json()
    acc_token = dat.get('access_token')
    rfh_token = dat.get('refresh_token')
    Token.objects.create(
        acc_token=acc_token,
        rfh_token=rfh_token,
    )

    return redirect('bitrix:current_user')


def show_curr_user(request):
    """Страница отображает текущего авторизованного пользователя"""
    token = Token.objects.latest('create')
    acc_token = token.acc_token
    if (datetime.now(timezone.utc) - token.create).seconds > 3600:
        acc_token = get_new_token()
    response_curr_user = requests.get(
        url=f'https://b24-iqhkzt.bitrix24.ru/rest/user.current?auth={acc_token}')
    curr_user = response_curr_user.json().get('result')
    name = curr_user.get('NAME')
    last_name = curr_user.get('LAST_NAME')
    second_name = curr_user.get('SECOND_NAME')
    email = curr_user.get('EMAIL')
    context = {
        "name": name,
        "last_name": last_name,
        "second_name": second_name,
        "email": email
    }
    return render(request, 'bitrix/user.html', context)
