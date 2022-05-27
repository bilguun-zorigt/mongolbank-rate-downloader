import os
import sys
from datetime import date, datetime, timedelta
from scrapy import Spider, Request, crawler


class BoMRate(Spider):
    name = "BoMRate"
    date_ints = []

    def start_requests(self):
        for year, month, day in self.date_ints:
            url_params = f"vYear={year}&vMonth={month}&vDay={day}"
            url = f"https://www.mongolbank.mn/dblistofficialdailyrate.aspx?{url_params}"
            yield Request(
                url,
                dont_filter=True,
                callback=self.parse,
                cb_kwargs={
                    "date_str": f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
                },
            )

    def parse(self, response, **kwargs):
        table = response.xpath('//*[@id="ContentPlaceHolder1_panelExchange"]/ul')
        rates = {}
        for currency in table.xpath("li/table/tr"):
            name = currency.xpath("td[2]/text()[1]").extract()[0].replace(",", "")
            symbol = self.symbols.get(name, name)
            rate = currency.xpath("td[3]/span/text()[1]").extract()[0].replace(",", "")
            rates.update({symbol: rate})
        date_str = kwargs.get("date_str")
        print("scraped ", date_str)
        yield {"date": date_str, **rates}

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


def print_copyright():
    print("All Right Reserved.")
    print("Bilguun Zorigt. 2022")
    print("https://github.com/bilguun-zorigt")
    print("")


if __name__ == "__main__":
    print_copyright()
    # get user input and generate list of dates
    INPUT_DATE_1 = str(input("Enter date to download from (yyyy-mm-dd): "))
    INPUT_DATE_2 = str(input("Enter date to download to (yyyy-mm-dd): "))
    date1 = datetime.strptime(INPUT_DATE_1, "%Y-%m-%d").date()
    date2 = datetime.strptime(INPUT_DATE_2, "%Y-%m-%d").date()
    start_date = min(date1, date2)
    end_date = max(date1, date2)
    date_before_yesterday = date.today() - timedelta(days=2)
    end_date = date_before_yesterday if end_date > date_before_yesterday else end_date
    number_of_days = (end_date - start_date).days + 1
    dates = [start_date + timedelta(days=day) for day in range(number_of_days)]
    date_ints = [(d.year, d.month, d.day) for d in dates]

    # get filepath - determine if application is a script file or frozen exe
    if getattr(sys, "frozen", False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    FILENAME = (
        f"BoM Rates {start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.csv"
    )
    FILEPATH = os.path.join(application_path, FILENAME)

    # remove previous files if exists
    try:
        os.remove(FILEPATH)
    except OSError:
        pass

    # Crawl and save result as rates-stacked.csv
    process = crawler.CrawlerProcess(
        settings={
            # "LOG_LEVEL": "ERROR",
            "FEEDS": {FILENAME: {"format": "csv"}},
        }
    )
    process.crawl(BoMRate, date_ints=date_ints)
    print("")
    print("***** Starting *****")
    process.start()
    print("******* Done *******", " File saved to: ", FILEPATH)
    print("")
    print_copyright()

    a = input("Press enter to exit...")
    if a:
        exit(0)
