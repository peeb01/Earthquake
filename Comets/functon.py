import re
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astroquery.jplhorizons import Horizons



class PositionCalculator:

    object_planet = ['SUN', '199', '299', '399', '301', '-74', '599', '699', '433', 'Eros', 'Orus', '-49',
                       '-490', '-255', '2000016', '90000188', '90000190', '90000191', 
                        'Leucus', 'Eurybates','Polymele', 'Vesta', 'Mathilde', 'Lutetia', 'Donaldjohanson','Braille', 'Annefrank', 
                        'Bennu', 'Itokawa', '-64', 'Apophis', 'Ryugu', '-122911', 'Patroclus', 
                        '90000855', 'Dinkinesh', '20065803' , 'Gaspra', 'Ceres']

    @lru_cache(maxsize=None)
    def query_horizons(self, obj, epoch):
        query = Horizons(obj, location='@0', epochs=epoch.tdb.jd)
        table = query.vectors(refplane='earth')
        return table
    def positions_normal(self, times):
        """
        Args:
            times: List of times in UTC format yyyy-mm-dd hh:mm:ss

        Returns:
            results: DataFrame with columns ['Time', 'Object0_X', 'Object0_Y', 'Object0_Z', 'Object1_X', 'Object1_Y', ...]
        """
        results = []

        for time in times:
            row = [time]
            for obj in self.object_planet:
                try:
                    epoch = Time(time)
                    table = self.query_horizons(obj, epoch)
                    coordinates = SkyCoord(table['x'].quantity, table['y'].quantity, table['z'].quantity,
                                           representation_type='cartesian', frame='icrs', obstime=epoch)
                    result_str = str(coordinates)
                    matches = re.findall(r'-?\d+\.\d+', result_str)
                    result_list = [float(match) for match in matches]
                except Exception as e:
                    # print(f"Error for {obj} at time {time}: {e}")
                    result_list = [99, 99, 99]

                row += result_list

            results.append(row)

        columns = ['Time'] + [f'{obj}_{coord}' for obj in self.object_planet for coord in ['X', 'Y', 'Z']]
        results_df = pd.DataFrame(results, columns=columns)
        return results_df
    

    def positions_parallel(self, times):
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.calculate_position_single, time) for time in times]
            results = [future.result() for future in futures]
        return pd.concat(results, ignore_index=True)

    def calculate_position_single(self, time):
        row = [time]
        for obj in self.object_planet:
            try:
                epoch = Time(time)
                query = Horizons(obj, location='@0', epochs=epoch.tdb.jd)
                table = query.vectors(refplane='earth')
                coordinates = SkyCoord(table['x'].quantity, table['y'].quantity, table['z'].quantity,
                                       representation_type='cartesian', frame='icrs', obstime=epoch)
                result_str = str(coordinates)
                matches = re.findall(r'-?\d+\.\d+', result_str)
                result_list = [float(match) for match in matches]
            except Exception as e:
                # print(f"Error for {obj} at time {time}: {e}")
                result_list = [99, 99, 99]

            row += result_list

        columns = ['Time'] + [f'{obj}_{coord}' for obj in self.object_planet for coord in ['X', 'Y', 'Z']]
        return pd.DataFrame([row], columns=columns)


# time_list = ['2023-12-21 15:21:42', '2023-12-22 12:00:00'] 
# calculator = PositionCalculator()
# result_df = calculator.calculate_positions(time_list)

# result_df.to_csv('positions.csv', index=False)