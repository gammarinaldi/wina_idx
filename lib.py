import concurrent.futures
import login
import logout
import order
import portfolio
import csv
import telegram
import logging
import traceback
import os
import time
import users
import auto_trading_list
import delete_auto_trade
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

LOG = []

class data_order():
    def __init__(self, emiten, buy_price, take_profit, cut_loss):
        self.emiten = emiten
        self.buy_price = buy_price
        self.take_profit = take_profit
        self.cut_loss = cut_loss

def get_env():
    load_dotenv()
    return os.getenv('ENABLE_SIGNAL'), os.getenv('ENABLE_BUY'), os.getenv('ENABLE_SELL'), os.getenv('SELL_DELAY'), os.getenv('DIR_PATH') 

def get_dir_path():
    load_dotenv()
    return os.getenv('DIR_PATH')

def get_tele_data():
    load_dotenv()
    tele_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    tele_chat_ids = [os.getenv('TELEGRAM_CHAT_ID_WINA'), os.getenv('TELEGRAM_CHAT_ID_SINYALA')]
    tele_log_id = os.getenv('TELEGRAM_LOGGER_ID')

    return tele_bot_token, tele_chat_ids, tele_log_id

def get_tele_bot():
    tele_bot_token, tele_chat_ids, tele_log_id = get_tele_data()
    bot = telegram.Bot(token=tele_bot_token)
    return bot, tele_chat_ids, tele_log_id

def is_empty_csv(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        for i, _ in enumerate(reader):
            if i:  # Found the second row
                return False
    return True

def get_result():
    dir_path = get_dir_path()
    with open(f"{dir_path}\\result.csv", "r") as file:
        csvreader = csv.reader(file)
        if is_empty_csv(f"{dir_path}\\result.csv") == False:
            next(csvreader, None)

            list = []
            for row in csvreader:
                emiten = row[0]
                if row[0].find(".JK") != -1:
                    emiten = emiten.replace(".JK", "")

                signal_date = row[1].split(" ")[0]
                # close = row[2]
                # change = row[3]
                # trx = row[4]
                buy_price = row[5]
                take_profit = row[6]
                cut_loss = row[7]
                list.append([emiten, signal_date, buy_price, take_profit, cut_loss])
            return list
        else:
            msg = "No signal for today"
            bot, tele_chat_ids, _ = get_tele_bot()
            load_dotenv()
            if os.getenv('ENABLE_SIGNAL') == "1":
                send_msg_v2(bot, tele_chat_ids, msg)
            return msg

def do_login(user):
    res = login.call(user)
    if res.status_code == 200:
        data = res.json()
        access_token = "jwt " + data["access_token"]
        msg = user["email"] + ": login OK"
        print(msg)
        LOG.append(msg)
        return res.status_code, data, access_token
    else:
        msg = user["email"] + ": login error: " + res.text
        LOG.append(msg)
        return res.status_code, data, ""

def do_logout(access_token, user):
    res = logout.call(access_token)
    if res.status_code == 200:
        msg = user["email"] + ": logout OK"
        LOG.append(msg)
    else:
        msg = user["email"] + ": logout error: " + res.text
        LOG.append(msg)

def get_signal_history():
    dir_path = get_dir_path()
    with open(f"{dir_path}\\signal_history.csv", "r") as file:
        csvreader = csv.reader(file)
        if is_empty_csv(f"{dir_path}\\signal_history.csv") == False:
            next(csvreader, None)
            list = []
            for row in csvreader:
                list.append([row['emiten'], row['signal_date'], row['buy_price'], row['take_profit'], row['cut_loss']])
        file.close()
    return list

def check_position(access_token, porto_dicts, user):
    print('Check position...')
    res = auto_trading_list.call(access_token)
    if res.status_code == 200:
        data = res.json()
        at_list_dicts = data["results"]

        for item in porto_dicts:
            emiten = item['stock']
            lot = int(item['lot'])
            dicts = [i for i in at_list_dicts if i['code'] == emiten]
            if len(dicts) == 2:
                print(emiten + ': Position ok')
            elif len(dicts) == 1:
                signal_history_dicts = [i for i in get_signal_history() if i[0] == emiten]
                for item in signal_history_dicts[-1]:
                    h_emiten = item[0]
                    h_tp = item[3]
                    h_cl = item[4]
                    if h_emiten == emiten:
                        comparator = dicts[0]['comparator']
                        if comparator == 'LTE':
                            print('Re-create auto sell for take profit')
                            order.create_sell(access_token, emiten, h_tp, lot, "GTE")
                        else:
                            print('Re-create auto sell for cut loss')
                            order.create_sell(access_token, emiten, h_cl, lot, "LTE")
            else:
                print('Remove unused auto trade setup')
                for trade in at_list_dicts:
                    delete_auto_trade.call(access_token, trade['id'])
    else:
        msg = user["email"] + ": check position error: " + res.text
        LOG.append(msg)

def get_portfolio(access_token, user):
    porto_res = portfolio.call(access_token)
    if porto_res.status_code == 200:
        porto_data = porto_res.json()
        return porto_data["result"]["portfolio"]
    else:
        msg = user["email"] + ": get portfolio error: " + porto_res.text
        LOG.append(msg)

def buy(user, list_order):
    LOG.append("Order Buy Report:")
    login_status, data, access_token = do_login(user)
    if login_status == 200:
        access_token = "jwt " + data["access_token"]
        # porto = portfolio.call(access_token)
        # data_porto = porto.json()
        # trading_limit = data_porto["result"]["trading_limit"]
        trading_limit = 4_000_000
        amount = trading_limit / 4

        for obj in list_order:
            res = order.create_buy(access_token, obj.emiten, amount)
            if res.status_code == 200:
                msg = user["email"] + ": order buy " + obj.emiten + " sent"
                print(msg)
                LOG.append(msg)
                print(res.json())
            else:
                msg = user["email"] + ": order buy " + obj.emiten + " error: " + res.text
                LOG.append(msg)
        
        do_logout(access_token, user)
    else:
        msg = user["email"] + ": login error: " + res.text
        LOG.append(msg)

def sell(user, list_order):
    LOG.append("Order Sell Report:")
    login_status, _, access_token = do_login(user)
    if login_status == 200:
        portfolio = get_portfolio(access_token, user)
        if isinstance(portfolio, list) and portfolio != []:
            check_position(access_token, portfolio, user)

            for obj in list_order:
                emiten = obj.emiten
                tp = obj.take_profit
                cl = obj.cut_loss
                dicts = [i for i in portfolio if i['stock'] == emiten]
                
                if dicts != []:
                    lot = dicts[0]["lot"]
                    res = order.create_sell(access_token, emiten, tp, lot, "GTE")
                    if res.status_code == 200:
                        msg = user["email"] + ": set TP " + emiten + " sent"
                        LOG.append(msg)
                        print(msg)
                        print(res.json())

                        time.sleep(3)

                        res = order.create_sell(access_token, emiten, cl, lot, "LTE")
                        if res.status_code == 200:
                            msg = user["email"] + ": set CL " + emiten + " sent"
                            LOG.append(msg)
                            print(msg)
                            print(res.json())
                        else:
                            msg = user["email"] + ": set CL error: " + res.text
                            LOG.append(msg)
                    else:
                        msg = user["email"] + ": set TP error: " + res.text
                        LOG.append(msg)
                else:
                    LOG.append(user["email"] + ": setup sell " + emiten + " failed, not exists in portolio")
        do_logout(access_token, user)
    
def async_order(side, list_order, bot):
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_user = executor_submit(side, executor, list_order)
        for future in concurrent.futures.as_completed(future_to_user):
            user = future_to_user[future]
            try:
                if future.result() == None:
                    print(user["email"] + ": RESULT OK")
                else:
                    print(user["email"] + ": RESULT ERROR")
                    print(future.result())
            except Exception:
                _, _, tele_log_id = get_tele_data()
                error_log(bot, tele_log_id)

def executor_submit(side, executor, list_order):
    if side == "buy":
        return {executor.submit(buy, user, list_order): user for user in users.list}
    else:
        return {executor.submit(sell, user, list_order): user for user in users.list}

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

def send_log(bot, chat_id, log):
    bot.send_message(chat_id=chat_id, text=join_msg(log))

def join_msg(list):
    if list:
        return '\n'.join(list)
    else:
        return "Message is empty"

def send_msg_v2(bot, chat_ids, msg):
    for chat_id in chat_ids:
        bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN_V2)

def error_log(bot, chat_id):
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    error_msg = traceback.format_exc()
    logger.debug(error_msg)
    bot.send_message(chat_id=chat_id, text=error_msg)
