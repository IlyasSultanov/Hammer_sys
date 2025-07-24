import psycopg2

# Явно задайте строку подключения в ASCII
conn = psycopg2.connect(
    "dbname='test_db' user='test_user' host='localhost' password='test_pw' port='5432'"
)
print("Успешное подключение!")
conn.close()