import pandas as pd
import sqlite3

# Шаг 1. Загрузка данных из CSV-файлов
users_file = 'users1.csv'
log_file = 'log1.csv'

# Создание базы данных SQLite
conn = sqlite3.connect('bets_data.s3db')
cursor = conn.cursor()

# Создаем таблицу USERS
cursor.execute('''
CREATE TABLE IF NOT EXISTS USERS (
    user_id TEXT,
    email TEXT,
    geo TEXT
);
''')

# Создаем таблицу LOG
cursor.execute('''
CREATE TABLE IF NOT EXISTS LOG (
    user_id TEXT,
    time DATETIME,
    bet REAL,
    win REAL
);
''')



# Загружаем данные из users_file (кодировка koi8_r)
data_users = pd.read_csv(users_file, encoding='koi8_r', delim_whitespace=True, names=['user_id', 'email', 'geo'], skiprows=1)
data_users.to_sql('USERS', conn, if_exists='replace', index=False)

# Загружаем данные из log_file
data_log = pd.read_csv(log_file, names=['user_id', 'time', 'bet', 'win'])
data_log.to_sql('LOG', conn, if_exists='replace', index=False)


# Извлечение корректного формата user_id с помощью SQL
cursor.execute("""
UPDATE LOG
SET user_id = (SELECT substr(user_id, instr(user_id, 'user_')) WHERE user_id LIKE '%user_%');
""")

# Очистка данных
cursor.execute("DELETE FROM USERS WHERE user_id NOT LIKE 'user_%' AND user_id NOT GLOB 'user_[0-9]*';")
cursor.execute("DELETE FROM LOG WHERE user_id NOT LIKE 'user_%' AND user_id NOT GLOB 'user_[0-9]*';")

cursor.execute("""
UPDATE log
SET time = datetime(
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(
                            REPLACE(
                                REPLACE(
                                    REPLACE(SUBSTR(time, 2), ' 1:', ' 01:'),
                                ' 2:', ' 02:'),
                            ' 3:', ' 03:'),
                        ' 4:', ' 04:'),
                    ' 5:', ' 05:'),
                ' 6:', ' 06:'),
            ' 7:', ' 07:'),
        ' 8:', ' 08:'),
    ' 9:', ' 09:')
)
WHERE time LIKE '[%';

""")

# Преобразование user_id в формат id
cursor.execute("""
UPDATE USERS
SET user_id = (SELECT SUBSTR(user_id, INSTR(user_id, '_') + 1) WHERE user_id LIKE '%user_%');
""")
cursor.execute("""
UPDATE LOG
SET user_id = (SELECT SUBSTR(user_id, INSTR(user_id, '_') + 1) WHERE user_id LIKE '%user_%');
""")


# Закрываем соединение
conn.commit()
conn.close()