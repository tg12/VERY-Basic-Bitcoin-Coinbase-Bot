#/usr/bin/env python
import random, decimal, time, datetime, os, sys

pid = str(os.getpid())
pidfile = "/tmp/mydaemon.pid"

if os.path.isfile(pidfile):
    print (pidfile +  " already exists, exiting")
    sys.exit()
open(pidfile, 'w').write(pid)
try:

# Do some actual work here
#Authenticate First Step

 from coinbase.wallet.client import Client

 client = Client('<<YOUR API KEY>>','<<YOUR API KEY>>', api_version='2017-11-20')
 accounts = client.get_accounts()
 currency_code = 'GBP'  # can also use EUR, CAD, etc.

 for x in range(1):
  #Make the request
  #price = client.get_spot_price(currency=currency_code)
  #print ('Current bitcoin price in ' +  currency_code + " " +  price.amount)
  price = client.get_buy_price(currency_pair = 'BTC-GBP')
  #print ('Current BTC BUY price in ' +  currency_code + " " +  price.amount)
  price = client.get_sell_price(currency_pair = 'BTC-GBP')
  #print ('Current BTC SELL price in ' +  currency_code + " " +  price.amount)

 accounts = client.get_accounts()

 for account in accounts.data:
   balance = account.balance
   #print (account.name, balance.amount, balance.currency)
   #print (account.get_transactions())

#**********************TESTING************************
#**********************TESTING************************
#**********************TESTING************************
#**********************TESTING************************

 #for x in range(100):
  #test_amount_btc = (format(random.uniform(0.001, 0.006),'.8f'))
  #amount_in_gbp_fiat = float(test_amount_btc) * float(price.amount)
  #print (test_amount_btc + "BTC is worth " +  format(amount_in_gbp_fiat,'.2f') + " GBP")

 #for x in range(5):
  #print("DEBUG ****END OF UNIT TEST*** float.price is " + price.amount)

#**********************TESTING************************
#**********************TESTING************************
#**********************TESTING************************
#**********************TESTING************************

#Notes
#balance.amount is always the number of BTC you HODL currently, Value is 0.00000000
#price.amount is the value of 1 BTC in nominated currency, This case GBP
#Thus, The math is this Number of Bitcoin's held for now less than 1, times by the price. That is the total value to you in fiat

 with open('/root/MyPythonCode/pricehist.txt', 'r') as f:
    lines = f.read().splitlines()
    last_line = lines[-1]
    starting_price_fiat = float(last_line) * float(price.amount)

 print ("Your starting Fiat Balance is (Last time this script ran)  " +  str(starting_price_fiat) + "GBP")
 #Current price from Exchange
 amount_in_gbp_fiat = float(balance.amount) * float(price.amount)
 print ("You current balance is worth in fiat (From the Exchange)  " +  str(amount_in_gbp_fiat) + "GBP")

 for x in range(1):
  if amount_in_gbp_fiat <= starting_price_fiat:
   print ("DEBUG: NO CHANGE!!! (Or Price is lower)")
   open('/root/MyPythonCode/tradingbot.log', 'a+').write(str(datetime.datetime.now()) + " DEBUG: NO ACTION NEEDED!!!" + '\n')
  else:
    #work out price increase and it's respective percentage
    price_change = float(amount_in_gbp_fiat - starting_price_fiat)
    percentage = 100 * float(price_change)/float(starting_price_fiat)
    if percentage >= 3:
     #If it reaches here you are in profit plus a little bit for fee's and stuff
     open('/root/MyPythonCode/tradingbot.log', 'a+').write("DEBUG CONSIDER SELLING!!! " + str(datetime.datetime.now()) + " " + str(price_change) + " Percentage Increase is " + (percentage) + '\n')
     #Write a little market to the file to signify this fact
     open('/root/MyPythonCode/pricehist.txt', 'a+').write("***PROFIT MARKER*** " + str(datetime.datetime.now()) + '\n')
     #Then make sure we never read the Profit market into the variable, Write it to the file.
     open('/root/MyPythonCode/pricehist.txt', 'a+').write(str(starting_price_fiat) + '\n')
     #FOR NOW, We just need something here to compare it too. So just write the starting price again back to the file, So we can then compare it against our balance.
     #This is just TEMP

     #Sell, Sell amount over 10 quid (price_change)
     #Example - DO NOT USE
     #sell = client.sell('2bbf394c-193b-5b2a-9155-3b4732659ede',amount="10",currency="BTC", payment_method="83562370-3e5c-51db-87da-752af5ab9559")

     #*****IMPLEMENT LATER****
     #sell = client.sell(total=float(price_change),currency="GBP") #Is this a float or a string??? Not sure check this out later

     #while sell.status != 'completed' or 'canceled':
      #time.sleep(5)
      #print ("DEBUG: Waiting for 5 seconds and check again")
      #print (sell.status)
      #NOTE: Status is either created, completed, canceled. loop whilst not completed!!!! We need to wait to the transaction is either cancelled or even better completed

     #RANDOM THOUGHT: Buy another 10 quids worth, Why do I need to do this when i can skim off the top keeping my initial 10 quids worth

     #new_start price = float(balance.amount) * float(price.amount)
     #print ("DEBUG: What is my new start price??? " + new_start_price)
     #This should be close to my initial tenner as possible
     #open('/root/MyPythonCode/pricehist.txt', 'a+').write(str(new_start_price) + '\n')
     #There you have it, Start again. Done everything we need to at this point, Sold the price difference with Fee's back to start again at this point.
     print ("DEBUG: YAY SUCCESS!!!")

finally:
    os.unlink(pidfile)
