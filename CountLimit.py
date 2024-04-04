"""
获得每日涨跌停统计, tushare limit_list接口获得是每日个股涨跌停情况，
以下代码为，统计每日涨停数和跌停数
"""
import pandas as pd
import numpy as np
import os
base_path = 'stock'
base_path = os.path.join(base_path, 'OtherData')

filename = []
U = []
D = []

for file in os.listdir(base_path):
    if 'limit_list' in file:
        filename.append(file)
        df = pd.read_csv(os.path.join(base_path, file))
        tmp = len(df[df['limit'] == 'U'])
        U.append(tmp)
        tmp = len(df[df['limit'] == 'D'])
        D.append(tmp)


def getDateStr(x):
    return x.split('.')[0].split('_')[-1]

df = pd.DataFrame()
df['file'] = filename
df['U'] = U
df['D'] = D
df['date'] = df['file'].apply(getDateStr)

df = df.sort_values('date').reset_index(drop=True)

df.to_csv(os.path.join('stock', 'limit.csv'), index=None)