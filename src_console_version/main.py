import os
import sys
from datetime import date, datetime, timedelta
from scrapy import Spider, crawler


class BoMRate(Spider):
    name = "BoMRate"
    start_urls = None

    def parse(self, response, **kwargs):
        table = response.xpath('//*[@id="ContentPlaceHolder1_panelExchange"]/ul')
        rates = {}
        for currency in table.xpath("li/table/tr"):
            name = currency.xpath("td[2]/text()[1]").extract()[0].replace(",", "")
            symbol = self.symbols.get(name, name)
            rate = currency.xpath("td[3]/span/text()[1]").extract()[0].replace(",", "")
            rates.update({symbol: rate})
        print("SCRAPED: ", response.request.url[: -len("&date=yyyy-mm-dd")])
        yield {"date": response.request.url[-len("yyyy-mm-dd") :], **rates}

    symbols = {
        "АНУ доллар": "USD",
        "Евро": "EUR",
        "Японы иен": "JPY",
        "Швейцар франк": "CHF",
        "Шведийн крон": "SEK",
        "Английн фунт": "GBP",
        "Болгарын лев": "BGN",
        "Унгарын форинт": "HUF",
        "Египетийн фунт": "EGP",
        "Энэтхэгийн рупи": "INR",
        "Хонгконг доллар": "HKD",
        "ОХУ-ын рубль": "RUB",
        "Казахстан тэнгэ": "KZT",
        "БНХАУ-ын юань": "CNY",
        "БНСУ-ын вон": "KRW",
        "БНАСАУ-ын вон": "KPW",
        "Канадын доллар": "CAD",
        "Австралийн доллар": "AUD",
        "Чех крон": "CZK",
        "Тайван доллар": "TWD",
        "Тайланд бат": "THB",
        "Индонезийн рупи": "IDR",
        "Малайзын ринггит": "MYR",
        "Сингапур доллар": "SGD",
        "АНЭУ-ын дирхам": "AED",
        "Кувейт динар": "KWD",
        "Шинэ Зеланд доллар": "NZD",
        "Данийн крон": "DKK",
        "Польшийн злот": "PLN",
        "Украйны гривн": "UAH",
        "Норвегийн крон": "NOK",
        "Непалын рупи": "NPR",
        "Өмнөд Африкийн ранд": "ZAR",
        "Туркийн лира": "TRY",
        "Вьетнамын донг": "VND",
        "Алт /унцаар/": "XAU",
        "Мөнгө /унцаар/": "XBA",
        "Зээлжих тусгай эрх": "X",
    }


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
