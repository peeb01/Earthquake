import pandas as pd

df = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\\RAW_DATA_ASTEROIDS.csv') 


def parse_date(value):
    try:
        return pd.to_datetime(value, format='%m/%d/%Y')
    except ValueError:
        try:
            return pd.to_datetime(value, format='%Y-%m-%d')
        except ValueError:

            return pd.NaT
        

df['Time'] = df['Time'].apply(parse_date)

df['Time'].fillna('1900-01-01', inplace=True)

df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%Y-%m-%d')
print(df)
df.to_csv('AsteroidCT.csv')


