#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

def clean():
    df = pd.read_excel('ClimateChange.xlsx', sheetname='Data')
    df_co2 = df[df['Series code'] == 'EN.ATM.CO2E.KT']
    df_gdp = df[df['Series code'] == 'NY.GDP.MKTP.CD']
    co2_values = df_co2.iloc[:,6:].replace('..', pd.np.NAN)
    gdp_values = df_gdp.iloc[:,6:].replace('..', pd.np.NAN)
    co2_fill = co2_values.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1).fillna(0)
    gdp_fill = gdp_values.fillna(method='ffill', axis=1).fillna(method='bfill', axis=1).fillna(0)
    co2_sum = co2_fill.astype('float').sum(axis=1)
    gdp_sum = gdp_fill.astype('float').sum(axis=1)

    co2 = pd.DataFrame({'CO2-SUM': co2_sum}).set_index(df_co2['Country code'])
    gdp = pd.DataFrame({'GDP-SUM': gdp_sum}).set_index(df_gdp['Country code'])
    clean_data = co2.join(gdp).drop_duplicates().dropna()

    return clean_data

def co2_gdp_plot():
    df = clean()
    df.iloc[:,0] = ((df.iloc[:,0] - df.iloc[:,0].min()) /
                    ((df.iloc[:,0].max() - df.iloc[:,0].min())))
    df.iloc[:,1] = ((df.iloc[:,1] - df.iloc[:,1].min()) /
                    ((df.iloc[:,1].max() - df.iloc[:,1].min())))

    fig, axes = plt.subplots()
    df.plot(ax=axes)
    plt.xlabel('Counties')
    plt.ylabel('Values')
    plt.title('GDP-CO2')

    c_list = ['CHN', 'USA', 'GBR', 'FRA','RUS']
    cn_list = []
    c_index = []
    c_values = {}
    for i in range(len(df)):
        if df.iloc[i,:].name in c_list:
            cn_list.append(df.iloc[i,:].name)
            c_index.append(i)
            c_values[df.iloc[i,:].name] = round(df.iloc[i,:], 3).tolist()

    china = c_values['CHN']
    return axes, china

china = co2_gdp_plot()
print(china[1])
