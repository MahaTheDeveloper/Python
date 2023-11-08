import csv
import time
import threading
import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

# Global variables
CHROMEDRIVER_PATH = "C:\\chromedriver\\chromedriver-win64\\chromedriver.exe"
URL = 'https://www.amazon.com/Best-Sellers/zgbs'
scraping = False  # Flag to indicate if scraping is in progress
results = []  # To store the scraped data

# Define a function to extract product titles from the Amazon Best Sellers page
def extract_product_titles(url):
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.get(url)
    time.sleep(2)  # Adjust the wait time for the page to load completely

    # Use BeautifulSoup to parse the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find all product titles on the page
    product_titles = soup.find_all('div', {'class': 'p13n-sc-truncate-desktop-type2'})

    # Extract the text content of the product titles
    titles = [title.get_text(strip=True) for title in product_titles]

    driver.quit()
    return titles

# Define a function to start the scraping process
def start_scraping():
    global scraping, results
    scraping = True
    results = extract_product_titles(URL)
    scraping = False

# Define a function to save results to a CSV file
def save_to_csv():
    if results:
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
                fieldnames = ['Product Title']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for title in results:
                    writer.writerow({'Product Title': title})

# Create a GUI window
window = tk.Tk()
window.title("Web Scraping Automation")

# Create a Chrome service and set the executable path
chrome_service = Service(CHROMEDRIVER_PATH)

# Create a Chrome web driver with the service
chrome_options = webdriver.ChromeOptions()

# Create Start and Stop buttons
start_button = tk.Button(window, text="Start Scraping", command=start_scraping)
stop_button = tk.Button(window, text="Stop Scraping", command=window.quit)
save_button = tk.Button(window, text="Save to CSV", command=save_to_csv)

start_button.pack()
stop_button.pack()
save_button.pack()

# Start the GUI
window.mainloop()
