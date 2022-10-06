# beca v. 1.0
#
# This script is a first prototype of a euro cost averaging script for the bitpanda pro exchange
# variables "insert_APIKEY_here" and "insert_private_APIKEY_here" needs to be replaced with your api keys throughout the script. only create API key for buying and selling, no withdrawal rights are recommended!! (in case your keys get compromised in some way)
# variable dayOfRefill ist the day of the month when new money arrives in the bitpanda pro EUR account
# the script checks the balance at startup, then checks the btc price, calculates how often the minimal amount of btc can be bought until dayOfRefill and goes to sleep for the corresponding amount of time until the calculated next buy.
# so whenever money is sent to the EUR account on the exchange, it will try to use that money in full until the next dayOfRefill!
# variable buyAmountInEUR is what it says it is
#
# if you wanna tip me, here is my btc coffee address: bc1qu70pg9uzjwj8pcjd4cpvuttsveghtdh9e5qlj4
#
import calendar
import datetime
import http.client
import logging
import time

import ccxt

logging.basicConfig(filename='ecapy.log',
                    format='%(levelname)s %(asctime)s :: %(message)s',
                    level=logging.DEBUG)


def sweet_dreams(secs: float):
    debug = True
    max_sleep_secs = 1000000
    secs_extra_ms = 0

    if secs > max_sleep_secs:
        if type(secs) is float:
            secs_extra_ms = str(secs).split('.')[-1]
            if secs_extra_ms:
                secs_extra_ms = secs_extra_ms.lstrip('0')

            secs_extra_ms = float(f"0.{secs_extra_ms}")

        secs = int(secs)
        secs_divide = float(secs) / max_sleep_secs  # e.g: 2.4123
        secs_int = int(secs_divide)  # e.g: 2
        secs_decimal_remainder = int(str(secs_divide).split(".")[-1])  # e.g 4123
        chunks = [max_sleep_secs for _ in range(secs_int)]
        if secs_decimal_remainder:
            chunks.append(int(str(secs_decimal_remainder).lstrip('0')))

        if secs_extra_ms:
            chunks.append(secs_extra_ms)

        if debug:
            print(f"Debug [sweet_dreams]: -> Total: {secs} | Max: {max_sleep_secs} | Chunks: {chunks}")
            logging.debug(f"Debug [sweet_dreams]: -> Total: {secs} | Max: {max_sleep_secs} | Chunks: {chunks}")
            # quit()

        for seconds in chunks:
            time.sleep(seconds)
    else:
        if debug:
            print(f"Debug [sweet_dreams]: -> Total: {secs} | Max: {max_sleep_secs} | Chunks: None")
            logging.debug(f"Debug [sweet_dreams]: -> Total: {secs} | Max: {max_sleep_secs} | Chunks: None")
            # quit()

        time.sleep(secs)

exchange_id = 'bitpanda'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': 'insert_APIKEY_here',
    'secret': 'insert_private_APIKEY_here',
})
dayOfRefill = 21
buyAmountInEUR = 11

# start loop
while 1:
    now = datetime.datetime.now()
    print("new Loop: " + str(now))
    logging.debug("new Loop: " + str(now))
    # print(exchange.fetch_balance()['EUR']['free'])
    availableEUR = float(exchange.fetch_balance()['EUR']['free'])
    print("availableEUR: " + str(availableEUR))
    logging.debug("availableEUR: " + str(availableEUR))

    daysInCurrentMonth = calendar.monthrange(now.year, now.month)[1]
    print("daysInCurrentMonth: " + str(daysInCurrentMonth))
    logging.debug("daysInCurrentMonth: " + str(daysInCurrentMonth))
    currentDay = now.day
    print("currentDay: " + str(currentDay))
    logging.debug("currentDay: " + str(currentDay))

    ticker1 = 'BTC'  # first ticker of the crypto pair
    ticker2 = 'EUR'  # second ticker of the crypto pair
    pair_price_data = exchange.fetch_ticker(ticker1 + '/' + ticker2)
    pair_price_dataValue = pair_price_data['close']

    # print("fetched dict: " + exchange.fetch_ticker(ticker1 + '/' + ticker2))
    print("pair_price_dataValue: " + str(pair_price_dataValue))
    logging.debug("pair_price_dataValue: " + str(pair_price_dataValue))

    daysTillRefill = dayOfRefill - currentDay
    if daysTillRefill < 0:
        daysTillRefill = daysInCurrentMonth - currentDay + dayOfRefill
    print("daysTillRefill: " + str(daysTillRefill))
    logging.debug("daysTillRefill: " + str(daysTillRefill))
    print("now.hour: " + str(now.hour))
    logging.debug("now.hour: " + str(now.hour))

    buyIntervalMins = (daysTillRefill * 24 * 60) / (availableEUR / buyAmountInEUR)
    print("buyIntervalMins: " + str(buyIntervalMins))
    logging.debug("buyIntervalMins: " + str(buyIntervalMins))

    buyAmountInBTC = float(buyAmountInEUR) / float(pair_price_dataValue)
    print("buyAmountInBTC: " + str(buyAmountInBTC))
    logging.debug("buyAmountInBTC: " + str(buyAmountInBTC))

    # Create BuyOrder
    if availableEUR > buyAmountInEUR:
        conn = http.client.HTTPSConnection("api.exchange.bitpanda.com")
        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer insert_private_APIKEY_here"
        }
        payload = "{\"instrument_code\":\"BTC_EUR\",\"side\":\"BUY\",\"type\":\"MARKET\",\"amount\":\"" + str(
            round(buyAmountInBTC, 5)) + "\"}"
        headers = {
            'Content-Type': "application/json",
            'Accept': "application/json",
            'Authorization': "Bearer insert_private_APIKEY_here"
        }
        conn.request("POST", "/public/v1/account/orders", payload, headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        logging.debug(data.decode("utf-8"))
    # # END Create BuyOrder
    print("buyIntervalMins*60: " + str(buyIntervalMins * 60))
    logging.debug("buyIntervalMins*60: " + str(buyIntervalMins * 60))
    sweet_dreams(buyIntervalMins * 60)
