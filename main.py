import gspread
from gspread import Client, Spreadsheet
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import messagebox


def get_characteristics(link):
    try:
        # Получаем HTML-страницу товара
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "lxml")
        characteristics_button = soup.find("a", class_="_2S7Nj _3i2oe")
        try:
            characteristics_url = characteristics_button["href"]

            # Отправляем GET-запрос на страницу подробных характеристик
            characteristics_response = requests.get(f"https://market.yandex.ru/{characteristics_url}")

            try:
                # Создаем объект BeautifulSoup для парсинга HTML-кода страницы характеристик
                characteristics_soup = BeautifulSoup(characteristics_response.content, "lxml")

                # Находим все элементы с названиями характеристик
                names = characteristics_soup.find_all("div", class_="_2TxqA")

                # Находим все элементы со значениями характеристик
                values = characteristics_soup.find_all("div", class_="_3PnEm")

                # Парсим названия и значения характеристик
                characteristics_dict = {}
                for n, v in zip(names, values):
                    characteristics_dict[n.find("span").text.strip()] = v.find("dd").text.strip()

                return characteristics_dict

            except Exception as e:
                print(e)
                return

        except Exception as e:
            print(e)
            return

    except Exception as e:
        print(e)
        return


def add_characteristics(characteristics: dict, df):
    # Объединяем характеристики всех товаров в один датафрейм
    df = pd.concat([df, pd.DataFrame([characteristics])], ignore_index=True)
    return df


def get_urls(sh: Spreadsheet):
    ws = sh.sheet1
    ws.add_cols(50)
    df = pd.DataFrame()
    for i in range(2, len(ws.col_values(1)) + 1):
        val = ws.acell(f'A{i}').value
        print(val)
        res = get_characteristics(val)
        print(res)
        df = add_characteristics(res, df)
    df = df.fillna('')

    # Обновление таблицы, добавление характеристик товаров
    ws.update(values=[df.columns.values.tolist()], range_name='B1')
    ws.update(values=df.values.tolist(), range_name='B2')


def main():
    # Получение доступа к API
    gc: Client = gspread.service_account('./credentials.json')
    # Получение ссылки на Google таблицу
    link = entry.get()
    sh: Spreadsheet = gc.open_by_url(link)
    # Обработка данных таблицы
    get_urls(sh)
    # Сообщение о завершении обработки
    messagebox.showinfo("Обработка завершена", "Обработка данных завершена!")
    # Закрытие главного окна
    window.destroy()


# Создание главного окна
window = tk.Tk()
window.geometry('900x110')
window.title('Добавление в таблицу характеристик товаров')

# Создание метки и поля ввода для ссылки на Google таблицу
label = tk.Label(window, text="Введите ссылку на Google таблицу:", font=("Arial", 10))
label.pack(anchor="center", pady=5, expand=1)
entry = tk.Entry(window, width=95, font=("Arial", 12))
entry.pack(anchor="center", pady=5, expand=1)

# Создание кнопки для запуска обработки данных
button = tk.Button(window, text="Обновить таблицу", font=("Arial", 10), command=main)
button.pack(anchor="center", pady=5, expand=1)

# Запуск главного цикла окна
window.mainloop()
