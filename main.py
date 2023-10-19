import json
from requests import post, get
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from cfg import *
from bs4 import BeautifulSoup as BS
from insert_filters import *
import sqlite3
from datetime import datetime, timedelta
from fake_useragent import UserAgent
import cloudscraper

scraper = cloudscraper.create_scraper()

db = sqlite3.connect('cards.db')
cur = db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS cards(indetifier TEXT, time TEXT)")
db.commit()

date_time_str = '2023-06-29 00:20:00.000000'

useragent = UserAgent()

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomaticControlled")
options.add_argument(f"user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.888 YaBrowser/23.9.2.888 Yowser/2.5 Safari/537.36'")
options.add_argument("--headless")

browser = webdriver.Chrome(options=options)

cook_url = "https://tradeback.io/ru"

q = "https://tradeback.io/ru/comparison#"

parametrs = param.format(GAME, SECOND_SERVICE, AUTO_BUY, MIN_PRICE, MAX_PRICE, MIN_COUNT, MIN_PROSENT, MAX_PROSENT)

URL = q+"{" + parametrs + "}"


def check_card():
    while True:
        try:
            times = cur.execute("SELECT time FROM cards").fetchall()
            for bd_time in times:
                if datetime.now() - datetime.strptime(bd_time[0], '%Y-%m-%d %H:%M:%S.%f') > timedelta(minutes=1):
                    cur.execute("DELETE FROM cards WHERE time = (?)", (bd_time[0],))
                    db.commit()

            cards = browser.find_element(By.CSS_SELECTOR, 'tbody[id="table-body"]').find_elements(By.CSS_SELECTOR, "tr")

            if len(cards) != 0:
                titles = []
                prices = []
                for card in cards:
                    card_html = BS(card.get_attribute("innerHTML"), "lxml")

                    if card_html is not None:

                        title_table = card_html.find("td", class_="copy-name").text

                        price_table = card_html.find_all("td", class_="field-price")[0].find("div", class_="first-line").find("span", class_="price usd unavailable")

                        if price_table is not None:
                            price_table = price_table.text

                        elif price_table is None:
                            price_table = card_html.find_all("td", class_="field-price")[0].find("div",
                                                                                                 class_="first-line").find("span", class_="price usd").text


                        if cur.execute("SELECT indetifier FROM cards WHERE indetifier = (?)", (title_table + price_table.replace("$ ", ''),)).fetchone() is None:
                            prices.append(price_table)
                            titles.append(title_table)

                if len(titles) == 0:
                    print("Found 0 items", datetime.now())

                    browser.find_element(By.CSS_SELECTOR, 'div[class="comparison-refresh-btn"]').click()
                    sleep(5)
                    continue

                else:
                    buy_skin(titles, prices)
                    titles.clear()
                    prices.clear()
                    continue

            else:
                print("Found 0 items", datetime.now())
                browser.find_element(By.CSS_SELECTOR, 'div[class="comparison-refresh-btn"]').click()
                sleep(5)
                continue
        except AttributeError as ex:
            print(ex)
            browser.find_element(By.CSS_SELECTOR, 'div[class="comparison-refresh-btn"]').click()
            sleep(5)
            continue

try:
    browser.set_window_size(1920, 1080)

    browser.get(cook_url)

    browser.add_cookie(cookies)
    print("Cookies loaded")
    browser.get(URL)


    def break_auto_refresh():
        browser.find_elements(By.CSS_SELECTOR, "div[class='dropdown-select']")[3].click()
        sleep(0.1)
        browser.find_element(By.CSS_SELECTOR, "label[for='auto-update-live']").click()


    def sort():
        browser.find_elements(By.CSS_SELECTOR, "th[class='center']")[2].find_element(By.CSS_SELECTOR, "i[class='fa fa-sort']").click()


    def number_of_sales():
        browser.find_element(By.CSS_SELECTOR, "div[id='more-filters']").click()
        elements = browser.find_elements(By.CSS_SELECTOR, "div[class='comparison-sales-block']")


        elements[0].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").click()
        elements[0].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.CONTROL + "a")
        elements[0].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.DELETE)
        elements[0].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(STEAMCOMMUNITY_NUM_SALES)

        elements[1].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").click()
        elements[1].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.CONTROL + "a")
        elements[1].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.DELETE)
        elements[1].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(CS_DOTA_MONEY_NUM_SALES)

        elements[2].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").click()
        elements[2].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.CONTROL + "a")
        elements[2].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.DELETE)
        elements[2].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(BITSKINS_NUM_SALES)

        elements[3].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").click()
        elements[3].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.CONTROL + "a")
        elements[3].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.DELETE)
        elements[3].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(DMARKET_NUM_SALES)

        elements[4].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").click()
        elements[4].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.CONTROL + "a")
        elements[4].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(Keys.DELETE)
        elements[4].find_element(By.CSS_SELECTOR, "input[class='comparison-sales-input sales-filter']").send_keys(TM_MARKET_NUM_SALES)

        browser.find_element(By.CSS_SELECTOR, "div[class='iziModal-header-buttons']").find_elements(By.CSS_SELECTOR, "a")[0].click()

    number_of_sales()
    sleep(0.2)
    break_auto_refresh()
    sleep(0.2)
    sort()
    sleep(2)

    def buy_skin(titles, prices):
        print(f"{len(titles)} skins from table")

        url_inv = "https://cdn.cs.trade:8443/api/getInventory"
        print(datetime.now())
        response = get(url_inv)
        print(datetime.now())
        print("Inventory geted")
        response_data = response.json()
        inventory = response_data["inventory"]

        balance = []
        successful_items_name = []
        successful_items = []
        items_unavailable = []
        items_tradable = []
        items_unavailable_count = 0
        for num, item in enumerate(inventory):
            for title, price in zip(titles, prices):
                if title in item['market_hash_name'] and str(item['price']) == price.replace("$ ", ''):
                    if item["status"] == "unavailable":
                        if items_unavailable_count < 1:
                            items_unavailable_count += 1
                            items_unavailable.append(item)

                    elif item["status"] == "tradable":
                        items_tradable.append(item)


        print(f"Number of skins from cs.trade. unavailable: {len(items_unavailable)}, tradable: {len(items_tradable)} ")

        url = "https://cs.trade/trade"
        def send_req():
            response = scraper.post(
                url,
                data={"bot": "virtual", "bot_chosen_items": json.dumps(items_unavailable), "tt": "r"},
                headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                cookies=session_to_cs_trade,
            )

            resp_data = response.json()

            if resp_data['status'] == 'error':
                print(response.json()['error'])
                if 'item_status' in response.json().keys():
                    if response.json()['item_status'] == 'not_found':
                        error_items = response.json()['bot_not_found_items']
                        for item in items_unavailable:
                            if dict(item)['id'] in error_items:
                                items_unavailable.remove(item)
                        send_req()

            else:
                balance.append(resp_data['user_balance'])
                for it in items_unavailable:
                    if cur.execute("SELECT indetifier FROM cards WHERE indetifier = (?)",
                                   (it['market_hash_name'] + str(it['price']),)).fetchone() is None:

                        successful_items.append(it['market_hash_name'] + str(it['price']))
                        successful_items_name.append(it['market_hash_name'])

        if len(items_unavailable) != 0:
            send_req()

        if len(items_tradable) != 0:
            for num, item in enumerate(items_tradable):
                response = scraper.post(
                    url,
                    data={"bot": dict(item)["bot"], "bot_chosen_items": json.dumps([items_tradable[num]]), "tt": "s"},
                    headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                    cookies=session_to_cs_trade,
                )

                resp_data = response.json()

                if resp_data['status'] == 'error':
                    continue
                else:
                    balance.append(resp_data['user_balance'])
                    if cur.execute("SELECT indetifier FROM cards WHERE indetifier = (?)",
                                   (item['market_hash_name'] + str(item['price']),)).fetchone() is None:

                        successful_items.append(item['market_hash_name'] + str(item['price']))
                        successful_items_name.append(item['market_hash_name'])

        for index_item in successful_items:
            cur.execute("INSERT INTO cards VALUES (?, ?)", (index_item, datetime.now(),))
            db.commit()

        if len(successful_items_name) == 0:
            items_unavailable_len = 0
            items_tradable_len = 0
        else:
            items_unavailable_len = len(items_unavailable)
            items_tradable_len = len(items_tradable)

        print(f"{len(successful_items_name)} Successful purchases (unavailable: {items_unavailable_len}, tradable: {items_tradable_len}): {successful_items_name} ")

        if len(balance) == 0:
            bal = ''
        else:
            bal = balance[-1]

        print(f"End of purchases, balance: {bal} $")
        return


    check_card()
except AttributeError:
    print("exepition")
    browser.get(URL)
    sleep(3)
    check_card()