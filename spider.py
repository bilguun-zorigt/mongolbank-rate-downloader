import datetime
import scrapy
import re
from translation import symbols


def get_date(response):
    date_text = response.xpath('//*[@id="ContentPlaceHolder1_lblDate"]/text()').get()
    date_parts = re.findall(r"\d+", date_text)
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    return (datetime.datetime.strftime(datetime.date(year, month, day), "%Y-%m-%d"),)


class BoMRate(scrapy.Spider):
    name = "BoMRate"
    start_urls = None

    def parse(self, response):
        table = response.xpath('//*[@id="ContentPlaceHolder1_panelExchange"]/ul')
        for currency in table.xpath("li/table/tr"):
            name = currency.xpath("td[2]/text()[1]").extract()[0].replace(",", "")
            symbol = symbols.get(name, name)
            rate = currency.xpath("td[3]/span/text()[1]").extract()[0].replace(",", "")
            yield {"date": get_date(response), "symbol": "".join(symbol), "rate": rate}
        self.queue.put(1)
