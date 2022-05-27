import os
import csv
import pandas
from scrapy.crawler import CrawlerProcess
from spider import BoMRate


def scraper(dates, queue):
    # def main(dates, progress_up):
    # Get List of URLs to scrape
    urls_to_scrape = [
        f"https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear={date.year}&vMonth={date.month}&vDay={date.day}"
        for date in dates
    ]

    # remove previous files if exists
    try:
        os.remove("rates-stacked.csv")
    except OSError:
        pass

    try:
        os.remove("rates-unstacked.csv")
    except OSError:
        pass

    # Crawl and save result as rates-stacked.csv
    process = CrawlerProcess(
        settings={
            "FEEDS": {
                "rates-stacked.csv": {"format": "csv"},
                # "rates-stacked.json": {"format": "json"},
            }
        }
    )
    process.crawl(BoMRate, start_urls=urls_to_scrape, queue=queue)
    process.start()

    # Open and sort rates-stacked.csv
    with open("rates-stacked.csv", newline="") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        sortedlist = sorted(
            spamreader, key=lambda row: (row["date"], row["symbol"]), reverse=False
        )

    with open("rates-stacked.csv", "w") as f:
        fieldnames = ["date", "symbol", "rate"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in sortedlist:
            writer.writerow(row)

    # Save rates-unstacked.csv
    dataframe = pandas.read_csv("rates-stacked.csv")
    dataframe.set_index(keys=["date", "symbol"]).unstack().to_csv("rates-unstacked.csv")

    queue.put("done")
