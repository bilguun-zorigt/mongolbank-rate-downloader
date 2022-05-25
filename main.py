import csv
import pandas
import datetime
from scrapy.crawler import CrawlerProcess
from spider import BoMRate


def main(start_date, end_date):
    # Get List of URLs to scrape
    days = (end_date - start_date).days + 1
    dates = [start_date + datetime.timedelta(days=i) for i in range(days)]
    urls_to_scrape = [
        f"https://www.mongolbank.mn/dblistofficialdailyrate.aspx?vYear={date.year}&vMonth={date.month}&vDay={date.day}"
        for date in dates
    ]

    # Crawl and save result as rates-stacked.csv
    process = CrawlerProcess(
        settings={
            "FEED_URI": "rates-stacked.csv",
            "FEED_FORMAT": "csv",
        }
    )
    process.crawl(BoMRate, start_urls=urls_to_scrape)
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
