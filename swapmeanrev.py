from numpy import linalg as LA
import numpy as np


def initialize(context):

    #context will be the nasdaq 100 stocks
    context.nasdaq_100 = [sid(24),    sid(114),   sid(122),   sid(630)  , sid(67),
      sid(20680), sid(328),   sid(14328), sid(368),   sid(16841),
      sid(9883),  sid(337),   sid(38650), sid(739),   sid(27533),
      sid(3806),  sid(18529), sid(1209),  sid(40207), sid(1419),
      sid(15101), sid(17632), sid(39095), sid(1637),  sid(1900),
      sid(32301), sid(18870), sid(14014), sid(25317), sid(36930),
      sid(12652), sid(26111), sid(24819), sid(24482), sid(2618),
      sid(2663),  sid(27543), sid(27543), sid(2696),  sid(42950),
      sid(20208), sid(2853),  sid(8816),  sid(5530),  sid(3212),
      sid(9736),  sid(23906), sid(26578), sid(22316), sid(13862),
      sid(3951),  sid(8655),  sid(25339), sid(4246),  sid(43405),
      sid(27357), sid(32046), sid(4485),  sid(43919), sid(4668),
      sid(8677),  sid(22802), sid(3450),  sid(5061),  sid(5121),
      sid(5149),  sid(5166),  sid(23709), sid(13905), sid(19926),
      sid(19725), sid(8857),  sid(5767),  sid(5787),  sid(19917),
      sid(6295),  sid(6413),  sid(6546),  sid(20281), sid(6683),
      sid(26169), sid(6872),  sid(11901), sid(13940), sid(7061),
      sid(15581), sid(24518), sid(7272),  sid(39840), sid(7671),
      sid(27872), sid(8017),  sid(38817), sid(8045),  sid(8132),
      sid(8158),  sid(24124), sid(8344),  sid(8352),  sid(14848)]


    #context.stocks = []
    context.max_notional =  1000000
    context.previous_prices = None
    context.day = None

    schedule_function(handler, date_rules.every_day())

# Will be called on every trade event for the securities
def handler(context, data):
  if context.previous_prices == None:
      context.previous_prices = np.array([data[stock].price for stock in context.stocks])
      return

  if context.day == None:
      context.day = data[context.stocks[0]].datetime
      return

  if data[context.stocks[0]].datetime.day == context.day.day:
      return

  # calculate and shift change from previous days price
  current_prices = np.array([data[stock].price for stock in context.stocks])

  pct_change = current_prices / context.previous_prices - 1

  # normalize

  norm_pct = pct_change / LA.norm(pct_change)

  buy_multiplier = 1

  #iterate through the stocks which we are looking at
    for i in range(len(norm_pct)):
        stock = context.stocks[i]
        #calculating how much to buy/sell;

        #selling = rounded value weighted by performance
        sell_amount = round(-1 * context.portfolio.positions[stock].amount * norm_pct[i] * norm_pct[i])
        #Buying = max buying ability (based on available funds) weighted
        buy_amount = buy_multiplier * round((context.portfolio.cash / data[stock].price) * norm_pct[i] * norm_pct[i])

        notional = context.portfolio.positions[stock].amount * data[stock].price
        #executes the buying and selling only if change is favored in positive or negative
        if norm_pct[i] > 0 and abs(sell_amount) > 0 and notional > -context.max_notional:
            if abs(norm_pct[i]**2 > 0.05):
                order(stock, sell_amount)

        if norm_pct[i] < 0 and buy_amount > 0 and notional < context.max_notional:
            if abs(norm_pct[i]) > 0.05:
                order(stock, buy_amount)



  context.previous_prices = current_prices
  context.day = data[context.stocks[0]].datetime
