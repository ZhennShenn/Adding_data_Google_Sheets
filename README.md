# Adding_data_Google_Sheets

Приложение работает с Google Sheets API. 
Программа собирает данные о характеристиках товара и добавляет их в таблицу.
На вход нужно передать ссылку на гугл таблицу, в первой колонке ('url') которой должны быть ссылки на карточки товаров Яндекс Маркета. 

# Запуск программы

Для получения файла credential.json для авторизации в Google API вам потребуется выполнить следующие шаги:

1. Перейдите на страницу Google API Console (https://console.developers.google.com/).
2. Создайте новый проект или выберите существующий проект.
3. В разделе "Библиотека" (Library) найдите и включите нужные API, Google Drive API и Google Sheets API.
4. В разделе "Учетные данные" (Credentials) нажмите на кнопку "Создать учетные данные" (Create Credentials) и выберите "Идентификатор клиента OAuth" (OAuth client ID).
5. После создания учетных данных вы сможете скачать файл credential.json, который содержит информацию о вашем клиентском идентификаторе.
6. Добавить файл credentials.json в проект.

Для установки зависимостей из файла requirements.txt вам нужно выполнить следующие шаги:

1. Откройте командную строку или терминал и перейдите в папку, где находится файл requirements.txt.
2. Выполните команду
```bash
pip install -r requirements.txt
```
Эта команда установит все зависимости, перечисленные в файле requirements.txt.
