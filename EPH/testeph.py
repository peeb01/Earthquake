from skyfield.api import load, Topos

eph = load('de421.bsp')
print(eph)
# 9/24/1950  12:23:00 PM

observer = Topos(latitude_degrees=0, longitude_degrees=0)
ts = load.timescale()
t = ts.utc(1950, 9, 24, 12, 23, 0)
sun = eph['VENUS']
earth = eph['earth']
astrometric = sun.at(t).observe(earth)

distance = astrometric.distance().au  
print(distance)


list_eph = ['SUN', 'MERCURY BARYCENTER', 'VENUS BARYCENTER', 'MOON', 'MARS', 'JUPITER BARYCENTER', 'SATURN BARYCENTER', 'URANUS BARYCENTER', 'NEPTUNE BARYCENTER']
