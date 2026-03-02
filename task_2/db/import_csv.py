import csv

import psycopg2
from psycopg2.extras import execute_values

from logger import logger


class PostgresImporter:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.conn_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self._create_table()

    def _create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            file_type TEXT,
            content TEXT
        );
        """
        create_index_sql = """
        CREATE INDEX IF NOT EXISTS idx_fts_content ON documents USING GIN (to_tsvector('russian', content));
        """
        conn = psycopg2.connect(**self.conn_params)
        cur = conn.cursor()
        cur.execute(create_table_sql)
        cur.execute(create_index_sql)
        conn.commit()
        cur.close()
        conn.close()

    def import_csv(self, csv_path):
        conn = psycopg2.connect(**self.conn_params)
        cur = conn.cursor()

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = [(row['file_path'], row['file_name'], row['file_type'], row['content']) for row in reader]

        insert_sql = """
        INSERT INTO documents (file_path, file_name, file_type, content)
        VALUES %s
        """
        execute_values(cur, insert_sql, rows)
        conn.commit()
        logger.info(f"Записано {len(rows)} строк в бд.")
        cur.close()
        conn.close()