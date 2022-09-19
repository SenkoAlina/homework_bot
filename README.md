# Бот в Telegram

Telegram-бот, который обращается к API сервиса Яндекс. Практикум и оповещает о статусе сданной на проверку домашней работы. 
Присылает сообщения, когда статус изменен - взято в проверку, есть замечания, зачтено.

## Технологии:

* Python 3.7
* python-dotenv
* python-telegram-bot 

## Как запустить проект:


Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SenkoAlina/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Записать в переменные окружения (файл .env) необходимые ключи:

* токен профиля на Яндекс.Практикуме
* токен телеграм-бота
* свой ID в телеграме

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
