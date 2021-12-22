import backtrader as bt
import pandas as pd
from pydao import PyDao
from strategy_double_sma import StrategyDoubleSma, StrategyDoubleSmaWithFilter
from datetime import datetime


def load_data(symbol,start_time,end_time):
    py = PyDao()
    df_1min = py.get_klines(symbol, start_time=start_time, end_time=end_time, time_interval='1min')
    df_15min = py.get_klines(symbol, start_time=start_time, end_time=end_time, time_interval='15min')
    df_15min.to_csv('15min_kline_data.csv')

    data_1min = bt.feeds.PandasData(dataname=df_1min)
    data_15min = bt.feeds.PandasData(dataname=df_15min)
    return (data_1min, data_15min)


def init_cerebro(data,strategy):
    cerebro = bt.Cerebro()

    cerebro.adddata(data[0])
    cerebro.adddata(data[1])
    cerebro.addsizer(bt.sizers.PercentSizer, percents=100)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
    cerebro.broker.setcash(500)
    cerebro.addstrategy(strategy)

    return cerebro


def get_result(cerebro):
    result = cerebro.run()
    res_list = [[
        round(cerebro.broker.getvalue(),2),
        result[0].analyzers.returns.get_analysis()['rtot'],
        result[0].analyzers.returns.get_analysis()['rnorm100'],
        result[0].analyzers.drawdown.get_analysis()['max']['drawdown'],
        result[0].analyzers.sharpe.get_analysis()['sharperatio']
    ]]
    return res_list


if __name__ == '__main__':
    symbol_list = ['NBSUSDT','COCOSUSDT','DOGEUSDT']
    res_dict = {}
    for symbol in symbol_list:
        data = load_data(symbol,start_time=datetime(2021,12,1),end_time=datetime(2021,12,15))
        cerebro = init_cerebro(data,StrategyDoubleSma)
        res_dict[symbol] = get_result(cerebro)
    print(res_dict)



    #res_df = pd.DataFrame(res_list, columns=['Total_return', 'APR', 'DrawDown', 'SharpeRatio'])





