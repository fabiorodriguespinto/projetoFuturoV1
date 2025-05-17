from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/predictions")
def get_predictions(limit: int = 10):
    conn = sqlite3.connect("/data/app.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT price, day_of_year, created_at FROM predictions ORDER BY id DESC LIMIT ?", 
        (limit,)
    )
    results = cursor.fetchall()
    conn.close()
    return [
        {"price": r[0], "day_of_year": r[1], "created_at": r[2]} 
        for r in results
    ]
