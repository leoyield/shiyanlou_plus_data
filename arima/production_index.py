import pandas as pd
import warnings
from statsmodels.tsa.stattools import arma_order_select_ic
from statsmodels.sandbox.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings('ignore')

def get_data():
    data = pd.read_csv('agriculture.csv')
    return data

def index2period():
    data = get_data()
    index = pd.to_datetime(data.iloc[:, 0].values, format='%Y')
    new_data = data.iloc[:, 1]
    new_data.index = index
    new_data.index = new_data.index.to_period('A')
    return new_data

def get_d():
    data = index2period()
    P = acorr_ljungbox(data)[1]
    d_data = data
    for i in range(1, 5):
        d_data = d_data.diff().dropna()
        P = acorr_ljungbox(d_data)[1]
        if len(P[P<0.05]) / len(P) >= 0.5:
            d = i
            break
    return d, d_data

def arima():
    d, data = get_d()
    p, q = arma_order_select_ic(data.values, ic='aic')['aic_min_order']
    print('p:',p, ' q:',q)
    return p, d, q


if __name__ == '__main__':
    pqd = arima()
    print(pqd)
