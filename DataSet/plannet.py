import pandas as pd
import concurrent.futures
from skyfield.api import load, Topos
import numpy as np

def calculate_planet_position(row, ts, observer, planet):
    t = ts.utc(year=row['y'], month=row['m'], day=row['d'], hour=row['h'], minute=row['mm'], second=row['s'])
    planet_position = observer.at(t).observe(planet)
    x, y, z = planet_position.apparent().position.au
    return [row['time'], x, y, z]

def process_chunk(chunk, ts, observer, planet):
    planet_pos_chunk = chunk.apply(calculate_planet_position, axis=1, ts=ts, observer=observer, planet=planet)
    return planet_pos_chunk.values.tolist()

def run(planet_name):
    df = pd.read_csv('D:\Earthquake\DataSet\DATASET.csv')
    df['time'] = pd.to_datetime(df['time'])
    df['y'] = df['time'].dt.year
    df['m'] = df['time'].dt.month
    df['d'] = df['time'].dt.day
    df['h'] = df['time'].dt.hour
    df['mm'] = df['time'].dt.minute
    df['s'] = df['time'].dt.second


    eph = load('de421.bsp')
    earth = eph['earth']
    observer = earth + Topos(latitude_degrees=0, longitude_degrees=0)
    planet = eph[planet_name]
    ts = load.timescale()

    def process_chunk_wrapper(chunk):
        return process_chunk(chunk, ts, observer, planet)

    num_parts = 8
    chunks = np.array_split(df, num_parts)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_chunk_wrapper, chunks))

    planet_pos = [item for sublist in results for item in sublist]

    result_df = pd.DataFrame(planet_pos, columns=['time', 'x', 'y', 'z'])
    print(result_df)
    result_df.to_csv(f'{planet_name}_positions.csv', index=False)


"""
SPICE kernel file 'de421.bsp' has 15 segments
  JD 2414864.50 - JD 2471184.50  (1899-07-28 through 2053-10-08)
      0 -> 1    SOLAR SYSTEM BARYCENTER -> MERCURY BARYCENTER
      0 -> 2    SOLAR SYSTEM BARYCENTER -> VENUS BARYCENTER
      0 -> 3    SOLAR SYSTEM BARYCENTER -> EARTH BARYCENTER
      0 -> 4    SOLAR SYSTEM BARYCENTER -> MARS BARYCENTER
      0 -> 5    SOLAR SYSTEM BARYCENTER -> JUPITER BARYCENTER
      0 -> 6    SOLAR SYSTEM BARYCENTER -> SATURN BARYCENTER
      0 -> 7    SOLAR SYSTEM BARYCENTER -> URANUS BARYCENTER
      0 -> 8    SOLAR SYSTEM BARYCENTER -> NEPTUNE BARYCENTER
      0 -> 9    SOLAR SYSTEM BARYCENTER -> PLUTO BARYCENTER
      0 -> 10   SOLAR SYSTEM BARYCENTER -> SUN
      3 -> 301  EARTH BARYCENTER -> MOON
      3 -> 399  EARTH BARYCENTER -> EARTH
      1 -> 199  MERCURY BARYCENTER -> MERCURY
      2 -> 299  VENUS BARYCENTER -> VENUS
      4 -> 499  MARS BARYCENTER -> MARS
"""

# run('MOON')
# run('MERCURY BARYCENTER')
# run('VENUS BARYCENTER')
# run('MARS BARYCENTER')
# run('JUPITER BARYCENTER')
# run('SATURN BARYCENTER')
# run('SUN')

# run('URANUS BARYCENTER')
# run('NEPTUNE BARYCENTER')


from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.jplhorizons import Horizons
import numpy as np

# list object
object_plannet = ['SUN', '199', '299', '399', '301', '-74', '599', '699', '433', 'Eros', 'Orus', '-49',
                       '-490', '-255', '2000016', '90000190',  
                        'Leucus', 'Eurybates','Polymele', 'Vesta', 'Mathilde', 'Lutetia', 'Donaldjohanson','Braille', 'Annefrank', 
                        'Bennu', 'Itokawa', '-64', 'Apophis', 'Ryugu', '-122911', 'Patroclus', 
                        '90000855', 'Dinkinesh', '20065803' , 'Gaspra', 'Ceres']

df = pd.read_csv('D:\Earthquake\DataSet\DATASET.csv')
df['time'] = pd.to_datetime(df['time'])


def ran(obj: str):
    data_list = []

    for i in range(len(df)):
        epoch = Time(df['time'][i])
        q = Horizons(obj, location='@0', epochs=epoch.tdb.jd)
        tab = q.vectors(refplane='earth')
        c = SkyCoord(tab['x'].quantity, tab['y'].quantity, tab['z'].quantity,
                    representation_type='cartesian', frame='icrs',
                    obstime=epoch)

        x, y, z = np.array(c.cartesian.xyz)
        
        x_scalar, y_scalar, z_scalar = x.item(), y.item(), z.item()
        
        row = [str(df['time'][i]), x_scalar, y_scalar, z_scalar]
        data_list.append(row)

    dt = pd.DataFrame(data_list, columns=['time', 'x', 'y', 'z'])
    dt.to_csv(f'{obj}_position.csv')
    return np.array(data_list)


import concurrent.futures
import numpy as np

def process_chunk(chunk, obj):
    data_list = []

    for i in range(len(chunk)):
        try:
            epoch = Time(chunk['time'].iloc[i])
            q = Horizons(obj, location='@0', epochs=epoch.tdb.jd)
            tab = q.vectors(refplane='earth')
            c = SkyCoord(tab['x'].quantity, tab['y'].quantity, tab['z'].quantity,
                        representation_type='cartesian', frame='icrs',
                        obstime=epoch)

            x, y, z = np.array(c.cartesian.xyz)

            x_scalar, y_scalar, z_scalar = x.item(), y.item(), z.item()

        except Exception as e:
            # print(f"Error processing row {i}: {e}")
            x_scalar, y_scalar, z_scalar = 99, 99, 99

        row = [str(chunk['time'].iloc[i]), x_scalar, y_scalar, z_scalar]
        data_list.append(row)

    return data_list


def process_chunk_wrapper(args):
    chunk, obj = args
    return process_chunk(chunk, obj)

def ran_p(obj):
    num_parts = 8
    chunks = np.array_split(df, num_parts)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_chunk_wrapper, [(chunk, obj) for chunk in chunks]))

    flattened_results = [item for sublist in results for item in sublist]

    dt = pd.DataFrame(flattened_results, columns=['time', 'x', 'y', 'z'])
    dt.to_csv(f'{obj}_position.csv', index=False)
    return flattened_results


pos = ran_p('Orus')
ps = pd.DataFrame(pos, columns=['time', 'x', 'y', 'z'])
print(ps)
ps.to_csv('Orus.csv')