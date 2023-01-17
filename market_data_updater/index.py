import users
import api.login
import api.stock_info
import api.stock_all
import concurrent.futures
import traceback
import time
import api.get_security_token
import api.login_security
import api.buy
import api.sell
import api.portfolio
import csv
import os
import requests
import json
import telegram
import watchlist

from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from math import floor
from dotenv import load_dotenv

load_dotenv()

dir_path = os.getenv('DIR_PATH')
params = dict(apiKey=os.getenv('PROXY_ROTATOR_KEY'))
resp = requests.get(url=os.getenv('PROXY_ROTATOR_URL'), params=params)
resp_text = json.loads(resp.text)
proxies = {
   "http": f"http://{resp_text['proxy']}"
}

today = date.today()
quote_date = today.strftime('%Y-%m-%d')

log_list = []

def get_tele_data():
    load_dotenv()
    tele_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    tele_log_id = os.getenv('TELEGRAM_LOGGER_ID')

    return tele_bot_token, tele_log_id

def get_tele_bot():
    tele_bot_token, tele_log_id = get_tele_data()
    bot = telegram.Bot(token=tele_bot_token)
    return bot, tele_log_id

def send_log():
    bot, tele_log_id = get_tele_bot()
    bot.send_message(chat_id=tele_log_id, text=join_msg(log_list))

def join_msg(list):
    if list:
        return '\n'.join(list)
    else:
        return "Message is empty"

def tick(price):
    if price <= 200: 
        return 1
    elif price > 200 and price <= 500: 
        return 2
    elif price > 500 and price <= 2000: 
        return 5
    elif price > 2000 and price <= 5000: 
        return 10
    else: 
        return 25
        
def do_update(access_token, symbol):
    res = api.stock_info.call(access_token, symbol, proxies)
    try:
        if res.status_code == 200:
            data = res.json()
            if data["data"] == None:
                print(symbol + ": No data")
            else:
                symbol = data["data"]["symbol"]
                open = data["data"]["open"]
                high = data["data"]["high"]
                low = data["data"]["low"]
                close = data["data"]["close"]
                volume = data["data"]["volume"]

                save_result(symbol, quote_date, open, high, low, close, volume)
        else:
            event = symbol + ": HTTP error"
            log_list.append(event)
            print(event)
            print(res.text)
    except:
            save_failed(symbol)
            # print(symbol + ": Exception error")
            # print("Error traceback:")
            # print(traceback.format_exc())
            print("Response:")
            print(res)

def save_result(symbol, date, o, h, l, c, v):
    with open(f'{dir_path}\\result.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f) #this is the writer object
        writer.writerow([symbol, date, o, h, l, c, v]) #this is the data
        f.close()

def save_failed(symbol):
    with open(f'{dir_path}\\failed.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f) #this is the writer object
        writer.writerow([symbol]) #this is the data
        f.close()

def executor_submit(executor, access_token):
    return {executor.submit(do_update, access_token, symbol): symbol for symbol in watchlist.list}

def async_screening(access_token):
    event = "Start async screening..."
    log_list.append(event)
    print(event)

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_user = executor_submit(executor, access_token)
        for future in concurrent.futures.as_completed(future_to_user):
            try:
                if future.result() != None:
                    print("Async result error")
                    print(future.result())
            except Exception as error:
                print("Exeption error occured:")
                print(error)
                print(traceback.format_exc())

if __name__ == '__main__':
    event = "WINA Market Data Updater"
    log_list.append(event)
    print(event)

    t1 = time.time()
    event = "Using proxies: " + proxies["http"]
    log_list.append(event)
    print(event)

    # Clear result.csv
    open(f'{dir_path}\\result.csv', "w+").close()

    email = users.list[0]
    password = users.list[1]
    pin = users.list[2]
    res = api.login.call(email, password, proxies)
    
    if res.status_code == 200:
        data = res.json()
        print(data)
        access_token = "Bearer " + data["data"]["access_token"]

        async_screening(access_token)
        # do_update(access_token, "ADMR")

        event = "Async screening finish."
        log_list.append(event)
        print(event)
    else:
        event = "HTTP error"
        log_list.append(event)
        print("HTTP error")
        print(res.text)

    t2 = time.time()
    diff = t2 -t1
    event = f"Elapsed times: {str(round(diff, 2))} seconds."
    log_list.append(event)
    print(f"Elapsed times: {str(round(diff, 2))} seconds.")

    send_log()
    