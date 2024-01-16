import re
import pandas as pd


from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.jplhorizons import Horizons


# list object
object_plannet = ['SUN', '199', '299', '399', '301', '-74', '599', '699', '433', 'Eros', 'Orus', '-49',
                       '-490', '-255', '2000016', '90000190',  
                        'Leucus', 'Eurybates','Polymele', 'Vesta', 'Mathilde', 'Lutetia', 'Donaldjohanson','Braille', 'Annefrank', 
                        'Bennu', 'Itokawa', '-64', 'Apophis', 'Ryugu', '-122911', 'Patroclus', 
                        '90000855', 'Dinkinesh', '20065803' , 'Gaspra', 'Ceres']

def calculate_position(obj, time):
    """
    Args : 
        obj     : obj name str
        time    : time (utc) format yyyy-mm-dd
    """
    epoch = Time(time)
    q = Horizons(obj, location='@0', epochs=epoch.tdb.jd)
    tab = q.vectors(refplane='earth')
    c = SkyCoord(tab['x'].quantity, tab['y'].quantity, tab['z'].quantity,
                representation_type='cartesian', frame='icrs',
                obstime=epoch)
    result = str(c)
    matches = re.findall(r'-?\d+\.\d+', result)
    result_list = [float(match) for match in matches]
    return result_list

time = pd.read_csv('D:\Project\Earthquake\Comets\\time.csv')
time['time'] = pd.to_datetime(time['Date'])
time = time[time['time'] >= '2000-01-01'].astype(str)
time = time['time'][:100]
print(len(time))

import threading


rl = []
columns = ['time', 'Object', 'x', 'y', 'z']

class Main(threading.Thread):
    def __init__(self, i):
        super().__init__()
        self.i = i

    def run(self):
        lq = []
        for t in time:
            try:
                ls = calculate_position(object_plannet[self.i], t)
                lq.extend([t, object_plannet[self.i]] + ls)
            except Exception as e:
                # print(f"Error calculating position for object {i} at time {t}: {e}")
                lq.extend([t, object_plannet[self.i], 99, 99, 99])
        rl.append(lq)

results_df = pd.DataFrame(columns=columns)

threads = [Main(i) for i in range(len(object_plannet))]
for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

for result in rl:
    results_df = pd.concat([results_df, pd.DataFrame([result], columns=columns)], ignore_index=True)

# Save the DataFrame to a CSV file
results_df.to_csv('file_data_asteroid.csv', index=False)


# results = rl
# print(rl)
# results_df = pd.DataFrame(results, columns=columns)
# results_df.to_csv('file_data_asteroid101.csv')