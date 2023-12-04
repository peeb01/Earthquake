"""
Calculate distance between earth and plannets
"""

from skyfield.api import load, Topos
import numpy as np

eph = load('de421.bsp')
observer = Topos(latitude_degrees=0, longitude_degrees=0)


sun = eph['sun']
mercury = eph['mercury barycenter']
venus = eph['venus barycenter']
earth = eph['earth']
mars = eph['mars barycenter']
jupiter = eph['jupiter barycenter']
saturn = eph['saturn barycenter']
uranus = eph['uranus barycenter']
neptune = eph['neptune barycenter']

planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

ts = load.timescale()
current_time = ts.now()

earth_position = (eph['earth'] + observer).at(current_time).position.au

for planet in planets:
    planet_position = (planet).at(current_time).position.au 
    distance_km = np.linalg.norm(planet_position - earth_position)
    print(f"Distance between Earth and {str(planet)[49:]}: {distance_km:.10f} AU")
