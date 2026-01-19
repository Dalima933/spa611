import numpy as np
import matplotlib.pyplot as plt

from astropy import units as u
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, FK5, get_sun
from astropy.time import Time


# ---------------------------
# Given J2000 coordinates of Cygnus A
# ---------------------------
ra_j2000  = "19h59m28.3566s"
dec_j2000 = "+40d44m02.096s"

cyga_j2000 = SkyCoord(ra=ra_j2000, dec=dec_j2000, frame="icrs")

# ---------------------------
# Q1: Does RA/Dec change today?
# ---------------------------
now = Time.now()
cyga_today = cyga_j2000.transform_to(FK5(equinox=now))

print("\n==============================")
print("Q1: Does RA/Dec change today?")
print("==============================")
print("J2000 RA  :", cyga_j2000.ra.to_string(u.hour))
print("J2000 Dec :", cyga_j2000.dec.to_string(u.deg))
print("Today RA  :", cyga_today.ra.to_string(u.hour))
print("Today Dec :", cyga_today.dec.to_string(u.deg))
print("→ Yes. RA/Dec change slowly due to Earth's precession.\n")


# ---------------------------
# Q2: Azimuth & Elevation from IIT Kanpur
# ---------------------------
iitk = EarthLocation(lat=26.5123*u.deg, lon=80.2329*u.deg, height=125*u.m)

altaz = AltAz(obstime=now, location=iitk)
cyga_altaz = cyga_j2000.transform_to(altaz)

print("==============================")
print("Q2: Azimuth & Elevation from IIT Kanpur")
print("==============================")
print("Time :", now.iso)
print("Azimuth   :", cyga_altaz.az.to(u.deg))
print("Elevation :", cyga_altaz.alt.to(u.deg), "\n")


# ---------------------------
# Q3: Polar plot (Az/El over 24h)
# ---------------------------
times = now + np.linspace(0, 24, 144)*u.hour
coords = cyga_j2000.transform_to(AltAz(obstime=times, location=iitk))

az = coords.az.rad
el = coords.alt.deg

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, polar=True)

sc = ax.scatter(az, 90 - el, c=el, cmap="viridis")
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_title("Cygnus A: Azimuth & Elevation over 24h (IIT Kanpur)")
plt.colorbar(sc, label="Elevation (deg)")
plt.show()


# ---------------------------
# Q4: Sun vs Cygnus A over 1 year
# ---------------------------
year = Time("2026-01-01") + np.linspace(0, 365, 366)*u.day
sun_coords = get_sun(year).icrs

plt.figure(figsize=(10, 5))
plt.plot(year.datetime, sun_coords.ra.deg, label="Sun RA")
plt.plot(year.datetime, sun_coords.dec.deg, label="Sun Dec")
plt.hlines(cyga_j2000.ra.deg, year.datetime[0], year.datetime[-1], colors="r", label="Cygnus A RA")
plt.hlines(cyga_j2000.dec.deg, year.datetime[0], year.datetime[-1], colors="g", label="Cygnus A Dec")

plt.xlabel("Date")
plt.ylabel("Degrees")
plt.title("Sun vs Cygnus A: RA/Dec over One Year")
plt.legend()
plt.show()

print("==============================")
print("Q4: Comparison Sun vs Cygnus A")
print("==============================")
print("→ Sun's RA and Dec change continuously over the year.")
print("→ Cygnus A stays almost constant (only tiny precession).")
print("→ So Sun moves across the sky, Cygnus A is fixed in direction.\n")

print("All questions answered & plots generated ✔")
