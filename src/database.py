import pymysql

database = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="videojuegos",
    port=3306
)

print(database)