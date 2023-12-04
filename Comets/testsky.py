"""
calculate distance from comets to earth

"""
# code from : https://stackoverflow.com/questions/40418675/how-to-calculate-distance-to-comets-using-skyfields

from skyfield.api import load
from skyfield.constants import GM_SUN_Pitjeva_2005_km3_s2 as GM_SUN
from skyfield.data import mpc

ts = load.timescale()

eph = load('de421.bsp')
sun, earth = eph['sun'], eph['earth']

with load.open(mpc.COMET_URL) as f:
    comets = mpc.load_comets_dataframe(f)
comets = comets.set_index('designation', drop=False)
row = comets.loc['1P/Halley']
comet = sun + mpc.comet_orbit(row, ts, GM_SUN)

t = ts.utc(2023, 12, 4)
ra, dec, distance = earth.at(t).observe(comet).radec()

print('Distance in AU:', distance.au)