#!/usr/bin/env python3

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

def clean():
    df = pd.read_csv('beijing_house_price.csv')
    df = df.iloc[:,:6].join(df.iloc[:,7]).join(df.iloc[:,9:])
    df = df.astype('float').drop_duplicates().dropna()
    corr = df.corr().iloc[:,8].abs().sort_values(ascending=False)
    return df[corr[:4].index.tolist()]

def beijin(n):
    df = clean()
    split_num = int(len(df)*0.7)
    X_train = df.iloc[:split_num,1:]
    y_train = df.iloc[:split_num,0]
    X_test = df.iloc[split_num:,1:]
    y_test = df.iloc[split_num:,0]

    poly_n = PolynomialFeatures(n)
    poly_X_train = poly_n.fit_transform(X_train)
    poly_X_test = poly_n.fit_transform(X_test)
    model = LinearRegression()
    model.fit(poly_X_train, y_train.values.reshape(len(y_train), 1))
    result = model.predict(poly_X_test)

    return result #poly_X_train.shape, y_train.values.reshape(len(y_train), 1).shape
print(clean().head())
print('-'*50)
print(beijin(1))
