#
import numpy as np
import pandas as pd

def clean():
    df = pd.read_csv('nyc-east-river-bicycle-counts.csv')
    df = df[['Brooklyn Bridge', 'Manhattan Bridge']]
    df = df.astype('int').drop_duplicates().dropna()
    return df

def linear(x, w, b):
    f = x * w + b
    return f

def loss(y, f):
    loss = ((y - f)*(y - f)).mean()
    return loss

def gradient(x, y, f):
    wh = -2 * (x * (y - f)).mean()
    bh = -2 * (y - f).mean()
    #print('wh,bh:',wh,bh)
    return wh, bh

def gradient_descent():
    df = clean()
    x = df.iloc[:,0].values
    y = df.iloc[:,1].values
    w = 0
    b = 0
    lr = 0.0001
    num_iter = 90
    count = 1
    for i in range(num_iter):
        f = linear(x, w, b)
        wh, bh = gradient(x, y, f)
        w -= lr * wh
        b -= lr * bh
        if count % 10 == 0:
            print('w, b count {}: '.format(count), w, b)
        count += 1
    return w, b
a = gradient_descent()
print(a)
