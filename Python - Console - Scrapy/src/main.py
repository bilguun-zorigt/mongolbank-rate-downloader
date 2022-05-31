import os
import sys
from datetime import date, datetime, timedelta
from scrapy import Spider, crawler


class BoMRate(Spider):
    name = "BoMRate"
    start_urls = None

    def parse(self, response, **kwargs):
        span_id_prefix = "ContentPlaceHolder1_lbl"
        elements = response.css(f".uk-comment-list span[id^={span_id_prefix}]")
        rates = {}
        for element in elements:
            symbol = element.css("::attr(id)").get()[len(span_id_prefix) :]
            rate = element.css("::text").get().replace(",", "")
            rates.update({symbol: rate})
        print("SCRAPED: ", response.request.url[: -len("&date=yyyy-mm-dd")])
        yield {"date": response.request.url[-len("yyyy-mm-dd") :], **rates}


if __name__ == "__main__":
    INFO = "Source code at: https://github.com/bilguun-zorigt\n"
    print(INFO)
    # get user input and generate list of dates
    INPUT_DATE_1 = str(input("Enter date to download from (yyyy-mm-dd): "))
    INPUT_DATE_2 = str(input("Enter date to download to (yyyy-mm-dd): "))
    date1 = datetime.strptime(INPUT_DATE_1, "%Y-%m-%d").date()
    date2 = datetime.strptime(INPUT_DATE_2, "%Y-%m-%d").date()
    start_date = min(date1, date2)
    end_date = min(max(date1, date2), date.today() - timedelta(days=2))
    number_of_days = (end_date - start_date).days + 1
    dates = [start_date + timedelta(days=day) for day in range(number_of_days)]
    date_parts = [(d.year, str(d.month).zfill(2), str(d.day).zfill(2)) for d in dates]
    start_urls = [
        "https://www.mongolbank.mn/dblistofficialdailyrate.aspx?"
        f"vYear={year}&vMonth={month}&vDay={day}&date={year}-{month}-{day}"
        for year, month, day in date_parts
    ]

    # get filepath - determine if application is a script file or frozen exe
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    FN = f"Rates {start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.csv"
    FILEPATH = os.path.join(application_path, FN)

    # remove previous files if exists
    try:
        os.remove(FILEPATH)
    except OSError:
        pass

    # Crawl and save result as rates-stacked.csv
    print("\n***** Starting...")
    process = crawler.CrawlerProcess(
        settings={
            "LOG_LEVEL": "ERROR",
            "FEEDS": {FN: {"format": "csv"}},
        }
    )
    process.crawl(BoMRate, start_urls=start_urls)
    process.start()
    print("***** Done. File saved to: ", FILEPATH, "\n")
    print(INFO)

    a = input("Press enter to exit...")
    if a:
        exit(0)
