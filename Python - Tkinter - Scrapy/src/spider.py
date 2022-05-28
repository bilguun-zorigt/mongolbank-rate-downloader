"""
scrapy spiders module
"""
import scrapy
from symbols import symbols


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
            yield {
                "date": response.request.url[-len("yyyy-mm-dd") :],
                "symbol": symbol,
                "rate": rate,
            }
        self.queue.put(0)
