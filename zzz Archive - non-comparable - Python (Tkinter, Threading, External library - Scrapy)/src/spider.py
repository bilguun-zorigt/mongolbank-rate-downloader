"""
scrapy spiders module
"""
import scrapy


class BoMRate(scrapy.Spider):
    """Mongolbank website exchange rate scrape spider"""

    name = "BoMRate"
    start_urls = None
    queue = None

    def parse(self, response, **kwargs):
        """parse single date page"""
        span_id_prefix = "ContentPlaceHolder1_lbl"
        elements = response.css(f".uk-comment-list span[id^={span_id_prefix}]")
        date = response.request.url[-len("yyyy-mm-dd") :]
        for element in elements:
            symbol = element.css("::attr(id)").get()[len(span_id_prefix) :]
            rate = element.css("::text").get().replace(",", "")
            yield {
                "date": date,
                "symbol": symbol,
                "rate": rate,
            }
        self.queue.put(0)
