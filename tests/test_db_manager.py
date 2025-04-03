# from typing import Any
# from unittest.mock import MagicMock, patch
#
#
# def test_create_database_new(db_manager):  # type:ignore
#     """Тест для создания новой базы данных, если она не существует."""
#     with patch("psycopg2.connect") as mock_connect:
#         mock_conn = MagicMock()
#         mock_conn.autocommit = True
#         mock_cur = MagicMock()
#         mock_connect.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#         mock_cur.fetchone.return_value = None  # База данных не существует
#
#         db_manager.create_database()
#
#         mock_cur.execute.assert_any_call("SELECT 1 FROM pg_database WHERE datname='test_db'")
#         mock_cur.execute.assert_any_call("CREATE DATABASE test_db")
#
#
# def test_create_database_existing(db_manager: Any) -> None:
#     """Тест для случая, когда база данных уже существует."""
#     with patch("psycopg2.connect") as mock_connect:
#         mock_conn = MagicMock()
#         mock_conn.autocommit = True
#         mock_cur = MagicMock()
#         mock_connect.return_value = mock_conn
#         mock_conn.cursor.return_value = mock_cur
#         mock_cur.fetchone.return_value = [1]  # База данных уже существует
#
#         db_manager.create_database()
#
#         mock_cur.execute.assert_called_once_with("SELECT 1 FROM pg_database WHERE datname='test_db'")
