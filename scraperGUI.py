import tkinter as tk
import requests
from pageNav import pageNavigation
from tkinter.filedialog import askopenfilename, asksaveasfilename
from csvWriter import writeCSV
import re

class scraperGUI:

    def __init__(self):
        self.datalist = [[]]

    def handleScrapeButton(self):
        url = self.searchBoxEntry.get()

        response = requests.get(url)

        if response.status_code != 200:
            self.notificationLabel["text"] = u"URL is not valid and or doesn't exists on the internet"
            print("URL does not exist on Internet")
        else:
            self.notificationLabel["text"] = u"URL is valid and exists on the internet. Now scraping..."
            pagenav = pageNavigation(url)
            self.datalist = pagenav.main_page_navigation()
            self.notificationLabel["text"] = u"Scraping finished! Click Save to make .csv result."

    def handleSaveButton(self):
        filepath = asksaveasfilename(
            defaultextension="csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
        )
        if not filepath:
            return
        self.saveBoxEntry["text"] = filepath
        writeCSV(self.datalist, filepath)

    def showDialogue(self):

        self.window = tk.Tk()
        self.window.title("eBay Scraper")
        self.topFrame = tk.Frame(master=self.window, borderwidth=5)
        self.searchBoxLabel = tk.Label(master=self.topFrame, text="eBay URLs Here...", width=20)
        self.searchBoxLabel.pack(side=tk.LEFT, padx=5, pady=5)
        self.searchBoxEntry = tk.Entry(master=self.topFrame, width = 100)
        self.searchBoxEntry.pack(side=tk.LEFT, padx=5, pady=5)
        self.searchButton = tk.Button(master=self.topFrame, text="Scrape", width=20, command=self.handleScrapeButton)
        self.searchButton.pack(side=tk.LEFT, padx=5, pady=5)
        self.topFrame.pack(side=tk.TOP)

        self.middleFrame = tk.Frame(master=self.window, borderwidth=5)
        self.saveBoxLabel = tk.Label(master=self.middleFrame, text=".csv File Path Here...", width=20)
        self.saveBoxLabel.pack(side=tk.LEFT, padx=5, pady=5)
        self.saveBoxEntry = tk.Entry(master=self.middleFrame, width = 100)
        self.saveBoxEntry.pack(side=tk.LEFT, padx=5, pady=5)
        self.saveBoxButton = tk.Button(master=self.middleFrame, text="Save", width=20, command=self.handleSaveButton)
        self.saveBoxButton.pack(side=tk.LEFT, padx=5, pady=5)
        self.middleFrame.pack(side=tk.TOP)

        self.notificationLabel = tk.Label(master=self.window, borderwidth=5, text="")
        self.notificationLabel.pack(side=tk.TOP)

        # self.searchButton.bind("<Button-1>", self.handleScrapeButton())

        self.window.mainloop()
