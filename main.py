import os
from src.db_manager import DBManager
from src.api_client import HeadHunterAPI
from src.utils import save_companies_to_file, load_companies_from_file
from config import config

def main():
    """
    Основная функция для взаимодействия с пользователем.
    """
    db_config = config() # Загружаем параметры для подключения к БД из файла config.py

    db_name = "hh_database" # Имя базы данных.
    db_manager = DBManager(db_name, db_config)  # Создаем экземпляр DBManager

    # 1. Создание базы данных и таблиц (если необходимо)
    db_manager.create_database() # Создать БД, если ее не существует
    db_manager.create_tables() # Создать таблицы employers и vacancies, если их не существует

    # 2. Получение данных о компаниях и вакансиях (из файла или API)
    companies_file = "companies.json" # Файл для хранения информации о компаниях

    if os.path.exists(companies_file): # Если файл с компаниями существует
        companies = load_companies_from_file(companies_file) # Загрузить список компаний из файла
        print("Компании загружены из файла.")
    else:
        hh_api = HeadHunterAPI() # Создаем экземпляр HeadHunterAPI для работы с API hh.ru
        #Список ID интересующих компаний.  Можно менять этот список.
        company_ids = [1740, 80, 78638, 3529, 4181, 1455, 2748, 208707, 15478, 3388]#
        companies = [] # Инициализация списка компаний
        for company_id in company_ids:
            company = hh_api.get_company(company_id) # Получаем информацию о компании по ID
            if company:
                companies.append(company) # Добавляем компанию в список

        save_companies_to_file(companies, companies_file) # Сохранить список компаний в файл
        print("Компании загружены из API и сохранены в файл.")

    # 3. Заполнение базы данных
    db_manager.save_companies_to_db(companies) # Сохраняем данные о компаниях в БД
    for company in companies:
        vacancies = HeadHunterAPI().get_vacancies(company['id']) # Получаем вакансии компании через API
        db_manager.save_vacancies_to_db(vacancies, company['id']) # Сохраняем вакансии в БД

    # 4. Взаимодействие с пользователем
    while True:
        print("\nВыберите действие:")
        print("1 - Получить список компаний и количество вакансий у каждой компании")
        print("2 - Получить список всех вакансий")
        print("3 - Получить среднюю зарплату по вакансиям")
        print("4 - Получить список вакансий с зарплатой выше средней")
        print("5 - Получить список вакансий, содержащих ключевое слово")
        print("0 - Выход")

        choice = input("Ваш выбор: ")

        if choice == '1':
            companies_vacancies = db_manager.get_companies_and_vacancies_count()
            if companies_vacancies:
                for company, count in companies_vacancies.items():
                    print(f"{company}: {count} вакансий")
            else:
                print("Нет данных о компаниях и вакансиях.")

        elif choice == '2':
            all_vacancies = db_manager.get_all_vacancies()
            if all_vacancies:
                for vacancy in all_vacancies:
                    print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")
            else:
                print("Нет данных о вакансиях.")

        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == '4':
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            if higher_salary_vacancies:
                for vacancy in higher_salary_vacancies:
                    print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")
            else:
                print("Нет вакансий с зарплатой выше средней.")

        elif choice == '5':
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            if keyword_vacancies:
                for vacancy in keyword_vacancies:
                    print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата: {vacancy[2]}, Ссылка: {vacancy[3]}")
            else:
                print(f"Нет вакансий, содержащих ключевое слово '{keyword}'.")

        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")

if __name__ == "__main__":
    main()