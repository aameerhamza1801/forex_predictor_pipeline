import pandas as pd
import requests
import os

class DataIngestion():
    def __init__(self, currency, updated_data = pd.DataFrame({}), data = pd.DataFrame({})):
        self.currency = currency
        self.data = data
        self.updated_data = updated_data
        self.url = 'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol='+currency.split('-')[0]+'&to_symbol='+currency.split('-')[1]+'&outputsize=full&apikey=QYKHMCQRBZE4SXC5'

    def get_data(self, save_file):
        
        if not os.path.exists(save_file):
            response = requests.get(self.url)
            data = response.json()
            time_series_data = data.get('Time Series FX (Daily)', {})
            self.data = pd.DataFrame.from_dict(time_series_data, orient = 'index').reset_index()
            self.data.columns = ['Date','Open','High','Low','Close']
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            self.data = self.data.sort_values('Date')
            # self.data = self.data.reset_index(drop=True)
            self.data = self.data.astype({'Open': 'float64', 'High': 'float64', 'Low': 'float64','Close':'float64'})
            self.data.to_csv(save_file)
        else:
            self.data = pd.read_csv(save_file, index_col = 0)
            self.data['Date'] = pd.to_datetime(self.data['Date'])
        return self.data
    
    def update_data(self, save_file, inplace = True):
        already_data = self.get_data(save_file)
        last_date = already_data.Date.iloc[-1]
        response = requests.get(self.url)
        data = response.json()
        time_series_data = data.get('Time Series FX (Daily)', {})
        new_data = pd.DataFrame.from_dict(time_series_data, orient = 'index').reset_index()
        new_data.columns = ['Date','Open','High','Low','Close']
        new_data['Date'] = pd.to_datetime(new_data['Date'])
        new_data = new_data.sort_values('Date').reset_index(drop=True)
        latest_date = new_data.Date.iloc[-1]
        if latest_date > last_date:
            if inplace == True:
                new_data.to_csv(save_file)
            return new_data
        return pd.DataFrame({}, columns = ['Date','Open','High','Low','Close'])


