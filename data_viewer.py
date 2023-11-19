import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import math

stay_id_to_find = 30005707
if len(sys.argv) >= 2:
    stay_id_to_find = int(sys.argv[1])
data_merge = './data/prive_24h_data.csv'
data_merge_datalist = pd.read_csv(data_merge)
stay_id_data = data_merge_datalist[data_merge_datalist['stay_id'] == stay_id_to_find]
df_str = stay_id_data.to_string(index=False)
for line in df_str.split('\n'):
    print(line)

print("------------------------------------------")
data_merge = './data/ground_truth_11_18.csv'
data_merge_datalist = pd.read_csv(data_merge)
stay_id_data = data_merge_datalist[data_merge_datalist['stay_id'] == stay_id_to_find]
df_str = stay_id_data.to_string(index=False)
for line in df_str.split('\n'):
    print(line)


