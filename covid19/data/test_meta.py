import pandas as pd
df = pd.read_csv('metadata.csv')
selected = df[['cord_uid','sha','publish_time','journal','url']].where(df['sha'].notna())

