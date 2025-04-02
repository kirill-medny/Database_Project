from typing import Any, Dict, Generator, List, Optional, Tuple, Union
from unittest.mock import MagicMock, patch

import pytest
from dotenv import load_dotenv

from src.api_client import HeadHunterAPI
from src.db_manager import DBManager

load_dotenv()


# Фикстуры для api_client
@pytest.fixture
def mock_hh_api() -> Generator[HeadHunterAPI, None, None]:
    """
    Фикстура для создания экземпляра HeadHunterAPI с заглушками.
    """
    with patch("src.api_client.requests.get") as mock_get:
        api = HeadHunterAPI()
        api.session = MagicMock()  # type:ignore # Создаем мок-объект для сессии
        api.session.get = mock_get  # type:ignore # Заменяем requests.get на мок-объект
        yield api


@pytest.fixture
def mock_company_data() -> Dict[str, Union[str, int]]:
    """
    Фикстура для предоставления моковых данных о компании.
    """
    return {
        "id": 123,
        "name": "Test Company",
        "alternate_url": "http://test.com",
    }


@pytest.fixture
def mock_vacancy_data() -> List[Dict[str, Union[str, Optional[Dict[str, Union[int, None]]]]]]:
    """
    Фикстура для предоставления моковых данных о вакансиях.
    """
    return [
        {
            "name": "Test Vacancy 1",
            "salary": {"from": 100000, "to": 150000},
            "alternate_url": "http://test.com/vacancy1",
            "snippet": {"responsibility": "Responsibilities 1"},  # type:ignore
        },
        {
            "name": "Test Vacancy 2",
            "salary": {"from": 120000, "to": 180000},
            "alternate_url": "http://test.com/vacancy2",
            "snippet": {"responsibility": "Responsibilities 2"},  # type:ignore
        },
    ]


# Фикстуры для utils
@pytest.fixture
def temp_json_file(tmp_path: Any) -> str:
    """
    Фикстура, создающая временный JSON-файл для тестирования.
    """
    file_path = tmp_path / "test_companies.json"
    return str(file_path)


@pytest.fixture
def sample_companies() -> List[Dict[str, Union[str, int, bool]]]:
    """
    Фикстура, предоставляющая пример списка компаний.
    """
    return [
        {"id": 1, "name": "Company A", "url": "http://companyA.com"},
        {"id": 2, "name": "Company B", "url": "http://companyB.com"},
    ]


@pytest.fixture
def db_manager() -> DBManager:
    """Фикстура для создания экземпляра DBManager."""
    db_config = {"host": "localhost", "port": 5432, "user": "postgres", "password": "password"}
    return DBManager("test_db", db_config)


@pytest.fixture
def db_connection_mock() -> Tuple[MagicMock, MagicMock]:
    """Фикстура для мокирования соединения с базой данных."""
    connection_mock = MagicMock()
    cursor_mock = MagicMock()
    connection_mock.cursor.return_value = cursor_mock
    return connection_mock, cursor_mock
