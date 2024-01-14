from functon import PositionCalculator, Position
import time

import pandas as pd

print('RUN 3000000')

df0 = pd.read_csv('new_dataset.csv')
df0['time'] = pd.to_datetime(df0['time']).dt.strftime('%Y-%m-%d %H:%M:%S')

df0 = df0[(df0['time'] > '2000-01-01 00:00:00') ]       #& (df0['time'] <= '2005-01-01 00:00:00
# df0 = df0[(df0['time'] > '2010-01-01 00:00:00') & (df0['time'] <= '2020-01-01 00:00:00')]
# print(len(df0))

start = time.time()
calculator = PositionCalculator()
# result = calculator.positions_parallel(df0['time'][:100000])
# result = calculator.positions_parallel(df0['time'][100000:200000])
result = calculator.positions_parallel(df0['time'][200000:300000])

end = time.time()
print(result)
print('time : ', end-start)

result.to_csv('new_3000000_position.csv')