import argparse
import sqlite3


def main():
    # Настройка аргументов командной строки, добавил опцию --limit
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
    )
    args = parser.parse_args()

    conn = sqlite3.connect("tenders.db")
    cursor = conn.cursor()

    cursor.execute(
        """SELECT id,
        tender_number_span,
        title,
        delivery_address,
        initial_price,
        customer_branches,
        link
        FROM tenders LIMIT ?""",
        (args.limit,),
    )
    rows = cursor.fetchall()
    conn.close()

    print(
        f"{'ID':<5}{'Номер':<20}{'Название':<50}{'Адрес':<18}"
        f"{'Цена':<15}{'Категории':<40}{'Ссылка':<50}"
    )
    # Выводим строки из БД используя срезы для сокращения
    for row in rows:
        print(
            f"{row[0]:<5}"
            f"{row[1][26:]:<20}"
            f"{row[2][7:55]:<50}"
            f"{row[3][:15]:<18}"
            f"{row[4]:<15}"
            f"{row[5][:35]:<40}"
            f"{row[6][:40]:<10}"
        )


if __name__ == "__main__":
    main()
