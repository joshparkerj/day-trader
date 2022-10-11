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

simulation_size = 500000

# targets = [{ 'target': 1.005 + 0.0000005 * i, 'running total': [1000.0 for _ in range(simulation_size)] } for i in range(10000)]

# print(len([quotes[equity] for equity in quotes.keys()]))

running_totals = [1000.0 for _ in range(simulation_size)]

target = 1.008778

print(len(quotes.keys()))

for i in range(trading_days):
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
    if position_exit > 500:
      # regulatory transaction fee
      position_exit -= position_exit * 22.9 / 1000000.0
    if position_entry_shares > 50:
      # trading activity fee
      position_exit -= 0.00013 * position_entry_shares      
    running_totals[j] = position_exit

# print(sorted(running_totals))

print(f'less than 700: {len([x for x in running_totals if x < 700])}')
print(f'at least 700 and less than 800: {len([x for x in running_totals if x >= 700 and x < 800])}')
print(f'at least 800 and less than 900: {len([x for x in running_totals if x >= 800 and x < 900])}')
print(f'at least 900 and less than 1000: {len([x for x in running_totals if x >= 900 and x < 1000])}')
print(f'at least 1000 and less than 1100: {len([x for x in running_totals if x >= 1000 and x < 1100])}')
print(f'at least 1100 and less than 1200: {len([x for x in running_totals if x >= 1100 and x < 1200])}')
print(f'at least 1200 and less than 1300: {len([x for x in running_totals if x >= 1200 and x < 1300])}')
print(f'at least 1300 and less than 1400: {len([x for x in running_totals if x >= 1300 and x < 1400])}')
print(f'at least 1400: {len([x for x in running_totals if x >= 1400])}')

'''
x = [st['target'] for st in targets]
y = [mean(st['running total']) for st in targets]
plt.scatter(x, y)
plt.show()
'''
