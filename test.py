import pandas as pd

# 读取两个CSV文件
file1_path = './data/merged_data.csv'
file2_path = './data/merged_data2.csv'

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)

# 检查两个DataFrame是否相同
if df1.equals(df2):
    print("两个CSV文件相同")
else:
    print("两个CSV文件不同")
print(df2.columns)