from csv import DictReader
from glob import glob
from random import choices
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
from dataclasses import dataclass

'''

for traders with less than 25k in their brokerage accounts, three day trades are allowed per five day rolling period

this means, in effect, that three day trades are allowed per week as long as they are performed on the same days each week

Which days?

I will rule out Mondays since many market holidays fall on Mondays

The number of market holidays falling on each day are:
Monday: 19
Tuesday: 1
Wednesday: 2
Thursday: 3
Friday: 3

So, Tuesdays and Wednesdays are in.

Fridays have shortened days each November on black friday.

So, if day trading on exactly the same three weekdays each week, it seems that Tuesday, Wednesday, and Thursday are optimal.

For traders with 25k or more in their brokerage accounts, it would seem that there is no limitation on number of day trades. 

'''

csv_files = glob('./data-files/**/*.csv')

quotes = {}

@dataclass
class Quote:
  open_price: float
  high_price: float
  close_price: float
  trade_date: date

for csv_file in csv_files:
  with open(csv_file, newline='') as f:
    quote_reader = DictReader(f)
    quote = []
    for row in quote_reader:
      trade_date = date.fromisoformat(row['Date'])
      if trade_date.weekday() in (1, 2, 3):
        try:
          quote.append(Quote(float(row['Open']), float(row['High']), float(row['Close']), trade_date))
        except:
          print(csv_file)
          print(row)
    if (len(quote) != 155):
      print(csv_file)
      print(len(quote))
    else:
      quotes[csv_file.split('.')[1].split('\\')[2]] = quote

# sample_symbol = 'INDB'

trading_days = 155

simulation_size = 500

# targets = [{ 'target': 1.005 + 0.0000005 * i, 'running total': [1000.0 for _ in range(simulation_size)] } for i in range(10000)]

# print(len([quotes[equity] for equity in quotes.keys()]))

running_totals = [1000.0 for _ in range(simulation_size)]

target = 1.008778

for i in range(trading_days):
  print(i)
  equities = choices([key for key in quotes.keys()], k=simulation_size)
  for (j, equity) in enumerate(equities):
    quote = quotes[equity][i]
    entry_price = quote.open_price
    position_entry_shares = running_totals[j] / entry_price
    target_price = entry_price * target
    if target_price <= quote.high_price:
      position_exit = position_entry_shares * target_price
    else:
      position_exit = position_entry_shares * quote.close_price
    running_totals[j] = position_exit

print(sorted(running_totals))

'''
x = [st['target'] for st in targets]
y = [mean(st['running total']) for st in targets]
plt.scatter(x, y)
plt.show()
'''
