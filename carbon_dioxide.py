#!/usr/bin/env python3

import pandas as pd
import numpy as np

def co2():
    df_climate = pd.read_excel('ClimateChange.xlsx', sheetname=None)
    df_clean = clean(df_climate)
    df = df_clean[['Income group', 'Country name', 'stat']]
    df_sum = df[['Income group', 'stat']].groupby(by='Income group').sum()
    df_max = df[['Income group', 'stat']].groupby(by='Income group').max()
    df_min = df[['Income group', 'stat']].groupby(by='Income group').min()
    mx_cou_em = pd.DataFrame(columns=['Income group', 'Country name', 'stat'])
    mi_cou_em = pd.DataFrame(columns=['Income group', 'Country name', 'stat'])
    for m in df_max.stat.values:
        cou_em = df[df.stat == m]
        mx_cou_em = pd.concat([mx_cou_em, cou_em])
    for m in df_min.stat.values:
        cou_em = df[df.stat == m]
        mx_cou_em = pd.concat([mi_cou_em, cou_em])
    mx_cou_em = mx_cou_em.set_index(mx_cou_em['Income group'])[['Country name', 'stat']]
    mi_cou_em = mi_cou_em.set_index(mi_cou_em['Income group'])[['Country name', 'stat']]


    df_sum.columns = ['Sum emissions']
    mx_cou_em.columns = ['Highest emission country', 'Highest emissions']
    mi_cou_em.columns = ['Lowest emission country', 'Lowest emissions']
    results = pd.concat([df_sum, mx_cou_em, mi_cou_em], axis=1)
    return mx_cou_em

def clean(df):
    df1 = df['Data'][df['Data']['Series code'] == 'EN.ATM.CO2E.KT']
    df1_data = df1.iloc[:,6:].replace('..', np.nan).astype('float')
    df1_data = df1_data.fillna(method='ffill').fillna(method='bfill').fillna(0).sum(axis=1)

    df1_data = pd.DataFrame({'stat': df1_data}).replace(0, np.nan)
    df1_new = df1.iloc[:,:6].join(df1_data)

    df2 = df['Country'][['Country name', 'Income group']]

    df = pd.merge(df1_new, df2, on='Country name').dropna().drop_duplicates()

    return df

df = co2()
print(df.head())
print(df.shape)
