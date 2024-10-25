import os
import pandas as pd

folder_path = 'data'

csv_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.csv')]

dataframes = []

for file in csv_files:
    df = pd.read_csv(file, delimiter=';')
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

output_path = 'combined_data.csv'
combined_df.to_csv(output_path, index=False, sep=';')

output_path