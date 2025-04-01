import json

def save_companies_to_file(companies: list, filename: str):
    """
    Сохраняет список компаний в файл в формате JSON.

    Args:
        companies (list): Список словарей с информацией о компаниях.
        filename (str): Имя файла для сохранения данных.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(companies, f, ensure_ascii=False, indent=4)
        print(f"Данные о компаниях успешно сохранены в файл '{filename}'.")
    except IOError as e:
        print(f"Ошибка при записи в файл: {e}")

def load_companies_from_file(filename: str) -> list:
    """
    Загружает список компаний из файла в формате JSON.

    Args:
        filename (str): Имя файла для загрузки данных.

    Returns:
        list: Список словарей с информацией о компаниях.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка при чтении файла '{filename}': неверный формат JSON.")
        return []
    except IOError as e:
        print(f"Ошибка при чтении файла: {e}")
        return []