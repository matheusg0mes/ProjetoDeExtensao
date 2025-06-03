import mysql.connector

conn = mysql.connector.connect(
    host='maglev.proxy.rlwy.net',
    port=42726,
    user='root',
    password='IYFvHMUzhUAhURDvhvcwrLPZcUGIwVPK',
    database='railway'
)

cursor = conn.cursor()


cursor.close()
conn.close()
