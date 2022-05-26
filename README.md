# Bitrix24_test

1) В первую очередь необходимо добавить в свой bitrix24 новое приложение.
    - Главная -> Приложения -> Разработчикам -> Другое -> Локальное приложение
    - В открывшемся виджете поставить отметку "Серверное" и "Использует только API"
    - Путь обработчика и путь первоначальной установки указать: http://127.0.0.1:8000/b24_auth/
    - В настройке прав добавить "Пользователи"
    - Сохранить

2) Далее переходим к настройке самого проекта
   - Клонируем репозиторий на свою компьютер
     ```
      cd Bitrix24_test/
     ```
   - Создаем и активируем виртуальное окружение
      ```
     python -m venv venv
     source venv/Scripts/activate (для Windows)
     source venv/bin/activate (для Linux)
     ```
   - Устанавливаем зависимости
       ```
     pip install -r requirements.txt
       ```
   - Переходим в корневую папку проекта
       ```
     cd B24/
       ```
   - Выполняем миграции
       ```
     python manage.py migrate
       ```
   - Прежде, чем запустить сервер необходимо создать объект класса Bitrix содержащий в себе client_id, client_secret и domain. 
      Получить их можно в своем bitrix24 после добавления приложения. 
      Для этого: Главная -> Приложения -> Разработчикам -> Интеграции.
      Выбрать свое приложение и нажать "Редактировать". В открывшемся виджете
      Вы найдете искомые значения. domain же несложно получить из адресной строки Вашего браузера.
      Данный объект, помимо авторизационных данных имеет атрибут name, который указывается на усмотрение разработчика.
      Например, dev или prod
      Для создания объекта можно воспользоваться shell
      ```
     python manage.py shell
      ```
      В запустившейся консоли необходимо последовательно выполнить команды
      ```
     from bitrix.models import Bitrix
     Bitrix.objects.create(name='write_name', client_id='your_client_id', client_secret='your_client_secret', domain='your_domain')
      ```
     Далее в settings.py в параметре NAME необходимо прописать то значение, которое Вы указывали при создании объекта.
     ВАЖНО!!! Значение параметра domain должно быть вида 'https://b24-iqhkzt.bitrix24.ru'
     В дальнейшем, чтобы поменять авторизационные параметры, достаточно будет указать необходимое name в настройках.
     (Предварительно создав новый объект Bitrix)
   - Запускаем dev-сервер
       ```
     python manage.py runserver
       ```
   - Переходим на главную страницу проекта по адресу http://127.0.0.1:8000/
   - Видим, что для продолжения необходима авторизация в системе bitrix24,
     а значит нажимаем "Авторизоваться"
   - После ввода логина и пароля в системе bitrix24 Вас автоматически перебросит
     на страницу, которая отобразит список всех сотрудников в Вашем bitrix24
   - Вы восхитительны!