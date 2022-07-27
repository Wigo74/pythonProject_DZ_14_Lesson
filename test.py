import sqlite3

with sqlite3.connect("../netflix.db") as connection:
    cur = connection.cursor()
    sqlite_query = ("select * FROM netflix ")
    result = cur.execute(sqlite_query)
    data = cur.fetchall()
    connection.close()


print(data)
