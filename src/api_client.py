import requests


class HeadHunterAPI:
    """
    Класс для взаимодействия с API hh.ru для получения информации о компаниях и вакансиях.
    """

    def __init__(self) -> None:
        """
        Конструктор класса HeadHunterAPI.
        """
        self.base_url = "https://api.hh.ru/"
        self.user_agent = {"User-Agent": "HH-User-Agent"}

    def get_company(self, company_id: int) -> dict:
        """
        Получает информацию о компании по её ID.

        Args:
            company_id (int): ID компании на hh.ru.

        Returns:
            dict: Словарь с информацией о компании.
        """
        try:
            response = requests.get(f"{self.base_url}employers/{company_id}", headers=self.user_agent)
            response.raise_for_status()  # Проверка на ошибки HTTP
            data = response.json()
            return {"id": data["id"], "name": data["name"], "url": data["alternate_url"]}
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении данных о компании: {e}")
            return {}

    def get_vacancies(self, company_id: int) -> list:
        """
        Получает список вакансий компании по её ID с использованием пагинации.

        Args:
            company_id (int): ID компании на hh.ru.

        Returns:
            list: Список словарей с информацией о вакансиях.
        """
        vacancies = []
        area = 1481
        page = 0
        per_page = 100  # Максимальное количество вакансий на странице(по умолчанию — 20, максимальное значение — 100)
        all_pages_loaded = False

        while not all_pages_loaded:
            try:
                params = {"employer_id": company_id, "page": page, "per_page": per_page, "area": area}
                response = requests.get(f"{self.base_url}vacancies", headers=self.user_agent, params=params)
                response.raise_for_status()  # Проверка на ошибки HTTP

                data = response.json()
                items = data.get("items", [])  # Используем get() чтобы избежать KeyError

                if not items:  # Если страница пустая, значит, все вакансии загружены
                    all_pages_loaded = True
                    continue

                for item in items:
                    salary_from = item.get("salary", {}).get("from") if item.get("salary") else None
                    salary_to = item.get("salary", {}).get("to") if item.get("salary") else None
                    vacancies.append(
                        {
                            "name": item["name"],
                            "salary_from": salary_from,
                            "salary_to": salary_to,
                            "url": item["alternate_url"],
                            "description": item.get("snippet", {}).get("responsibility", ""),
                        }
                    )

                page += 1  # Переходим на следующую страницу

            except requests.exceptions.RequestException as e:
                print(f"Ошибка при получении данных о вакансиях (страница {page}): {e}")
                break  # Прерываем цикл при ошибке

        return vacancies
