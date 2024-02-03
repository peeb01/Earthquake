import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.jplhorizons import Horizons




def calculate_position(obj_list, time):
    try:
        epoch = Time(time)
        positions = []
        for obj_name in obj_list:
            q = Horizons(obj_name, location='@0', epochs=epoch.tdb.jd)
            tab = q.vectors(refplane='earth')
            c = SkyCoord(tab['x'].quantity, tab['y'].quantity, tab['z'].quantity,
                         representation_type='cartesian', frame='icrs',
                         obstime=epoch)

            x = c.cartesian.x.value
            y = c.cartesian.y.value
            z = c.cartesian.z.value

            positions.extend([x, y, z])

        return positions

    except Exception as e:
        # print(f"Error calculating positions at time {time}")
        return [99] * (len(obj_list) * 3)

def process_chunk(chunk, object_planet):
    positions = chunk.apply(lambda row: pd.Series(calculate_position(object_planet, row['Time'])), axis=1)

    # Unpack positions into separate columns with a different naming convention
    for i, obj_name in enumerate(object_planet):
        chunk[f'{obj_name}_new_x'] = positions[i * 3]
        chunk[f'{obj_name}_new_y'] = positions[i * 3 + 1]
        chunk[f'{obj_name}_new_z'] = positions[i * 3 + 2]

    return chunk

object_planet = ['SUN', '199', '299', '399', '301', '599', '699', '433', 'Eros', 'Orus',
                 'Leucus', 'Eurybates', 'Polymele', 'Vesta', 'Mathilde', 'Lutetia', 
                 'Donaldjohanson', 'Braille', 'Annefrank', 'Bennu', 'Itokawa', 'Apophis',
                 'Ryugu', 'Patroclus', '90000855', 'Dinkinesh', 'Gaspra', 'Ceres']

def main():
    # df = pd.read_csv('D:\Earthquake\Machine Learning Model\DataSetJP.csv')
    df = pd.read_csv('D:\Earthquake\Comets\\raw_asteroid\DATA TRASH\CLEAR101_P4.csv')
    df['Time'] = pd.to_datetime(df['Time'])

    no_use = ['-74', '-49', '-490', '-255', '2000016', '20065803', '-64']
    df = df[(~df['Object_Name'].isin(no_use))]

    num_threads = 8
    chunks = np.array_split(df, num_threads)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(process_chunk, chunks, [object_planet]*num_threads))

    df = pd.concat(results, ignore_index=True)
    df.to_csv('HELPJME.csv', index=False)


main()
