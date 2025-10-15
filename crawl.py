import asyncio
from dotenv import load_dotenv
import os

from crawler.cellphoneS import CellphoneSCrawler
from database.postgresql import PhoneDB

load_dotenv()


if __name__ == "__main__":
    crawled_data_db = PhoneDB(
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "password"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5432),
        database=os.getenv("POSTGRES_DB", "phone_db"),
    )

    # crawled_data_db.reset_table()

    crawler = CellphoneSCrawler(
        base_url=os.getenv("BASE_URL", "https://cellphones.com.vn/mobile.html"),
        database=crawled_data_db,
        headless=True
    )

    asyncio.run(crawler.run())
    crawled_data_db.get_data_ready()
