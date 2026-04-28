import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


LATITUDE_DEG = 52.52        # Berlin
LOCATION_NAME = "Berlin"
CAM_SCALE_MM_PER_HOUR = 20  # 1 hour = 20 mm mechanical displacement
NUM_DAYS = 365

days = np.arange(1, NUM_DAYS + 1)
latitude_rad = np.radians(LATITUDE_DEG)

# Solar declination δ(n)
decl_deg = 23.44 * np.sin(np.radians((360 / 365) * (days - 81)))
decl_rad = np.radians(decl_deg)

# Hour angle H₀
cos_H0 = -np.tan(latitude_rad) * np.tan(decl_rad)
cos_H0 = np.clip(cos_H0, -1.0, 1.0)
H0_rad = np.arccos(cos_H0)
H0_deg = np.degrees(H0_rad)

# Day length in hours
L = (2 * H0_deg) / 15

# Sunrise and Sunset times
sunrise = 12 - (L / 2)
sunset = 12 + (L / 2)

# Convert to Cam Profile (in mm)
sunrise_mm = (sunrise - np.min(sunrise)) * CAM_SCALE_MM_PER_HOUR
sunset_mm = (sunset - np.min(sunset)) * CAM_SCALE_MM_PER_HOUR
daylength_mm = (L - np.min(L)) * CAM_SCALE_MM_PER_HOUR


# Plot Standard Time Functions
plt.figure(figsize=(10, 5))
plt.plot(days, sunrise, label="Sunrise (hr)", color='orange')
plt.plot(days, sunset, label="Sunset (hr)", color='red')
plt.plot(days, L, label="Day Length (hr)", color='green')
plt.title(f"Sunrise, Sunset, Day Length - {LOCATION_NAME}")
plt.xlabel("Day of Year")
plt.ylabel("Time (hours)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# Plot Cam Profiles (Centered)

plt.figure(figsize=(10, 5))
plt.plot(days, sunrise_mm, label="Sunrise Cam (mm)", color='orange')
plt.plot(days, sunset_mm, label="Sunset Cam (mm)", color='red')
plt.plot(days, daylength_mm, label="Day Length Cam (mm)", color='green')
plt.title(f"Cam Displacement Profiles - {LOCATION_NAME}")
plt.xlabel("Day of Year")
plt.ylabel("Displacement (mm)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

