import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = "city_temperature.csv"

# Load dataset
df = pd.read_csv(file_path, low_memory=False)

print("Columns in dataset:", df.columns)

# -----------------------------
# Safe Date Creation (FIXED)
# -----------------------------
if {'Year', 'Month', 'Day'}.issubset(df.columns):
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']], errors='coerce')
    df = df.dropna(subset=['Date'])  # remove invalid dates
else:
    raise KeyError("Year, Month, Day columns are required")

# -----------------------------
# Check Temperature column
# -----------------------------
if 'AvgTemperature' not in df.columns:
    raise KeyError("AvgTemperature column not found")

# -----------------------------
# Basic Info
# -----------------------------
print("\nDataset Info:")
print(df.info())

print("\nFirst 5 rows:")
print(df.head())

# -----------------------------
# Data Cleaning
# -----------------------------
df = df.dropna(subset=['AvgTemperature'])
df['AvgTemperature'] = pd.to_numeric(df['AvgTemperature'], errors='coerce')

# Remove unrealistic values
df = df[(df['AvgTemperature'] > -50) & (df['AvgTemperature'] < 150)]

# -----------------------------
# City column check
# -----------------------------
if 'City' not in df.columns:
    raise KeyError("City column not found")

# Select first city
city_name = df['City'].iloc[0]
city_df = df[df['City'] == city_name].copy()

# Sort by date
city_df = city_df.sort_values(by='Date')

# -----------------------------
# Statistics
# -----------------------------
temps = city_df['AvgTemperature'].values

print(f"\nStatistics for {city_name}:")
print("Mean Temp:", np.mean(temps))
print("Max Temp:", np.max(temps))
print("Min Temp:", np.min(temps))

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(10, 5))
plt.plot(city_df['Date'], city_df['AvgTemperature'])

plt.title(f"Temperature Trend - {city_name}")
plt.xlabel("Date")
plt.ylabel("Avg Temperature")

plt.xticks(rotation=45)
plt.tight_layout()

plt.show()