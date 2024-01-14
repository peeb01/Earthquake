from functon import PositionCalculator, Position
import time

import pandas as pd

print('RUN 6000000++')

df0 = pd.read_csv('D:\\Project\\Earthquake\\DataSet\\new_dataset.csv')
df0['time'] = pd.to_datetime(df0['time']).dt.strftime('%Y-%m-%d %H:%M:%S')

df0 = df0[(df0['time'] > '2000-01-01 00:00:00') ]       #& (df0['time'] <= '2005-01-01 00:00:00
# df0 = df0[(df0['time'] > '2010-01-01 00:00:00') & (df0['time'] <= '2020-01-01 00:00:00')]
print(len(df0))

start = time.time()
calculator = PositionCalculator()
# result = calculator.positions_parallel(df0['time'][:100000])
# result = calculator.positions_parallel(df0['time'][100000:200000])
# result = calculator.positions_parallel(df0['time'][200000:300000])
# result = calculator.positions_parallel(df0['time'][300000:400000])
# result = calculator.positions_parallel(df0['time'][400000:500000])
# result = calculator.positions_parallel(df0['time'][500000:600000])
result = calculator.positions_parallel(df0['time'][600000:])
end = time.time()
print(result)
print('time : ', end-start)

result.to_csv('new_6000000_plus_position.csv')


