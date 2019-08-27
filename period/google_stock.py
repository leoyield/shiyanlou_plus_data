import pandas as pd

def get_data():
    data = pd.read_csv('GOOGL.csv')
    return data

def quarter_volume():
    data = get_data()
    index = pd.to_datetime(data.iloc[:, 0].values)
    
    df_pri = pd.DataFrame(data.iloc[:, 1:-1].values,
            columns=data.iloc[:, 1:-1].columns,
            index=index)
    df_pri.index = df_pri.index.to_period('D')
    df_pri = df_pri.resample('Q', convention='start').mean()
    
    df_vol = pd.DataFrame(data.iloc[:, -1])
    df_vol.index = index
    df_vol.index = df_vol.index.to_period('D')
    df_vol = df_vol.resample('Q', convention='start').sum()
    df = pd.concat([df_pri, df_vol], axis=1).sort_values(by='Volume',
             ascending=False)
    return df

if __name__ == '__main__':
    df = quarter_volume()
    print(df.head())
