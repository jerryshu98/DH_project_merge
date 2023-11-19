import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.impute import KNNImputer

# File paths
file_path_basic = './data/gender_race_admission_type_charttime_fio2_plateaupressure.csv'
file_path_basic2 = './data/basic_data2.csv'
file_path_O2 = './data/O2_flow.csv'
file_path_vet = './data/ventailation_data.csv'
file_path_vitalsign = './data/data_vitalsign.csv'
file_path_tabaco = './data/stay_id_Tobacco.csv'

# Reading data into dataframes
data_basic_df = pd.read_csv(file_path_basic)
data_basic2_df = pd.read_csv(file_path_basic2)
data_O2_df = pd.read_csv(file_path_O2)
data_vet_df = pd.read_csv(file_path_vet)
data_vitalsign_df = pd.read_csv(file_path_vitalsign)
data_tabaco_df = pd.read_csv(file_path_tabaco)

# Processing ventilation data
ventilation_df = data_vet_df
ventilation_df['charttime'] = pd.to_datetime(ventilation_df['charttime'])
ventilation_df = ventilation_df.sort_values(by=['stay_id', 'charttime'])
ventilation_df = ventilation_df.set_index('charttime')
ventilation_resampled = ventilation_df.groupby('stay_id').resample('H').max()
ventilation_resampled['respiratory_rate_set'] = ventilation_resampled['respiratory_rate_set'].fillna(method='ffill')
ventilation_resampled['tidal_volume_observed'] = ventilation_resampled['tidal_volume_observed'].fillna(method='ffill')
ventilation_resampled['peep'] = ventilation_resampled['peep'].fillna(method='ffill')
ventilation_resampled['minute_ventilation'] = ventilation_resampled['minute_ventilation'].fillna(method='ffill')
ventilation_resampled = ventilation_resampled.drop(columns='stay_id')
ventilation_resampled = ventilation_resampled.reset_index()
ventilation_resampled['subject_id'] = ventilation_resampled.groupby('stay_id')['subject_id'].fillna(method='ffill')

# Processing O2 flow data
o2_df = data_O2_df
o2_df['charttime'] = pd.to_datetime(o2_df['charttime'])
o2_df = o2_df.sort_values(by=['stay_id', 'charttime'])
o2_df = o2_df.set_index('charttime')
o2_resampled = o2_df.groupby('stay_id').resample('H').max()
o2_resampled['O2_flow'].replace('___', pd.NA, inplace=True)
o2_resampled['O2_flow'] = o2_resampled['O2_flow'].fillna(method='ffill')
o2_resampled = o2_resampled.drop(columns='stay_id')
o2_resampled = o2_resampled.reset_index()
o2_resampled['subject_id'] = o2_resampled.groupby('stay_id')['subject_id'].fillna(method='ffill')

# Processing basic data
basic_df = data_basic_df
basic_df['charttime'] = pd.to_datetime(basic_df['charttime'])
basic_df = basic_df.sort_values(by=['stay_id', 'charttime'])
basic_df = basic_df.set_index('charttime')
basic_resampled = basic_df.groupby('stay_id').resample('H').max()
basic_resampled['gender'] = basic_resampled['gender'].fillna(method='ffill')
basic_resampled['race'] = basic_resampled['race'].fillna(method='ffill')
basic_resampled['admission_type'] = basic_resampled['admission_type'].fillna(method='ffill')
basic_resampled['fio2'] = basic_resampled['fio2'].fillna(method='ffill')
basic_resampled['plateau_pressure'] = basic_resampled['plateau_pressure'].fillna(method='ffill')
basic_resampled = basic_resampled.drop(columns=['stay_id', 'hadm_id'])
basic_resampled = basic_resampled.reset_index()
basic_resampled['subject_id'] = basic_resampled.groupby('stay_id')['subject_id'].fillna(method='ffill')

# Processing vitalsign data
vitalsign_df = data_vitalsign_df
vitalsign_df['charttime'] = pd.to_datetime(vitalsign_df['charttime'])
vitalsign_df = vitalsign_df.sort_values(by=['stay_id', 'charttime'])
vitalsign_df = vitalsign_df.set_index('charttime')
vitalsign_resampled = vitalsign_df.groupby('stay_id').resample('H').max()
vitalsign_resampled['heart_rate'] = vitalsign_resampled['heart_rate'].fillna(method='ffill')
vitalsign_resampled['sbp'] = vitalsign_resampled['sbp'].fillna(method='ffill')
vitalsign_resampled['dbp'] = vitalsign_resampled['dbp'].fillna(method='ffill')
vitalsign_resampled['mbp'] = vitalsign_resampled['mbp'].fillna(method='ffill')
vitalsign_resampled = vitalsign_resampled.drop(columns=['stay_id'])
vitalsign_resampled = vitalsign_resampled.reset_index()
vitalsign_resampled['subject_id'] = vitalsign_resampled.groupby('stay_id')['subject_id'].fillna(method='ffill')

# Processing additional basic data
basic2_df = data_basic2_df
imputer = KNNImputer(n_neighbors=2) 
basic2_df[['max_height', 'max_weight']] = imputer.fit_transform(basic2_df[['max_height', 'max_weight']])

# Merging dataframes
merged_df = pd.merge(basic_resampled, basic2_df, on=['stay_id', 'subject_id'], how='outer')
merged_df = pd.merge(merged_df, o2_resampled, on=['stay_id', 'subject_id', 'charttime'], how='outer')
merged_df = pd.merge(merged_df, ventilation_resampled, on=['stay_id', 'subject_id', 'charttime'], how='outer')
merged_df['RSBI'] = merged_df['tidal_volume_observed'] / merged_df['respiratory_rate_set']
merged_df = pd.merge(merged_df, vitalsign_resampled, on=['stay_id', 'subject_id', 'charttime'], how='outer')
merged_df = pd.merge(merged_df, data_tabaco_df, on=['stay_id'], how='inner')
temp_df = merged_df
merged_df = merged_df.drop(columns=['subject_id'])
merged_df.insert(0, 'subject_id', temp_df['subject_id'])

# Filling missing values with mean values based on gender
merged_df['max_height'].fillna(merged_df.groupby('gender')['max_height'].transform('mean'), inplace=True)
merged_df['max_weight'].fillna(merged_df.groupby('gender')['max_weight'].transform('mean'), inplace=True)
merged_df['stay_id2'] = merged_df['stay_id']
merged_df = merged_df.groupby('stay_id2').ffill()

# Saving the merged data to a CSV file
merged_data_path = './data/merged_data.csv'
merged_df.to_csv(merged_data_path, index=False)
