import re
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import traceback
import asyncio
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed


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

    def positions_parallel(self, times):
        results = []
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.calculate_position_single, time, obj): (time, obj) for time in times for obj in self.object_planet}

            for future in as_completed(futures):
                time, obj = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    # Handle exception for the specific time and object
                    print(f"Error for object {obj} at time {time}: {e}")

        df = pd.concat(results, ignore_index=True)
        df['Object_Name'] = pd.Categorical(df['Object_Name'], categories=self.object_planet, ordered=True)
        df.sort_values(['Time', 'Object_Name'], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def calculate_position_single(self, time, obj):
        try:
            epoch = Time(str(time))
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

        return pd.DataFrame([[time, obj] + result_list], columns=['Time', 'Object_Name', 'X', 'Y', 'Z'])
    

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
    



class Position:

    object_planet = ['SUN', '199', '299', '399', '301', '-74', '599', '699', '433', 'Eros', 'Orus', '-49',
                     '-490', '-255', '2000016', '90000188', '90000190', '90000191', 
                     'Leucus', 'Eurybates', 'Polymele', 'Vesta', 'Mathilde', 'Lutetia', 'Donaldjohanson', 'Braille', 'Annefrank', 
                     'Bennu', 'Itokawa', '-64', 'Apophis', 'Ryugu', '-122911', 'Patroclus', 
                     '90000855', 'Dinkinesh', '20065803' , 'Gaspra', 'Ceres']

    async def calculate_position_single_async(self, time, obj):
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

        return obj, result_list

    async def positions_parallel_async(self, times):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            tasks = [self.calculate_position_single_async(time, obj) for time in times for obj in self.object_planet]
            results = await asyncio.gather(*tasks)

        data_dict = {}
        for obj, result_list in results:
            if obj not in data_dict:
                data_dict[obj] = result_list
            else:
                data_dict[obj] += result_list

        columns = ['Time'] + [f'{obj}_{coord}' for obj in self.object_planet for coord in ['X', 'Y', 'Z']]
        rows = [[time] + data_dict[obj] for time in times for obj in self.object_planet]
        return pd.DataFrame(rows, columns=columns)
    


# time_list = ['2023-12-21 15:21:42', '2023-12-22 12:00:00'] 
# calculator = PositionCalculator()
# result_df = calculator.calculate_positions(time_list)

# result_df.to_csv('positions.csv', index=False)
    
