import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import math
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or '3' to suppress all messages
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import roc_auc_score, accuracy_score
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
label_encoder = LabelEncoder()
pd.options.mode.chained_assignment = None

def check_missing_values(df):
    
    if df.isna().any().any():
        return 1 
    else:
        return 0 

def get_label(id_df):
    label = 0
    if not check_missing_values(id_df):
            label = id_df['label'].iloc[0]
            if label == 1:
                label = -72
            else:
                if id_df['Rev_h'].iloc[0] != -1000:
                    label = 48 - id_df['Rev_h'].iloc[0]
                elif id_df['dod_h'].iloc[0] != -1000 and id_df['dod_h'].iloc[0]>0 and id_df['dod_h'].iloc[0]<48:
                    label = (96 - id_df['dod_h'].iloc[0]*2)
                else:
                    label = 96 
    return label


def get_diff_value(df,colname,start, end):
    start = 23 - start
    end = 23 - end
    df = df.reset_index()
    return (df[colname][end]+df[colname][end-1]+df[colname][end-2]) - (df[colname][start]+df[colname][start+1]+df[colname][start+2])

def get_max_min(df,colname):
    max_value = df[colname].max()
    min_value = df[colname].min()
    result = max_value - min_value
    return result

def get_min(df, col):
    if df.empty or col not in df.columns:
        return float('nan')
    else:
        return df[col].min()

def get_max(df, col):
    if df.empty or col not in df.columns:
        return float('nan')
    else:
        return df[col].max()

def get_mean(df, col):
    return df[col].mean()

aug_columns = ['spo2','peep','heart_rate','respiratory_rate_set','plateau_pressure','tidal_volume_observed','fio2','O2_flow','sbp','dbp','mbp','resp_rate','RSBI','minute_ventilation']

def NN_data(flag_data_df, data_df,label_df,  hour = 23):
    total_x = []
    total_y = []
    for index, row in flag_data_df.iterrows():
        id_df = data_df[data_df['stay_id'] == row['stay_id']]
        id_df_label = label_df[label_df['stay_id'] == row['stay_id']]
        if not check_missing_values(id_df):
            label = get_label(id_df_label)
            id_df = id_df.drop(columns='stay_id')
            id_df = id_df.drop(columns='label')
            id_df = id_df.drop(columns='charttime')
            id_df = id_df.drop(columns='Rev_h')
            #id_df = id_df.drop(columns='dod_h')

            
            zero_hr_values = id_df.iloc[hour, :].values
            #zero_hr_values = generate_more_feature(id_df, aug_columns ,zero_hr_values)

            #zero_hr_values = np.append(zero_hr_values,  get_TVF_diff(id_df))
            total_x.append(zero_hr_values)
            total_y.append(label)
    total_x = np.array(total_x)
    total_y = np.array(total_y).reshape(-1, 1)
    return total_x, total_y

label_path = './data/data_by_table/pre_24h_data_v3.csv'
flag_data_path = './data/data_by_table/ground_truth.csv'
raw_data_path = './data/data_by_table/pre_24_merged_29_rows_11_28.csv'

data_df = pd.read_csv(raw_data_path)
flag_data_df = pd.read_csv(flag_data_path)
label_df = pd.read_csv(label_path)
data_df['BMI'] = data_df['weight_kg'] / ((data_df['height_cm'] / 100) ** 2)
data_df['gender'] = label_encoder.fit_transform(data_df['gender'])
data_df['race'] = label_encoder.fit_transform(data_df['race'])
data_df['first_careunit'] = label_encoder.fit_transform(data_df['first_careunit'])
data_df['admission_type'] = label_encoder.fit_transform(data_df['admission_type'])
data_df['insurance'] = label_encoder.fit_transform(data_df['insurance'])
data_df = data_df.drop(columns=['height_cm', 'weight_kg'])
data_df['RSBI'] =  data_df['tidal_volume_observed'] / data_df['resp_rate']
data_df['minute_ventilation'] = data_df['tidal_volume_observed'] * data_df['resp_rate']
print(data_df.columns)
print(data_df['charttime'])



total_x, total_y = NN_data(flag_data_df, data_df, label_df, 23)
print(total_x.shape)
print(total_y.shape)