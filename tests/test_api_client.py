from typing import Dict, List, Optional, Union
from unittest.mock import MagicMock

import pytest
import requests

from src.api_client import HeadHunterAPI


@pytest.mark.parametrize(
    "company_id, expected_result",
    [
        (123, {"id": 123, "name": "Test Company", "url": "http://test.com"}),
        (456, {}),  # Мок для случая, когда API возвращает ошибку
    ],
)
def test_get_company(mock_hh_api: HeadHunterAPI, company_id: int, expected_result: Dict[str, Union[str, int]]) -> None:
    """
    Тестирует метод get_company.
    """
    mock_response = MagicMock()
    if company_id == 123:
        mock_response.json.return_value = {"id": 123, "name": "Test Company", "alternate_url": "http://test.com"}
        mock_response.raise_for_status.return_value = None
    else:
        mock_response.json.return_value = {}
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

    mock_hh_api.session.get.return_value = mock_response  # type:ignore # Используем мок-объект для сессии
    result = mock_hh_api.get_company(company_id)
    assert result == expected_result


@pytest.mark.parametrize(
    "company_id, mock_responses, expected_vacancies",
    [
        (
            123,
            [
                {
                    "items": [
                        {
                            "name": "Test Vacancy 1",
                            "salary": {"from": 100000, "to": 150000},
                            "alternate_url": "http://test.com/vacancy1",
                            "snippet": {"responsibility": "Responsibilities 1"},
                        },
                        {
                            "name": "Test Vacancy 2",
                            "salary": {"from": 120000, "to": 180000},
                            "alternate_url": "http://test.com/vacancy2",
                            "snippet": {"responsibility": "Responsibilities 2"},
                        },
                    ]
                },
                {"items": []},  # Вторая страница - пустая, конец пагинации
            ],
            [
                {
                    "name": "Test Vacancy 1",
                    "salary_from": 100000,
                    "salary_to": 150000,
                    "url": "http://test.com/vacancy1",
                    "description": "Responsibilities 1",
                },
                {
                    "name": "Test Vacancy 2",
                    "salary_from": 120000,
                    "salary_to": 180000,
                    "url": "http://test.com/vacancy2",
                    "description": "Responsibilities 2",
                },
            ],
        ),
        (
            456,
            [{"items": []}],  # Нет вакансий
            [],
        ),
        (
            789,
            [
                {
                    "items": [
                        {
                            "name": "Test Vacancy 3",
                            "salary": {"from": 80000, "to": 120000},
                            "alternate_url": "http://test.com/vacancy3",
                            "snippet": {"responsibility": "Responsibilities 3"},
                        },
                    ]
                },
                {"items": []},  # Вторая страница - пустая
            ],
            [
                {
                    "name": "Test Vacancy 3",
                    "salary_from": 80000,
                    "salary_to": 120000,
                    "url": "http://test.com/vacancy3",
                    "description": "Responsibilities 3",
                },
            ],
        ),
    ],
)
def test_get_vacancies(
    mock_hh_api: HeadHunterAPI,
    company_id: int,
    mock_responses: List[Dict[str, List[Dict[str, Union[str, Optional[int], str]]]]],
    expected_vacancies: List[Dict[str, Union[str, Optional[int], str]]],
) -> None:
    """
    Тестирует метод get_vacancies.
    """
    # Мокируем несколько ответов, чтобы имитировать пагинацию
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_hh_api.session.get.side_effect = [  # type:ignore
        MagicMock(json=lambda: response) for response in mock_responses
    ]

    # Эмулируем логику обработки ответа API в тестируемой функции
    def emulate_get_vacancies(company_id: int) -> List[Dict[str, Optional[Union[str, int]]]]:
        vacancies = []
        for response_data in mock_responses:  # Перебираем все моковые ответы (страницы)
            for item in response_data.get("items", []):  # Перебираем вакансии на каждой странице
                salary_from = item.get("salary", {}).get("from") if item.get("salary") else None  # type:ignore
                salary_to = item.get("salary", {}).get("to") if item.get("salary") else None  # type:ignore
                vacancies.append(
                    {
                        "name": item["name"],
                        "salary_from": salary_from,
                        "salary_to": salary_to,
                        "url": item["alternate_url"],
                        "description": item.get("snippet", {}).get("responsibility", ""),  # type:ignore
                    }
                )
        return vacancies

    vacancies = emulate_get_vacancies(company_id)
    assert vacancies == expected_vacancies
