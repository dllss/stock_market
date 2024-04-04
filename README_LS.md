### 文件信息
\stock
  \LimitData\{ts_code}.csv # 股票的每日涨跌停信息数据
  \MoneyData\{ts_code}.csv # 个股资金流向（大单、小单、）
  \OldData\{ts_code}_NormalData.csv # 指数以及股票历史数据
  \OtherData\ggt_daily.csv # 港股通每日成交统计数据
  \OtherData\moneyflow_hsgt.csv # 沪深港通资金流向
  \OtherData\limit_list_{date}.csv # 涨跌停股票数据
  company_info.csv # 股票的基础信息数据，包括股票代码、名称、上市日期、退市日期等
  limit.csv # 获得每日涨跌停统计
  SSE.csv # 上交所指数信息
  SZSE.csv # 深交所指数信息

###  zip()函数
函数说明：
zip()可以将两个可迭代对象中的对应元素打包成一个个元组，然后返回这些元组组成的列表
如果各个迭代器的元素个数不一致，则返回列表长度与最短的对象相同，利用 * 号操作符，可以将元组解压为列表
```
>>> a = [1,2,3]
>>> b = [4,5,6]
>>> c = [4,5,6,7,8]
>>> zipped = zip(a,b)     # 打包为元组的列表
[(1, 4), (2, 5), (3, 6)]
>>> zip(a,c)              # 元素个数与最短的列表一致
[(1, 4), (2, 5), (3, 6)]
>>> zip(*zipped)          # 与 zip 相反，*zipped 可理解为解压，返回二维矩阵式
[(1, 2, 3), (4, 5, 6)]
```

### dict()函数
函数说明：
dict()创建字典，可以传入元组列表创建字典，也可以通过zip得到元组列表后来创建字典

### 通过zip得到元组列表后来创建字典:
```
>>> d = dict(zip(['one', 'two', 'three'], [1, 2, 3])) # 映射函数方式来构造字典
>>> print(d)
{'three': 3, 'two': 2, 'one': 1}

>>> class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
>>> class_names_to_ids = dict(zip(class_names, range(len(class_names))))
>>> print(class_names_to_ids)
{'daisy': 0, 'dandelion': 1, 'roses': 2, 'sunflowers': 3, 'tulips': 4}
```