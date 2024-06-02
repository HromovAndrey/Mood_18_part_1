# Завдання 1
# Для бази даних «Лікарня», яку ви розробляли в рамках
# курсу «Теорія Баз Даних», створіть додаток для взаємодії з
# базою даних, який дозволяє:
# ■ Вставляти рядки в таблиці бази даних.
# ■ Оновлення рядків у таблицях бази даних. При спробі
# оновлення усіх рядків в одній таблиці надайте запит на
# підтвердження користувачеві. Оновлювати усі рядки
# можна лише після підтвердження користувачем.
# ■ Видалення рядків з таблиць баз даних. При спробі видалити
# усі рядки в одній таблиці потрібно видавати користувачу
# запит на підтвердження. Видаляти усі рядки, можна тільки
# після підтвердження користувачем.
# Завдання 2
# Для бази даних «Лікарня», яку ви розробляли в рамках
# курсу «Теорія Баз Даних», створіть додаток для взаємодії
# з базою даних, який дозволяє створювати звіти:
# ▷ Вивести прізвища лікарів та їх спеціалізації;
# ▷ Вивести прізвища та зарплати (сума ставки та надбавки)
# лікарів, які не перебувають у відпустці;
# ▷ Вивести назви палат, які знаходяться у певному відділенні;
# Практичне завдання
# 1
# ▷ Вивести усі пожертвування за вказаний місяць у
# вигляді: відділення, спонсор, сума пожертвування, дата
# пожертвування;
# ▷ Вивести назви відділень без повторень, які спонсоруються певною компанією.
# Завдання 3
# Для бази даних «Лікарня», яку ви створювали в рамках
# курсу «Теорія баз даних», реалізуйте програму, яка дозволить
# працювати зі структурою бази даних. Програма має:
# ■ відображати назви усіх таблиць;
# ■ відображати назви стовпців певної таблиці;
# ■ відображати назви стовпців та їх типи для певної
# таблиці;
# ■ відображати зв’язки між таблицями;
# ■ вміти створювати таблиці;
# ■ видаляти таблиці;
# ■ додавати стовпці;
# ■ оновлювати стовпці;
# ■ видаляти стовпці.

from sqlalchemy import create_engine, MetaData, insert, delete, update
from sqlalchemy.orm import sessionmaker
import json
import sqlite3

with open('config.json', 'w') as file:
    data = {'user':'postgres','password':'Andrey36912'}
    json.dump(data,file)
with open('config.json', 'r') as file:
    data = json.load(file)
    db_user = data['user']
    db_password = data['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Hospital1'
engine = create_engine(db_url)

metadata = MetaData()
metadata.reflect(bind=engine)

connection = engine.connect()
def insert_row(table):
    connection = sqlite3.connect('hospital.db')
    cursor = connection.cursor()

    last_name = input("Enter last name: ")
    specialization = input("Enter specialization: ")
    salary = float(input("Enter salary: "))
    is_on_vacation = int(input("Is on vacation? (1 for yes, 0 for no): "))

    cursor.execute('''
        INSERT INTO Doctors (last_name, specialization, salary, is_on_vacation)
        VALUES (?, ?, ?, ?)
        ''', (last_name, specialization, salary, is_on_vacation))

    connection.commit()
    connection.close()
def updata_data(table):
    connection = sqlite3.connect('hospital.db')
    cursor = connection.cursor()
    doctor_id = int(input("Enter doctor ID to update: "))
    last_name = input("Enter new last name: ")
    specialization = input("Enter new specialization: ")
    salary = float(input("Enter new salary: "))
    is_on_vacation = int(input("Is on vacation? (1 for yes, 0 for no): "))

    cursor.execute('''
        UPDATE Doctors
        SET last_name = ?, specialization = ?, salary = ?, is_on_vacation = ?
        WHERE doctor_id = ?
        ''', (last_name, specialization, salary, is_on_vacation, doctor_id))

    connection.commit()
    connection.close()
def delete_data(table):
    connection = sqlite3.connect('hospital.db')
    cursor = connection.cursor()

    doctor_id = int(input("Enter doctor ID to delete: "))

    cursor.execute('''
        DELETE FROM Doctors WHERE doctor_id = ?
        ''', (doctor_id,))

    connection.commit()
    connection.close()

def generate_report(table):
    connection = sqlite3.connect('hospital.db')
    cursor = connection.cursor()

    query = input("Enter your SELECT query: ")
    cursor.execute(query)
    results = cursor.fetchall()

    for result in results:
        print(result)

    connection.close()
while True:
    print('Таблиці з бази данних')
    for table_name in metadata.tables.keys():
        print(table_name)

    table_name = input('Ведіть назву таблиці')

    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        print('Оберіть функцію')
        print('1 добавити рядок')
        print('2 видалити дані')
        print('3 змінити дані')
        print("4. створити дані")

        command = int(input('Номер функції'))

        if command == 1:
            insert_row(table)
        elif command == 2:
            updata_data(table)
        elif command == 3:
            delete_data(table)
        elif command == 4:
            generate_report(table)
