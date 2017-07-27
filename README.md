# DCO2MSSQL
Скрипт переноса данных о нарядах на работу из StruxureWare DCO в MSSQL DB на Python

## Настройка:
- Установить Python 3.5.x (3.6 не поддерживается модулем pymssql)
- Загрузить пакеты `pymssql`, `json`, `requests`, `PyQT5`. В командной строке выполнить:

```
pip install pymssql json requests PyQT5
```
- Скачать оба файла из репозитория (`reqScriptGUI.py` и `script.conf`) и разместить их в одной директории (желательно, чтобы в пути присутствовали только символы стандартной ASCII таблицы)
- В файле `reqScriptGUI.py` внести путь до файла `script.conf`:

```python
    def dbUpdateProc(self):
        conf_file = open('/home/apc/pyDCO2MSSQL/script.conf') #ЗДЕСЬ ВАШ ПУТЬ ДО script.conf
        config = json.load(conf_file)
        conf_file.close()
 ```
 - В файле `script.conf` настроить следующее:
 ```json
       "serverIP":"192.168.1.132",  # IP АДРЕС СЕРВЕРА DCO
	   "login":"dco",               # ЛОГИН DCO
	   "password":"dco123"          # ПАРОЛЬ DCO
 ```
   А также:
 ```json
       "sqlServerIP":"WINSERVER\\SQLSERVER", # ИМЯ_КОМПЬЮТЕРА\\MSSQL_СЕРВЕР
	   "dbName":"dco-db",                    # ИМЯ БД
	   "dbUser":"dco",                       # ЛОГИН ДЛЯ БД
	   "dbPswd":"dco123",                    # ПАРОЛЬ ДЛЯ ДБ
  ```
## Запуск и использование:
- Для запуска переноса данных можно дважды кликнуть по `reqScriptGUI.py` либо в командной строке из дериктории скрипта выполнить `python reqScriptGUI.py`
- После запуска откроется окно терминала (если запуск был не из терминала) и окно GUI интерфейса с двумя кнопками `Update DB` и `Quit`. 
- После нажатия на `Update DB` в командной строке будут отображаться логи операций (статус соединения с сервером БД и все выполняемые запросы к БД). В случае неверной настройки последние строки ошибки подскажут в чем проблема.
- Каждые 10 минут (данный параметр зависит от аргумента функции) 
```python
    time.sleep(xxx) #ВРЕМЯ В СЕКУНДАХ
    sqlconnect.close()
```
    скрипт будет повторять опрос БД. 
- `Quit` останавливает опрос и закрывает скрипт.

## Возможные проблемы:
- При ошибке во время установки пакета `pymssql` на macOS, выполнить:
```
brew install freetds@0.91
brew link --force freetds@0.91
pip install pymssql
```
- При ошибке запуска на Windows добавить переменную окружения `QT_QPA_PLATFORM_PLUGIN_PATH` с путем до папки с `qwindows.dll`
