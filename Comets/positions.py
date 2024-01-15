from functon import PositionCalculator, Position
import time

import pandas as pd

# print('RUN 6000000++')


df0 = pd.read_csv('D:\Project\Earthquake\Comets\\time.csv')
df0['Date'] = pd.to_datetime(df0['Date']).astype(str)

# df0 = df0[(df0['time'] > '2000-01-01') ]       #& (df0['time'] <= '2005-01-01 00:00:00
# df0 = df0[(df0['time'] > '2010-01-01 00:00:00') & (df0['time'] <= '2020-01-01 00:00:00')]
# print(len(df0))

start = time.time()
calculator = PositionCalculator()
# result = calculator.positions_parallel(df0['time'][:100000])
# result = calculator.positions_parallel(df0['time'][100000:200000])
# result = calculator.positions_parallel(df0['time'][200000:300000])
# result = calculator.positions_parallel(df0['time'][300000:400000])
# result = calculator.positions_parallel(df0['time'][400000:500000])
# result = calculator.positions_parallel(df0['time'][500000:600000])
print(df0['Date'][0])

result = calculator.positions_normal(df0['Date'][0])
end = time.time()
# result = calculator.positions_parallel('2000-01-01')
print(result)
print('time : ', end-start)

# result.to_csv('new_allstar_plus_position.csv')
