"""
module for starting the scrapy spider and transforming the results
"""
import os
import sys
import csv
import pandas
from scrapy.crawler import CrawlerProcess
from spider import BoMRate


def scraper(dates, queue):
    """
    Args:
        dates (list):
            list of dates to scrape
        queue (multiprocessing Queue class instance):
            send message to GUI process to update progressbar
    """
    # Get List of URLs to scrape
    urls_to_scrape = [
        "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?"
        f"vYear={date.year}&vMonth={date.month}&vDay={date.day}"
        f"&date={date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"
        for date in dates
    ]

    # get filepath - determine if application is a script file or frozen exe
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    stacked_filename = os.path.join(application_path, "rates-stacked.csv")
    unstacked_filename = os.path.join(application_path, "rates-unstacked.csv")

    # remove previous files if exists
    try:
        os.remove(stacked_filename)
    except OSError:
        pass

    try:
        os.remove(unstacked_filename)
    except OSError:
        pass
    queue.put(1)

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
    with open(stacked_filename, encoding="utf-8", newline="") as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=",")
        sortedlist = sorted(
            spamreader, key=lambda row: (row["date"], row["symbol"]), reverse=False
        )

    with open(
        stacked_filename,
        "w",
        encoding="utf-8",
    ) as csvfile:
        fieldnames = ["date", "symbol", "rate"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in sortedlist:
            writer.writerow(row)

    # Save rates-unstacked.csv
    dataframe = pandas.read_csv(stacked_filename)
    dataframe.set_index(keys=["date", "symbol"]).unstack().to_csv(unstacked_filename)

    queue.put(100)
