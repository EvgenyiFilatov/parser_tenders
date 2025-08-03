from fastapi import FastAPI
import sqlite3
from parse_tenders import parse_tenders

app = FastAPI()


@app.get("/parse-tenders")
def parse_tender():
    parse_tenders()
    return {"message": "Tenders parsed and stored successfully."}


@app.get("/tenders")
def get_tenders(limit: int = 10):
    conn = sqlite3.connect("tenders.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id, tender_number_span, title, delivery_address,
        initial_price, customer_branches, link FROM tenders LIMIT ?""",
        (limit,),
    )
    rows = cursor.fetchall()

    tenders_list = []
    for row in rows:
        tenders_list.append(
            {
                "id": row[0],
                "tender_number_span": row[1],
                "title": row[2],
                "delivery_address": row[3],
                "initial_price": row[4],
                "customer_branches": row[5],
                "link": row[6],
            }
        )

    conn.close()
    return tenders_list
