import backtrader as bt




class StrategyDoubleSma(bt.Strategy):
    params = (
        ('fast_length',7),
        ('slow_length',25)
    )

    def __init__(self):
        self.ma_fast = bt.indicators.SMA(self.datas[1].close,period = 7)
        self.ma_slow = bt.indicators.SMA(self.datas[1].close,period = 25)
        self.buy_price = None
        self.sell_price = None
        self.bar_executed = None
        self.active = False


    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.datetime(0)
        #print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        if not self.position:
            if self.ma_fast[-1] - self.ma_slow[-1] < 0 and self.ma_fast[0] - self.ma_slow[0] > 0:
                self.buy(exectype=bt.Order.Market)
        else:
            if self.data_close[0] <= self.buy_price and len(self) >= self.bar_executed + 15:
                self.close(exectype=bt.Order.Market)
            elif self.ma_fast[-1] - self.ma_slow[-1] > 0 and self.ma_fast[0] - self.ma_slow[0] < 0:
                self.close(exectype=bt.Order.Market)

        if self.ma_fast[0] < self.ma_slow[0]:
            self.active = True



    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
                self.bar_executed = len(self)

                self.log('BUY EXECUTED, Price: {}, Cost: {}'.format(
                    order.executed.price,
                    order.executed.value
                  )
                )

            elif order.issell():
                self.log('SELL EXECUTED, Price: {}, Cost: {}'.format(
                    order.executed.price,
                    order.executed.value
                    )
                )
                self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')



    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, Gross: {}'.format(trade.pnl))



class StrategyDoubleSmaWithFilter(bt.Strategy):
    params = (
        ('fast_length',7),
        ('slow_length',25)
    )

    def __init__(self):
        self.ma_fast = bt.indicators.SMA(self.datas[0].close,period = 7)
        self.ma_slow = bt.indicators.SMA(self.datas[0].close,period = 25)
        self.buy_price = None
        self.sell_price = None
        self.bar_executed = None

        self.volume = self.datas[1].volume
        bband = bt.indicators.BollingerBands(self.volume, period=20, devfactor=0.5)
        self.top = bband.top

    def log(self, txt, dt = None):
        dt = dt or self.datas[0].datetime.datetime(0)
        #print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        if not self.position:
            if self.ma_fast[0] >= self.ma_slow[0] and self.volume[0] >= self.top[0]:
                self.buy(exectype=bt.Order.Market)
        else:
            if self.data_close[0] <= self.buy_price and len(self) >= self.bar_executed + 15:
                self.close(exectype=bt.Order.Market)
            elif self.ma_fast[0] <= self.ma_slow[0]:
                self.close(exectype=bt.Order.Market)



    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.buy_price = order.executed.price
                self.bar_executed = len(self)
                self.log('BUY EXECUTED, Price: {}, Cost: {}'.format(
                    order.executed.price,
                    order.executed.value
                  )
                )
            elif order.issell():
                self.log('SELL EXECUTED, Price: {}, Cost: {}'.format(
                    order.executed.price,
                    order.executed.value
                    )
                )
                self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')



    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, Gross: {}'.format(trade.pnl))




