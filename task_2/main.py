import argparse

import os

from generator.generate_files import FileGenerator
from crawler.crawler import Crawler
from db.import_csv import PostgresImporter

from logger import logger


def main():
    parser = argparse.ArgumentParser(description="Document crawler and search index builder")
    parser.add_argument("--generate", action="store_true", help="Generate test files")
    parser.add_argument("--crawl", action="store_true", help="Crawl directory and save to CSV")
    parser.add_argument("--import-db", action="store_true", help="Import CSV to PostgreSQL")
    parser.add_argument("--root-dir", type=str, default="./test_files", help="Root directory to crawl")
    parser.add_argument("--output-csv", type=str, default="./output/result.csv", help="Output CSV file path")
    parser.add_argument("--dbname", type=str, default="mydb", help="PostgreSQL database name")
    parser.add_argument("--user", type=str, default="user", help="PostgreSQL user")
    parser.add_argument("--password", type=str, default="password", help="PostgreSQL password")
    parser.add_argument("--host", type=str, default="localhost", help="PostgreSQL host")
    parser.add_argument("--port", type=int, default=5432, help="PostgreSQL port")

    args = parser.parse_args()

    if args.generate:
        logger.info("генерация тестовых файлов...")
        gen = FileGenerator(output_dir=args.root_dir)
        gen.generate_all()
        logger.info(f"Тестовые файлы сгенерированы в {args.root_dir}")

    if args.crawl:
        logger.info("Старт обходчика...")
        crawler = Crawler(root_dir=args.root_dir)
        data = crawler.crawl()
        os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)
        crawler.save_to_csv(data, args.output_csv)
        logger.info(f"Обход выполнен. Результаты в  {args.output_csv}")

    if args.import_db:
        logger.info("Импорт данных в PostgreSQL...")
        importer = PostgresImporter(
            dbname=args.dbname,
            user=args.user,
            password=args.password,
            host=args.host,
            port=args.port
        )
        importer.import_csv(args.output_csv)
        logger.info("Импорт завершен.")

    if not (args.generate or args.crawl or args.import_db):
        parser.print_help()


if __name__ == "__main__":
    main()