import pandas as pd
import os 
import pickle

class Simulation():
    def __init__(self, data_x, data_y, length_frac, contracts = 10000, commission = 0.1):
        self.test_feat = data_x[int(len(data_x)*length_frac):]
        self.test_x = data_x[int(len(data_x)*length_frac):,-1]
        self.test_y = data_y[int(len(data_x)*length_frac):]
        self.contracts = contracts
        self.commission = commission


    def simulate(self, model_loc, sim_loc, return_range):
            df_trade = pd.DataFrame(self.test_x, columns=['return'])
            df_trade['label']  = self.test_y
            if not os.path.exists(model_loc):
                raise ValueError("No Model Found")
            else:
                model = pickle.load(open(model_loc, 'rb'))
            df_trade['pred']   = model.predict(self.test_feat)
            df_trade['won']    = df_trade['label'] == df_trade['pred']
            df_trade['return'] = df_trade['return'].shift(-1) * return_range
            df_trade.drop(df_trade.index[len(df_trade)-1], inplace=True)
            def calc_profit(row):
                if row['won']:
                    return abs(row['return'])*self.contracts - self.commission
                else:
                    return -abs(row['return'])*self.contracts - self.commission

            df_trade['pnl'] = df_trade.apply(lambda row: calc_profit(row), axis=1)
            df_trade['equity'] = df_trade['pnl'].cumsum()
            n_win_trades = float(df_trade[df_trade['pnl']>0.0]['pnl'].count())
            n_los_trades = float(df_trade[df_trade['pnl']<0.0]['pnl'].count())
            path = model_loc.split('/')[-1].split('.')[0]
            with open(sim_loc+'/'+path+'.txt', 'w') as f:
                f.write("Net Profit            : $%.2f\n" % df_trade.tail(1)['equity'])
                f.write("Number Winning Trades : %d\n" % n_win_trades)
                f.write("Number Losing Trades  : %d\n" % n_los_trades)
                f.write("Percent Profitable    : %.2f%%\n" % (100*n_win_trades/(n_win_trades + n_los_trades)))
                f.write("Avg Win Trade         : $%.3f\n" % df_trade[df_trade['pnl']>0.0]['pnl'].mean())
                f.write("Avg Los Trade         : $%.3f\n" % df_trade[df_trade['pnl']<0.0]['pnl'].mean())
                f.write("Largest Win Trade     : $%.3f\n" % df_trade[df_trade['pnl']>0.0]['pnl'].max())
                f.write("Largest Los Trade     : $%.3f\n" % df_trade[df_trade['pnl']<0.0]['pnl'].min())
                f.write("Profit Factor         : %.2f\n" % abs(df_trade[df_trade['pnl']>0.0]['pnl'].sum()/df_trade[df_trade['pnl']<0.0]['pnl'].sum()))
            f.close()
            return df_trade