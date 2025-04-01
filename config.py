import os
from typing import Dict, Optional

from dotenv import load_dotenv

load_dotenv()


def config() -> Dict[str, Optional[str]]:
    """
    Возвращает словарь с параметрами для подключения к базе данных PostgreSQL.
    Параметры следует заменить на ваши реальные значения.
    """
    return {
        "host": os.getenv("host"),  # Или IP-адрес сервера, где расположена БД
        "port": os.getenv("port"),  # Стандартный порт PostgreSQL
        "user": os.getenv("user"),  # Имя пользователя для подключения к БД
        "password": os.getenv("password"),  # Пароль пользователя
    }
