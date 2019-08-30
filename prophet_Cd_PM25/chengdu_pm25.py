import warnings
import pandas as pd
from fbprophet import Prophet

warnings.filterwarnings('ignore')

def get_data():
    data = pd.read_csv('Chengdu_HourlyPM25.csv')
    return data

def clearn_data():
    df = get_data()
    index = pd.to_datetime(df.iloc[:, 2].values, format='%m/%d/%Y %H:%M')
    data = df.iloc[:, 3]
    data = data.replace(-999, pd.np.nan)
    data = data.fillna(method='ffill').fillna(method='bfill')
    data.index = index
    data.index = data.index.to_period('H')
    data = data.resample('D').mean()
    data.index = data.index.to_timestamp()
    data = data.reset_index()
    data.columns = ['ds', 'y']
    return data

def additive():
    data = clearn_data()
    model = Prophet()
    model.fit(data)
    future = model.make_future_dataframe(periods=365, freq='D')
    pred = model.predict(future).iloc[len(data):, :]
    result = pred[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    forecast = result.iloc[:, 1:]
    forecast.index = pred.iloc[:, 0]
    forecast.to_csv('forecast.csv')
    return forecast

if __name__ == '__main__':
    fo = additive()
    print(fo.head())
    print(fo.tail())
