import sqlite3

con = sqlite3.connect("viajes.db")
cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tablas en la base de datos:", cursor.fetchall())

cursor.execute("SELECT * FROM interacciones;")
rows = cursor.fetchall()

for row in rows:
    print(row)

con.close()