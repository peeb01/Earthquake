import pandas as pd
import re
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.jplhorizons import Horizons


df = pd.read_csv('D:\Project\Earthquake\Comets\\raw_asteroid\AsteroidCT.csv')
df['Time'] = pd.to_datetime(df['Time'])
print(df)
