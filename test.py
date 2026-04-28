import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- Constants ---
latitude_deg = 52.52                 # Berlin latitude
base_radius_mm = 30                 # Base cam radius in mm
scale_mm_per_hr = 20               # Scale (1 hour = 20 mm)
days = np.arange(1, 366)           # Day of year

# --- Solar Calculations ---
latitude_rad = np.radians(latitude_deg)
decl_deg = 23.44 * np.sin(np.radians((360 / 365) * (days - 81)))
decl_rad = np.radians(decl_deg)

cos_H0 = -np.tan(latitude_rad) * np.tan(decl_rad)
cos_H0 = np.clip(cos_H0, -1.0, 1.0)
H0_rad = np.arccos(cos_H0)
H0_deg = np.degrees(H0_rad)

L = (2 * H0_deg) / 15  # Day length in hours
sunrise = 12 - L / 2
sunset = 12 + L / 2

# --- Cam Displacement (scaled and shifted above base radius) ---
sunrise_mm = base_radius_mm + (sunrise - np.min(sunrise)) * scale_mm_per_hr
sunset_mm = base_radius_mm + (sunset - np.min(sunset)) * scale_mm_per_hr
daylen_mm = base_radius_mm + (L - np.min(L)) * scale_mm_per_hr

# --- Polar Angles (360° for 365 days) ---
theta_deg = np.linspace(0, 360, 365)
theta_rad = np.radians(theta_deg)

# --- Convert to (X, Y) Coordinates ---
def polar_to_cartesian(r_values, theta_values_deg):
    theta_rad = np.radians(theta_values_deg)
    x = r_values * np.cos(theta_rad)
    y = r_values * np.sin(theta_rad)
    return x, y

# --- Save as CSV ---
def save_csv_profile(filename, r_values):
    x, y = polar_to_cartesian(r_values, theta_deg)
    df = pd.DataFrame({
        "Day": days,
        "Angle (deg)": theta_deg,
        "X": x,
        "Y": y
    })
    df.to_csv(filename, index=False)
    print(f"[✓] Saved: {filename}")

save_csv_profile("berlin_sunrise_cam.csv", sunrise_mm)
save_csv_profile("berlin_sunset_cam.csv", sunset_mm)
save_csv_profile("berlin_daylength_cam.csv", daylen_mm)

# --- Plot the Cam Profiles ---
plt.figure(figsize=(8, 8))
ax = plt.subplot(111, polar=True)
ax.plot(theta_rad, sunrise_mm, label="Sunrise Cam", color='orange')
ax.plot(theta_rad, sunset_mm, label="Sunset Cam", color='red')
ax.plot(theta_rad, daylen_mm, label="Daylength Cam", color='green')
ax.set_title("Circular Cam Profiles – Berlin", va='bottom')
ax.legend(loc='upper right')
plt.tight_layout()
plt.show()
