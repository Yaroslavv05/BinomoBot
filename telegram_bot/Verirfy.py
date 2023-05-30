import sqlite3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, NoSuchElementException


def get_exit_time():
    conn = sqlite3.connect('InfoToSignal.db')
    cursor = conn.cursor()
    info = []
    cursor.execute('SELECT * FROM DataSignal')
    rows = cursor.fetchall()
    for row in rows:
        info.append(row)
    exit_time = info[len(info) - 1][3]
    cursor.close()
    conn.close()
    return exit_time


# def get_now_price2():


def get_now_price():
    conn = sqlite3.connect('InfoToSignal.db')
    cursor = conn.cursor()
    info = []
    cursor.execute('SELECT * FROM DataSignal')
    rows = cursor.fetchall()
    for row in rows:
        info.append(row)

    symbol = info[len(info) - 1][0]
    while True:
        try:
            option = webdriver.ChromeOptions()
            option.add_argument('--headless')
            # option.add_argument('--no-sandbox')
            driver = webdriver.Chrome(options=option)

            url = f'https://ru.tradingview.com/chart/?symbol=OANDA%3A{symbol}'

            driver.get(url)

            time.sleep(5)
            return driver.find_element(By.XPATH, '/html/body/div[2]/div[6]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/span[1]/span[1]').text
        except (WebDriverException, NoSuchElementException):
            return False
