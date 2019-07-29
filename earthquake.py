#!/usr/bin/env python3

import numpy as np
import pandas as pd

def clean():
    data = pd.read_csv('earthquake.csv')
    df1 = data[['time', 'latitude', 'longitude', 'depth', 'mag']]
    region = []
    for i in data.place.values:
        if ',' in i:
            _, reg = i.split(',', 1)
        else:
            reg = 'None'
        region.append(reg)
    df2 = pd.DataFrame({'region': region}).replace('None', np.nan)
    df_clean = df1.join(df2).dropna().drop_duplicates()
    return df_clean

def mag_region():
    df_clean = clean()
    mag_grade = ['None', 'micro', 'light', 'strong', 'major', 'great']
    df_clean[['mag']].astype('float')
    df_grade = pd.cut(df_clean.mag.values, bins=[
                   df_clean.mag.min() if df_clean.mag.min() < -1 else -1,
                   0, 2, 5, 7, 9,
                   df_clean.mag.max() if df_clean.mag.max() > 10 else 10],
                   right = False,
                   labels = mag_grade)

    df_clean['mag'] = df_grade 
    df_middle = df_clean[['mag', 'region', 'depth']].replace('None', np.nan).dropna()
    df_middle = df_middle.groupby(['mag', 'region']).count().reset_index()
    df_middle.columns = ['mag', 'region', 'times']
    df_final = pd.DataFrame(columns=['mag', 'region', 'times'])
    for i in mag_grade[1:]:
        each_grade = df_middle[df_middle['mag'] == i]
        max_times = each_grade[each_grade['times'] == each_grade.times.max()]
        df_final = pd.concat([df_final, max_times])
    df_final.index = df_final.mag.values
    df_final = df_final[['region', 'times']]
    df_final.index.name = 'mag'
    df_final[['times']] = df_final[['times']].astype('int')
    return df_final

df = mag_region()
print(df.times)
print(df)
