import pandas as pd
from binance import Client
import time
from datetime import datetime

class PyDao:
    def __init__(self):
        api_key = "lbrZYZAI3B1taETwcA1DZZwFHaE24qt0cjQt5ffAN0Tl4gyvqLMju4M1Qn5hJ8pN"
        api_secret = "ON4FuMNqjxVo8CcKCGnCUfXjfM70ts3cChMui8JHlXlVMswZOMJIKctVnA1FIS6Y"
        self.client = Client(api_key, api_secret)

    @staticmethod
    def get_time_interval(time_interval):
        if time_interval == '1min':
            return Client.KLINE_INTERVAL_1MINUTE
        if time_interval == '15min':
            return Client.KLINE_INTERVAL_15MINUTE
        if time_interval == '1hour':
            return Client.KLINE_INTERVAL_1HOUR

    def get_timestamp(self, datetime_obj):
        return int(datetime_obj.timestamp()*1000)

    def get_klines(self, symbol, start_time, end_time, time_interval):
        start_time = self.get_timestamp(start_time)
        end_time = self.get_timestamp(end_time)

        kline = self.client.get_historical_klines(symbol=symbol, interval=self.get_time_interval(time_interval), start_str=start_time,end_str= end_time)

        data = pd.DataFrame(kline).iloc[:,:6]
        data.columns =['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']

        def todatetime(timestamp):
            return datetime.fromtimestamp(timestamp/1000)

        data['Datetime'] = data['Datetime'].apply(todatetime)
        data.set_index('Datetime', inplace=True)
        data.Open = data.Open.astype('float')
        data.Close = data.Close.astype('float')
        data.High = data.High.astype('float')
        data.Low = data.Low.astype('float')
        data.Volume = data.Volume.astype('float')
        self.finish()
        return data

    def finish(self):
        self.client.close_connection()

'''
def test():
    py = PyDao()
    df_1min = py.get_klines('NBSUSDT', start_time=datetime(2021,12,20), end_time=datetime(2021,12,21), time_interval='15min')
    df_1min.to_csv('15min_kline_data.csv')
test()
'''



