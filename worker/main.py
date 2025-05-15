## worker/main.py (resumo do fluxo)

import sqlite3
from datetime import datetime
# após chamada à inferência
price = prediction["prediction"]
day_of_year = datetime.now().timetuple().tm_yday

conn = sqlite3.connect("/data/app.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY AUTOINCREMENT, price REAL, day_of_year INT, created_at TEXT)")
cursor.execute("INSERT INTO predictions (price, day_of_year, created_at) VALUES (?, ?, ?)", (price, day_of_year, datetime.utcnow().isoformat()))
conn.commit()
conn.close()
