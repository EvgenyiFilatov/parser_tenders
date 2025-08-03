import requests
from bs4 import BeautifulSoup
import sqlite3

from constants import (
    BASE_URL,
    BEGIN_PAGE_NUMBERS,
    TENDERS_FETCHED,
    MAX_TENDERS
)


def parse_tenders():
    conn = sqlite3.connect("tenders.db")
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS tenders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tender_number_span TEXT,
        title TEXT,
        delivery_address TEXT,
        initial_price TEXT,
        customer_branches TEXT,
        link TEXT
    )"""
    )

    # Очистка всех данных из таблицы в начале каждого запуска
    cursor.execute("DELETE FROM tenders")

    base_url = BASE_URL
    page_number = BEGIN_PAGE_NUMBERS
    tenders_fetched = TENDERS_FETCHED
    max_tenders = MAX_TENDERS

    while tenders_fetched < max_tenders:
        url = f"{base_url}{page_number}"
        response = requests.get(url)
        page_content = response.text
        soup = BeautifulSoup(page_content, "html.parser")

        tender_articles = soup.find_all("article")

        if not tender_articles:
            break

        for row in tender_articles:
            if tenders_fetched >= max_tenders:
                break

            tender_info = row.find("div", class_="tender__info")
            tender_number_span_tag = tender_info.find(
                "span", class_="tender__number"
            )
            tender_number_span = (
                " ".join(tender_number_span_tag.get_text(strip=True).split())
                if tender_number_span_tag
                else "Не найден номер"
            )

            title_link_tag = tender_info.find("a")
            title = (
                title_link_tag["title"]
                if title_link_tag and "title" in title_link_tag.attrs
                else "Не найдено название"
            )
            title_link = (
                f"https://rostender.info{title_link_tag['href']}"
                if title_link_tag and "href" in title_link_tag.attrs
                else ""
            )

            address_column = row.find("div", class_="delivery-address-column")
            address_div = (
                address_column.find("div", class_="line-clamp line-clamp--n3")
                if address_column
                else None
            )
            delivery_address = (
                address_div.get_text(
                    strip=True
                ) if address_div else "Не найден адрес"
            )

            price_column = row.find("div", class_="price-column")
            price_div = (
                price_column.find(
                    "div", class_="starting-price__price starting-price--price"
                )
                if price_column
                else None
            )
            initial_price = (
                price_div.get_text(
                    strip=True
                ) if price_div else "Не найдена цена"
            )

            customer_branches_column = row.find(
                "div", class_="customer-branches-column"
            )
            customer_branches_ul = (
                customer_branches_column.find("ul", class_="list-branches__ul")
                if customer_branches_column
                else None
            )
            customer_branches = (
                ", ".join(
                    li.get_text(
                        strip=True
                    ) for li in customer_branches_ul.find_all("li")
                )
                if customer_branches_ul
                else "Не найдена информация о категориях заказчиков"
            )

            cursor.execute(
                """
            INSERT INTO tenders (
            tender_number_span,
            title, delivery_address,
            initial_price,
            customer_branches, link
            )
            VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    tender_number_span,
                    title,
                    delivery_address,
                    initial_price,
                    customer_branches,
                    title_link,
                ),
            )

            tenders_fetched += 1

        page_number += 1

    conn.commit()
    conn.close()


if __name__ == "__main__":
    parse_tenders()
