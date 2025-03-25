import meteostat as ms

with ms.connect_stations_db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stations;")
    tables = cursor.fetchall()
    print("Tables in database:", tables)
