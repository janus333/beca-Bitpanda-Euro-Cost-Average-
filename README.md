# beca-Bitpanda-Euro-Cost-Average-
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
