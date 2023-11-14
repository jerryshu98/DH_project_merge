import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
import math

data_basic = './data/gender_race_admission_type_charttime_fio2_plateaupressure.csv'
data_basic2 = './data/basic_data2.csv'
data_O2 = './data/O2_flow.csv'
data_vet = './data/ventailation_data.csv'
data_GT = './data/ground_truth_meta_data.csv'

data_basic_datalist = pd.read_csv(data_basic)
data_basic2_datalist = pd.read_csv(data_basic2)
data_O2_datalist = pd.read_csv(data_O2)
data_vet_datalist = pd.read_csv(data_vet)
data_GT_datalist = pd.read_csv(data_GT)

df = data_vet_datalist
df['charttime'] = pd.to_datetime(df['charttime'])
df = df.sort_values(by=['stay_id', 'charttime'])
df = df.set_index('charttime')
df_resampled = df.groupby('stay_id').resample('H').max()
df_resampled['respiratory_rate_set'] = df_resampled['respiratory_rate_set'].fillna(method='ffill')
df_resampled['tidal_volume_observed'] = df_resampled['tidal_volume_observed'].fillna(method='ffill')
df_resampled['peep'] = df_resampled['peep'].fillna(method='ffill')
df_resampled['minute_ventilation'] = df_resampled['minute_ventilation'].fillna(method='ffill')
df_resampled = df_resampled.drop(columns='stay_id')
df_resampled = df_resampled.reset_index()
df_resampled['subject_id'] = df_resampled.groupby('stay_id')['subject_id'].fillna(method='ffill')


df1 = data_O2_datalist
df1['charttime'] = pd.to_datetime(df1['charttime'])
df1 = df1.sort_values(by=['stay_id', 'charttime'])
df1 = df1.set_index('charttime')
df_resampled1 = df1.groupby('stay_id').resample('H').max()
df_resampled1['O2_flow'] = df_resampled1['O2_flow'].fillna(method='ffill')
df_resampled1 = df_resampled1.drop(columns='stay_id')
df_resampled1 = df_resampled1.reset_index()
df_resampled1['subject_id'] = df_resampled1.groupby('stay_id')['subject_id'].fillna(method='ffill')

df2 = data_basic_datalist
df2['charttime'] = pd.to_datetime(df2['charttime'])
df2 = df2.sort_values(by=['stay_id', 'charttime'])
df2 = df2.set_index('charttime')
df_resampled2 = df2.groupby('stay_id').resample('H').max()
df_resampled2['gender'] = df_resampled2['gender'].fillna(method='ffill')
df_resampled2['race'] = df_resampled2['race'].fillna(method='ffill')
df_resampled2['admission_type'] = df_resampled2['admission_type'].fillna(method='ffill')
df_resampled2['fio2'] = df_resampled2['fio2'].fillna(method='ffill')
df_resampled2['plateau_pressure'] = df_resampled2['plateau_pressure'].fillna(method='ffill')
df_resampled2 = df_resampled2.drop(columns='stay_id')
df_resampled2 = df_resampled2.drop(columns='hadm_id')
df_resampled2 = df_resampled2.reset_index()
df_resampled2['subject_id'] = df_resampled2.groupby('stay_id')['subject_id'].fillna(method='ffill')

df3 = data_basic2_datalist
df4 = pd.DataFrame()
df4['subject_id']= data_GT_datalist['subject_id']
df4['stay_id'] = data_GT_datalist['stay_id']
df4['label'] = data_GT_datalist['label']
df4 = df4.drop_duplicates()

df_merged = pd.merge(df_resampled2, df3, on=['stay_id', 'subject_id'], how='inner')
df_merged = pd.merge(df_merged, df_resampled1, on=['stay_id', 'subject_id', 'charttime'], how='inner')
df_merged = pd.merge(df_merged, df_resampled, on=['stay_id', 'subject_id', 'charttime'], how='inner')
df_merged['RSBI'] = df_merged['tidal_volume_observed']/df_merged['respiratory_rate_set']
df_merged = pd.merge(df_merged, df4, on=['stay_id', 'subject_id'], how='inner')
df_temp = df_merged
df_merged = df_merged.drop(columns=['subject_id'])
df_merged.insert(0, 'subject_id', df_temp['subject_id'])


merge_data = './data/merged_data.csv'
df_merged.to_csv(merge_data, index=False)