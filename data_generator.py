import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta

pd.options.mode.chained_assignment = None 
def find_data(raw_data_df,stay_id,target_time, flag, r_v, dod):
    target_time = pd.to_datetime(target_time).floor('H')
    df = raw_data_df
    df['charttime'] = pd.to_datetime(df['charttime'])
    df = df[df['stay_id'] == stay_id]
    start_time = target_time - pd.Timedelta(hours=24)
    selected_data = df[(df['charttime'] <= target_time)]
    selected_data['label'] = flag
    if np.isnan(r_v):
        selected_data['Rev_h'] = -1000
    else:
         selected_data['Rev_h'] = r_v
    if np.isnan(dod):
        selected_data['dod_h'] = -1000
    else:
         selected_data['dod_h'] = dod
    selected_data = selected_data.sort_values(by=['stay_id', 'charttime'])
    return selected_data.tail(24)


raw_data_path = './data/merged_data.csv'
flag_data_path = './data/ground_truth_11_21.csv'

raw_data_df = pd.read_csv(raw_data_path)
flag_data_df = pd.read_csv(flag_data_path)
cancate_data = pd.DataFrame()

for index, row in flag_data_df.iterrows():
    data_now = find_data(raw_data_df,row['stay_id'], row['endtime'],row['label'], row['re_vent_time_diff'], row['weaning_till_dod_hr'])
    if index > 0:
        cancate_data = pd.concat([cancate_data, data_now], ignore_index=False)
    else:
        cancate_data = data_now
        shape = data_now.shape


print(cancate_data)
print(cancate_data['stay_id'].nunique())
cancate_data.to_csv('./data/prive_24h_data.csv', index=False)
