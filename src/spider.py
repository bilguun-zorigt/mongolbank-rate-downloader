"""
scrapy spiders module
"""
import datetime
import re
import scrapy
from symbols import symbols


def get_date(response):
    """extract date from mongolbank daily rate page and convert to yyyy-mm-dd format"""
    date_text = response.xpath('//*[@id="ContentPlaceHolder1_lblDate"]/text()').get()
    date_parts = re.findall(r"\d+", date_text)
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    return (datetime.datetime.strftime(datetime.date(year, month, day), "%Y-%m-%d"),)


class BoMRate(scrapy.Spider):
    """Mongolbank website exchange rate scrape spider"""

    name = "BoMRate"
    start_urls = None
    queue = None

    def parse(self, response, **kwargs):
        """parse single date page"""
        table = response.xpath('//*[@id="ContentPlaceHolder1_panelExchange"]/ul')
        for currency in table.xpath("li/table/tr"):
            name = currency.xpath("td[2]/text()[1]").extract()[0].replace(",", "")
            symbol = symbols.get(name, name)
            rate = currency.xpath("td[3]/span/text()[1]").extract()[0].replace(",", "")
            yield {"date": get_date(response), "symbol": "".join(symbol), "rate": rate}
        self.queue.put(0)
