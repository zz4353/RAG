import psycopg
from psycopg.types.json import Json
import os
from pathlib import Path
import re


class PhoneDB:
    def __init__(self,
                 user: str,
                 password: str,
                 host: str,
                 port: int = 5432,
                 database: str = "phone_db"
                 ):
        self.connection = psycopg.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS phones (
                           id SERIAL PRIMARY KEY,
                           url TEXT UNIQUE,
                           title TEXT,
                           price TEXT,
                           colors TEXT[],
                           specs JSONB,
                           images TEXT[],
                           description TEXT
                       )""")

    def insert(self, infos: dict):
        self.cursor.execute("""
            INSERT INTO phones (url, title, price, colors, specs, images, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (url) DO UPDATE
            SET title = EXCLUDED.title,
                price = EXCLUDED.price,
                colors = EXCLUDED.colors,
                specs = EXCLUDED.specs,
                images = EXCLUDED.images,
                description = EXCLUDED.description
            """, (
            infos.get("url"),
            infos.get("title"),
            infos.get("price"),
            infos.get("colors"),
            Json(infos.get("specs")),
            infos.get("images"),
            infos.get("description")
        ))

    def get_all_data(self):
        self.cursor.execute("SELECT * FROM phones")
        return self.cursor.fetchall()
    
    def reset_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS phones")
        self.cursor.execute("""CREATE TABLE phones (
                           id SERIAL PRIMARY KEY,
                           url TEXT UNIQUE,
                           title TEXT,
                           price TEXT,
                           colors TEXT[],
                           specs JSONB,
                           images TEXT[],
                           description TEXT
                       )""")

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_multiple_cols_data(self, columns: list):
        cols = ", ".join(columns)
        self.cursor.execute(f"SELECT {cols} FROM phones")
        return self.cursor.fetchall()
    
    def get_data_ready(self):
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        
        data = self.get_all_data()
        
        for row in data:
            document = row[2]
            
            safe_name = re.sub(r'[\\/:"*?<>|]+', "_", document)
            document = Path(f"{output_dir}/{safe_name}.md")
            
            document_content = ""
            
            product_name = f"**Tên sán phẩm:** {row[2]}\n"
            product_price = f"**Giá sản phẩm:** {row[3]}\n"
            
            colors = ", ".join(row[4])
            product_colors = f"**Các màu của sản phẩm:** {colors}\n"
            product_infos = f"**Thông số sản phẩm: {self._process_product_infos(row[5])}"
            
            pr = row[7].strip()
            product_pr = f"**Giới thiệu sản phẩm:** {pr}\n"
            
            document_content += product_name
            document_content += product_price
            document_content += product_colors
            document_content += product_infos
            document_content += product_pr
            
            self._write_data_file(content=document_content, file_path=document)

    def _process_product_infos(self, product_infos):
        result = ""
        
        for key, value in product_infos.items():
            result += f"{key}: {value}\n"
        return result
    
    def _write_data_file(self, content, file_path):
        with open(file_path, "w") as f:
            f.write(content)
