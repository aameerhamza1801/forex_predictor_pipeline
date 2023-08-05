import numpy as np


class FeatureEngineering():
    def __init__(self, data, train_x = None, train_y = None):
        self.data = data
        self.train_x = train_x
        self.train_y = train_y

    def create_features(self, n_features):
        self.data['return'] = self.data['Close'] - self.data['Close'].shift(1)
        return_range = self.data['return'].max() - self.data['return'].min()
        self.data['return'] = self.data['return'] / return_range
        self.data['label'] = self.data['return'].shift(-1)
        self.data['label'] = self.data['label'].apply(lambda x: 1 if x>0.0 else 0)
        self.train_x = np.array([]).reshape([-1,n_features])
        self.train_y = np.array([]).reshape([-1,1])
        for index, row in self.data.iterrows():
            i = self.data.index.get_loc(index)
            if i<n_features:
                continue
            _x = np.array(self.data[i-n_features+1:i+1]['return']).T.reshape([1, -1])
            _y = self.data.loc[i]['label']
            self.train_x = np.vstack((self.train_x, _x))
            self.train_y = np.vstack((self.train_y, _y))
        self.train_y = self.train_y.reshape([-1])
        return self.train_x, self.train_y, return_range

