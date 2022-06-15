import math
import time
import datetime as dt
from scraper import ScrapeConcurrently


class Main:
    start_date = None
    end_date = None
    file_name = None
    total_days = None
    done_days = 0

    def __init__(self):
        self.welcome_message()

        dates_ordered = self.get_dates()
        self.total_days = len(dates_ordered)

        scraping_start_time = time.time()
        scraped = ScrapeConcurrently(dates_ordered, self.update_progress_bar)
        scraping_duration = time.time() - scraping_start_time

        convertion_start_time = time.time()
        csv_string = self.get_csv_string(
            scraped.symbols_ordered, dates_ordered, scraped.dates_symbols_rates
        )
        convertion_duration = time.time() - convertion_start_time

        csv_write_start_time = time.time()
        self.write_csv_file(csv_string)
        csv_write_duration = time.time() - csv_write_start_time

        self.success_message()

        print("Reports:")
        self.print_duration("Scraping:    ", scraping_duration)
        self.print_duration("Convertion:  ", convertion_duration)
        self.print_duration("CSV creation:", csv_write_duration)

    def welcome_message(self):
        print("Source code at: \033[34mhttps://github.com/bilguun-zorigt\033[0m")

    def get_date_input(self, message):
        while True:
            date_string = str(input(f"\033[0m{message}\033[34m"))
            try:
                return dt.datetime.strptime(date_string, "%Y-%m-%d").date()
            except:  # pylint: disable=bare-except
                print(
                    "\033[31mDate entered is not valid. "
                    "Must be formatted as yyyy-mm-dd\033[0m"
                )

    def get_dates(self):
        self.start_date = self.get_date_input("Enter start date (yyyy-m-d): ")
        self.end_date = self.get_date_input("Enter end date (yyyy-m-d): ")
        number_of_days = (self.end_date - self.start_date).days + 1
        return [
            self.start_date + dt.timedelta(days=day) for day in range(number_of_days)
        ]

    def update_progress_bar(self):
        self.done_days += 1
        pb_length = 25
        done_length = int(self.done_days * (pb_length / self.total_days))
        done_length_string = "█" * done_length
        remaining_length_string = "█" * (pb_length - done_length)
        percent_string = round(self.done_days / self.total_days * 100, 2)

        # https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
        print(
            f"\r\033[0mCurrent progress: \033[34m{done_length_string}\033[41;31m{remaining_length_string}\033[0m\033[34m {self.done_days}/{self.total_days} {percent_string}%\033[0m",
            end="",
        )

    def get_csv_string(self, symbols_ordered, dates_ordered, dates_symbols_rates):
        csv_string = "Date"
        for symbol in symbols_ordered:
            csv_string += "," + symbol

        for date in dates_ordered:
            date_string = date.isoformat()
            csv_string += "\n" + date_string
            for symbol in symbols_ordered:
                rate_string = f"{dates_symbols_rates[date].get(symbol, 0)}"
                rate_string = rate_string.rstrip("0").rstrip(".")
                if rate_string == "0":
                    rate_string = ""
                csv_string += "," + rate_string

        return csv_string

    def write_csv_file(self, csv_string):
        self.file_name = f"BoM Rates {self.start_date.strftime('%Y%m%d')}-{self.end_date.strftime('%Y%m%d')}.csv"
        open_file = open(self.file_name, "w")  # pylint: disable=unspecified-encoding
        open_file.write(csv_string)
        open_file.close()

    def success_message(self):
        print(f"\nFile saved: '\033[34m{self.file_name}\033[0m'\n")

    def print_duration(self, operation_name, duration_time):
        print(
            f"{operation_name} \033[34m{round(duration_time,2)}\033[0m seconds or \033[34m{int(duration_time*1000)}\033[0m milliseconds or \033[34m{int(duration_time*1000000)}\033[0m microseconds"
        )


if __name__ == "__main__":
    Main()
