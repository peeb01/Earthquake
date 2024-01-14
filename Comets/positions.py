from functon import PositionCalculator
import time

import pandas as pd


df0 = pd.read_csv('D:\\Project\\Earthquake\\DataSet\\new_dataset.csv')
df0['time'] = pd.to_datetime(df0['time'])


start = time.time()
calculator = PositionCalculator()
result = calculator.positions_parallel(df0['time'])
end = time.time()
print(result)
print('time : ', end-start)

result.to_csv('new_2000_2024_position.csv')