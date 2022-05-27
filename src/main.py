"""
main module to start GUI, processes, and threads
"""
import os
import sys
import datetime
import webbrowser
from threading import Thread
from multiprocessing import Process, Queue
from tkinter import Tk, Label, Button, PhotoImage, NORMAL, DISABLED
from tkinter.ttk import Progressbar, Style
from tkcalendar import DateEntry
from scrape import scraper


class Main:
    """Main"""

    DEFAULT_END_DATE = datetime.date.today() - datetime.timedelta(days=2)

    def __init__(self):
        self.root = Tk()
        self.root.title("BoM Rate Scraper")

        filename = "logo.png"
        if getattr(sys, "frozen", False):
            logo = PhotoImage(file=os.path.join(sys._MEIPASS, filename))
        else:
            logo = PhotoImage(file=filename)
        self.root.tk.call("wm", "iconphoto", self.root._w, logo)

        font = "Arial 14"
        style = Style()
        style.configure("green.Horizontal.TProgressbar", background="green")
        self.pbar = Progressbar(
            self.root,
            style="green.Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate",
            length=400,
        )
        label_from = Label(self.root, font=font, text="From:")
        label_to = Label(self.root, font=font, text="To:")
        self.entry_from = DateEntry(
            self.root,
            font=font,
            date_pattern="yyyy-mm-dd",
            year=self.DEFAULT_END_DATE.year - 1,
            month=12,
            day=25,
        )
        self.entry_to = DateEntry(
            self.root,
            font=font,
            date_pattern="yyyy-mm-dd",
            year=self.DEFAULT_END_DATE.year,
            month=self.DEFAULT_END_DATE.month,
            day=self.DEFAULT_END_DATE.day,
        )
        self.button = Button(self.root, font=font, text="Start", command=self.start)

        self.pbar.grid(row=2, columnspan=2, padx=50, pady=(25, 5))
        label_from.grid(row=0, column=0, padx=(0, 5), pady=(50, 25), sticky="e")
        label_to.grid(row=1, column=0, padx=(0, 5), pady=(25, 25), sticky="e")
        self.entry_from.grid(row=0, column=1, padx=(5, 0), pady=(50, 25))
        self.entry_to.grid(row=1, column=1, padx=(5, 0), pady=(25, 25))
        self.button.grid(row=4, columnspan=2, sticky="", pady=(25, 25))

        Label(
            self.root,
            text="All Rights Reserved.\nBilguun Zorigt. 2022",
        ).grid(row=5, columnspan=2, sticky="", pady=(25, 5))

        link = Label(
            self.root,
            text="https://github.com/bilguun-zorigt",
            fg="blue",
            cursor="hand2",
        )
        link.grid(row=6, columnspan=2, sticky="", pady=(5, 50))
        link.bind(
            "<Button-1>",
            lambda e: webbrowser.open_new("https://github.com/bilguun-zorigt"),
        )

        self.root.mainloop()

    def process_queue(self, queue, days_total):
        """
        Receive message from Scraping process
        and update GUI in the main process
        """
        days_scraped = 0
        for _ in range(days_total + 2):
            received_item = queue.get()
            if received_item == 100:
                self.pbar["value"] = 100
                self.button["text"] = "100%. Close"
                self.button["command"] = self.root.destroy
                self.button["state"] = NORMAL
            elif received_item > 0:
                self.pbar["value"] = received_item
                self.button["text"] = f"{received_item}%"
            else:
                days_scraped += 1
                percent_value = round((days_scraped / days_total) * 100, 2)
                percent_value = percent_value if percent_value <= 99 else 99
                self.pbar["value"] = percent_value
                self.button["text"] = f"{percent_value}%"

    def start(self):
        """
        Start scraping process
        and start queue handler in separate thread in the main process
        to update GUI in the main thread in main process
        """
        # DISABLE FORMS
        self.entry_from["state"] = DISABLED
        self.entry_to["state"] = DISABLED
        self.button["state"] = DISABLED
        self.button["text"] = f"{0}%"

        # DATE VARIABLES
        start_date = self.entry_from.get_date()
        end_date = self.entry_to.get_date()
        if end_date > self.DEFAULT_END_DATE:
            end_date = self.DEFAULT_END_DATE
        days_total = (end_date - start_date).days + 1
        dates = [start_date + datetime.timedelta(days=day) for day in range(days_total)]

        # CALL SCRAPING PROCESS
        queue = Queue()
        Process(target=scraper, kwargs={"dates": dates, "queue": queue}).start()
        Thread(target=self.process_queue, args=(queue, days_total)).start()


if __name__ == "__main__":
    Main()
