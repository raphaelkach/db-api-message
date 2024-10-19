import os
import pandas as pd
from datetime import datetime

def combine_csv_files():
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')

    data_folder = 'data'

    csv_files = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.startswith(f's_bahn_stuttgart_daten_{date_str}') and f.endswith('.csv')]

    if not csv_files:
        print("Keine CSV-Dateien für heute gefunden.")
        return

    df_list = []
    for file in csv_files:
        df = pd.read_csv(file, delimiter=';')
        df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)

    daily_data_folder = 'daily_data'
    if not os.path.exists(daily_data_folder):
        os.makedirs(daily_data_folder)

    combined_csv_file = os.path.join(daily_data_folder, f's_bahn_stuttgart_daten_{date_str}.csv')
    combined_df.to_csv(combined_csv_file, index=False, sep=';')

    print(f"Zusammengefasste Datei gespeichert: {combined_csv_file}")

if __name__ == '__main__':
    combine_csv_files()
