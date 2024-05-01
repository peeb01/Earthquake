from skyfield.api import load, Topos

eph = load('de421.bsp')
# asteroid_data = load('ast343de430.bsp')

observer = Topos(latitude_degrees=0, longitude_degrees=0)


ts = load.timescale()
t = ts.utc(2024, 1, 23, 12, 0, 0)

sun = eph['sun']
earth = eph['earth']
# asteroid = asteroid_data['EROS']

astrometric = sun.at(t).observe(earth)
x, y, z = astrometric.position.au

print(f"At {t}:")
print(f"X: {x:.10f} AU")
print(f"Y: {y:.10f} AU")
print(f"Z: {z:.10f} AU")
