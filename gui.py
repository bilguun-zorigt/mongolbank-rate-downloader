from tkinter import *
from tkcalendar import DateEntry
from main import main

root = Tk()
root.title("BoM Rate Scraper")
font = "Arial 14"


label_start = Label(root, font=font, text="From:")
label_start.grid(row=0, column=0, padx=(50, 5), pady=(50, 25), sticky="e")
start_date = DateEntry(
    root,
    font=font,
    date_pattern="yyyy-mm-dd",
)
start_date.grid(row=0, column=1, padx=(5, 50), pady=(50, 25))


label_end = Label(root, font=font, text="To:")
label_end.grid(row=1, column=0, padx=(50, 5), pady=(25, 25), sticky="e")
end_date = DateEntry(
    root,
    font=font,
    date_pattern="yyyy-mm-dd",
)
end_date.grid(row=1, column=1, padx=(5, 50), pady=(25, 25))


Button(
    root,
    font=font,
    text="Start Scraping",
    command=lambda: main(start_date.get_date(), end_date.get_date()),
).grid(row=2, columnspan=2, sticky="", pady=(25, 50))


root.mainloop()
