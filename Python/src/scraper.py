import asyncio
import aiohttp
import bs4


class ScrapeConcurrently:
    symbols_ordered = []
    dates_symbols_rates = {}
    session = None
    progress_callback = None

    def __init__(self, dates, progress_callback):
        self.progress_callback = progress_callback
        asyncio.run(self.scrape_concurrently(dates))

    async def scrape_concurrently(self, dates):
        async with aiohttp.ClientSession() as session:
            self.session = session
            await asyncio.gather(*[self.request(date) for date in dates])

    async def request(self, date):
        url_params = f"?vYear={date.year}&vMonth={date.month}&vDay={date.day}"
        url = "https://www.mongolbank.mn/dblistofficialdailyrate.aspx" + url_params

        async with self.session.get(url) as response:
            doc = await response.text()
            self.parse(date, doc)
            self.progress_callback()

    def parse(self, date, doc):
        span_id_prefix = "ContentPlaceHolder1_lbl"
        elements = bs4.BeautifulSoup(doc, "html.parser").select(
            f".uk-comment-list span[id^={span_id_prefix}]"
        )
        symbols_rates = {}
        for element in elements:
            symbol = element.get("id")[len(span_id_prefix) :]
            if symbol not in self.symbols_ordered:
                self.symbols_ordered.append(symbol)
            rate_text = element.get_text()
            if rate_text != "":
                rate = float(rate_text.replace(",", ""))
                symbols_rates.update({symbol: rate})

        self.dates_symbols_rates.update({date: symbols_rates})
