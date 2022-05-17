import logging
import os
import sys
import requests
import telegram
import time

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Отправляем сообщение в Telegram чат."""
    bot.send_message(TELEGRAM_CHAT_ID, message)
    logger.info('Сообщение отправлено')


def get_api_answer(current_timestamp):
    """Запрос к эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if response.status_code != 200:
        raise Exception(f'Неожиданный ответ сервера: {response.status_code}')
    return response.json()


def check_response(response):
    """Проверка ответа API на корректность."""
    if type(response) == dict:
        if 'homeworks' not in response:
            raise Exception("Отсутствует поле 'homeworks' в ответе API")
        homeworks = response['homeworks']
        if type(homeworks) != list:
            raise TypeError('Домашки пришли не в виде списка')
        return homeworks
    raise TypeError('Тип ответа API не является словарем')


def parse_status(homework):
    """Получение статуса домашней работы."""
    if 'homework_name' not in homework:
        message = "Отсутствует поле 'homework_name' в ответе API"
        logger.error(message)
        raise KeyError(message)
    if 'status' not in homework:
        message = "Отсутствует поле 'status' в ответе API"
        logger.error(message)
        raise Exception(message)
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status not in HOMEWORK_STATUSES:
        message = "Неизвестный статус"
        logger.error(message)
        raise Exception(message)
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка переменных окружения."""
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID and PRACTICUM_TOKEN:
        return True
    else:
        logger.critical(
            'Отсутствует одна(или более) из обязательных переменных окружения')
        return False


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        return None

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            for homework in homeworks:
                status = parse_status(homework)
                send_message(bot, status)

            current_timestamp = int(time.time())
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
