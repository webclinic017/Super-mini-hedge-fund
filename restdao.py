
from datetime import timedelta,datetime
import pandas as pd
import  requests
from typing import List


class RestDao:
    def __init__(self, address=None):
        self.address = address

    def get_trades(self, symbol, from_id):
        r = requests.get('https://api.binance.com/api/v3/aggTrades',
            params = {
                "symbol": symbol,
                "limit": 100,
                "fromId": from_id
        })
        return r.json()

    def get_first_trade_id_from_start_time(self, symbol, start_time):
        end_time = start_time + timedelta(seconds = 60)
        r = requests.get('https://api.binance.com/api/v3/aggTrades',
            params={
                'symbol' : symbol,
                "startTime" : self.get_unix_ms(start_time),
                "endTime" : self.get_unix_ms(end_time)
            })
        response = r.json()
        if len(response) > 0:
            return response[0]['a']
        else:
            raise Exception('No trades found')

    @staticmethod
    def get_unix_ms(time):
        return int(time.timestamp()*1000)

    def process_data(self, column_name: List[str], data)-> pd.DataFrame :
        df = pd.DataFrame(data)
        df = df[['a','p','q']]
        df.a = df.a.astype(float)
        df.p = df.p.astype(float)
        df.q = df.q.astype(float)
        df.columns = column_name
        return df




























