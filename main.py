import datetime
from multiprocessing import Process, Queue
from threading import Thread
from tkinter import *
from tkinter.ttk import Progressbar, Style
from tkcalendar import DateEntry
from scrape import scraper
import webbrowser
import os
import sys


if __name__ == "__main__":
    days_total = 1
    days_scraped = 0
    font = "Arial 14"
    queue = Queue()
    default_end_date = datetime.date.today() - datetime.timedelta(days=2)

    def process_queue(queue):
        global days_total
        global days_scraped
        for i in range(days_total + 1):
            received_item = queue.get()
            if received_item == "done":
                bar["value"] = 100
                button["text"] = "100%. Close"
                button["command"] = root.destroy
                button["state"] = NORMAL
            else:
                days_scraped += 1
                percent_value = round((days_scraped / days_total) * 100, 2)
                percent_value = percent_value if percent_value >= 1 else 1
                percent_value = percent_value if percent_value <= 99 else 99
                bar["value"] = percent_value
                button["text"] = f"{percent_value}%"

    def start():
        # DISABLE FORMS
        entry_from["state"] = DISABLED
        entry_to["state"] = DISABLED
        button["state"] = DISABLED
        button["text"] = f"{0}%"

        # DATE VARIABLES
        start_date = entry_from.get_date()
        end_date = entry_to.get_date()
        global default_end_date
        if end_date > default_end_date:
            end_date = default_end_date
        global days_total
        days_total = days_total + (end_date - start_date).days
        dates = [start_date + datetime.timedelta(days=day) for day in range(days_total)]

        # CALL SCRAPING PROCESS
        Process(target=scraper, kwargs={"dates": dates, "queue": queue}).start()
        Thread(target=process_queue, args=(queue,)).start()

    root = Tk()
    root.title("BoM Rate Scraper")

    filename = "logo.png"
    # if "_MEIPASS2" in os.environ:
    # filename = os.path.join(os.environ["_MEIPASS2"], filename)
    # logo = PhotoImage(file=filename)
    if getattr(sys, "frozen", False):
        logo = PhotoImage(file=os.path.join(sys._MEIPASS, filename))
    else:
        logo = PhotoImage(file=filename)
    root.tk.call("wm", "iconphoto", root._w, logo)

    style = Style()
    style.configure("green.Horizontal.TProgressbar", background="green")
    bar = Progressbar(
        root,
        style="green.Horizontal.TProgressbar",
        orient="horizontal",
        mode="determinate",
        length=400,
    )
    label_from = Label(root, font=font, text="From:")
    label_to = Label(root, font=font, text="To:")
    entry_from = DateEntry(
        root,
        font=font,
        date_pattern="yyyy-mm-dd",
        year=default_end_date.year - 1,
        month=12,
        day=25,
    )
    entry_to = DateEntry(
        root,
        font=font,
        date_pattern="yyyy-mm-dd",
        year=default_end_date.year,
        month=default_end_date.month,
        day=default_end_date.day,
    )
    button = Button(root, font=font, text="Start Scraping", command=start)

    bar.grid(row=2, columnspan=2, padx=50, pady=(25, 5))
    label_from.grid(row=0, column=0, padx=(0, 5), pady=(50, 25), sticky="e")
    label_to.grid(row=1, column=0, padx=(0, 5), pady=(25, 25), sticky="e")
    entry_from.grid(row=0, column=1, padx=(5, 0), pady=(50, 25))
    entry_to.grid(row=1, column=1, padx=(5, 0), pady=(25, 25))
    button.grid(row=4, columnspan=2, sticky="", pady=(25, 25))
    label_copyright = Label(
        root,
        # font="Arial 12",
        text="All Rights Reserved.\nBilguun Zorigt. 2022",
    ).grid(row=5, columnspan=2, sticky="", pady=(25, 5))

    link = Label(
        root, text="https://github.com/bilguun-zorigt", fg="blue", cursor="hand2"
    )
    link.grid(row=6, columnspan=2, sticky="", pady=(5, 50))
    link.bind(
        "<Button-1>", lambda e: webbrowser.open_new("https://github.com/bilguun-zorigt")
    )

    root.mainloop()
