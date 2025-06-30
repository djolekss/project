import mysql.connector

connect = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'zdravpaw3'
)

cursor = connect.cursor()