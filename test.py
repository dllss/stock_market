import pandas as pd

# 假设这是你的原始数据
data = {
    'column_name': ['A', 'B', 'C', 'D', 'E'],
    'another_column': ['X', 'Y', 'Z', 'X', 'Y']
}

# 创建DataFrame
df = pd.DataFrame(data)

# 这是你要删除的值
value_to_drop = 'C'

# 创建一个布尔掩码，标记要删除的行
mask = df['column_name'] != value_to_drop

# 使用drop函数删除行
df_dropped = df.drop(df.index[mask])

# 打印修改前的DataFrame
print("修改前的DataFrame:")
print(df)

# 打印修改后的DataFrame
print("\n修改后的DataFrame:")
print(df_dropped)