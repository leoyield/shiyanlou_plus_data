from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import pandas as pd

def get_data():
    data = []
    with open('shopping_data.csv') as f:
        lines = f.readlines()
    for line in lines:
        data.append([i for i in line.split(',') if len(i) > 0 and i != '\n'])
    return data

def rule():
    data = get_data()
    te = TransactionEncoder()
    te_ary = te.fit_transform(data)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='confidence',
            min_threshold=0.2)
    return frequent_itemsets, rules

if __name__ == '__main__':
    ru = rule()
    print(ru[0])
    print(ru[1])
