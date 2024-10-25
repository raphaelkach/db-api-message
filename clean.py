import pandas as pd


df = pd.read_csv('combined_data.csv', sep=';')


df = df.drop_duplicates()

df.to_csv('clean_message_db.csv', index=False)