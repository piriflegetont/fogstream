## Данные использованных аккаунтов
  1) Администратор 
      - **username/login**: admin
      - **password**: MeidY0QnhIwn
      - **email**: test.user.django@yandex.ru) 
1) Пользователь 
    - **username/login**: testUser
     - **password**: 123_makarena_123
     
## Команды

Здесь и далее все команды выполняются из *virtualenv* в директории с приложением.
Локальный запуск

~~~~cmd
\> python manage.py runserver
~~~~

Запуск тестов

~~~~cmd
\> python manage.py test
~~~~

Запуск тестов c проверкой на покрытие (требует установленного coverage) и формирование отчёта

~~~~cmd
\> coverage run --source testApp manage.py test testApp
\> coverage html
~~~~
     