#!/usr/bin/env python3

import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

def clean():
    df = pd.read_csv('beijing_house_price.csv')
    df = df.iloc[:,:6].join(df.iloc[:,7]).join(df.iloc[:,9:])
    df = df.astype('float').drop_duplicates().dropna()
    corr = df.corr().iloc[:,8].abs().sort_values(ascending=False)
    return df[corr[:4].index.tolist()]

def beijin(n):
    df = clean()
    X_train, X_test, y_train, y_test = train_test_split(df.iloc[:,1:],
                                       df.iloc[:,0], test_size = 0.3,
                                       random_state = 10)
    y_train = y_train.values.reshape(len(y_train), 1)
    y_test = y_test.values.reshape(len(y_test), 1)
    poly_n = PolynomialFeatures(n)
    poly_X_train = poly_n.fit_transform(X_train)
    poly_X_test = poly_n.fit_transform(X_test)
    model = LinearRegression()
    model.fit(poly_X_train, y_train)
    result = model.predict(poly_X_test)
    mae = mean_absolute_error(result, y_test)
    return mae
print(clean().head())
print('-'*50)
print(beijin(5))
