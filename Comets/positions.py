from functon import PositionCalculator, Position
import time

import pandas as pd


df0 = pd.read_csv('D:\\Project\\Earthquake\\DataSet\\new_dataset.csv')
df0['time'] = pd.to_datetime(df0['time'])

df0 = df0[(df0['time'] > '2000-01-01 00:00:00') & (df0['time'] <= '2010-01-01 00:00:00')]
# df0 = df0[(df0['time'] > '2010-01-01 00:00:00') & (df0['time'] <= '2020-01-01 00:00:00')]
print(len(df0))

start = time.time()
calculator = PositionCalculator()
result = calculator.positions_parallel(df0['time'])
end = time.time()
print(result)
print('time : ', end-start)

result.to_csv('new_2000_2010_position.csv')