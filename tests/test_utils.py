import json
import os
from typing import Any, Dict, List, Union
from unittest.mock import patch

from src.utils import load_companies_from_file, save_companies_to_file


def test_save_companies_to_file_success(
    temp_json_file: str, sample_companies: List[Dict[str, Union[str, int, bool]]]
) -> None:
    """
    Тестирует успешное сохранение списка компаний в JSON-файл.
    """
    save_companies_to_file(sample_companies, temp_json_file)
    assert os.path.exists(temp_json_file)

    with open(temp_json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert data == sample_companies


def test_load_companies_from_file_success(
    temp_json_file: str, sample_companies: List[Dict[str, Union[str, int, bool]]]
) -> None:
    """
    Тестирует успешную загрузку списка компаний из JSON-файла.
    """
    # Сначала сохраняем данные в файл
    save_companies_to_file(sample_companies, temp_json_file)

    # Затем загружаем данные из файла
    loaded_companies = load_companies_from_file(temp_json_file)
    assert loaded_companies == sample_companies


def test_load_companies_from_file_jsondecodeerror(temp_json_file: str, capsys: Any) -> None:
    """
    Тестирует обработку JSONDecodeError при загрузке из файла.
    """
    # Создаем файл с некорректным JSON
    with open(temp_json_file, "w", encoding="utf-8") as f:
        f.write("Not a JSON file")

    loaded_companies = load_companies_from_file(temp_json_file)
    captured = capsys.readouterr()

    assert f"Ошибка при чтении файла '{temp_json_file}': неверный формат JSON." in captured.out
    assert loaded_companies == []


def test_load_companies_from_file_ioerror(temp_json_file: str, capsys: Any) -> None:
    """
    Тестирует обработку IOError при загрузке из файла.
    """
    # Мокируем open, чтобы вызвать IOError
    with patch("builtins.open", side_effect=IOError("No read access")):
        loaded_companies = load_companies_from_file(temp_json_file)
        captured = capsys.readouterr()

        assert "Ошибка при чтении файла" in captured.out
        assert loaded_companies == []
