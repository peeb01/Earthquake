import pandas as pd
import numpy as np

df = pd.read_csv('D:\Earthquake\DataSet\DATASET_UPDATE.csv')

latitude = df['latitude'].values.astype(np.int32)
longitude = df['longitude'].values.astype(np.int32)


# Create DataFrames from the generated data
lat_df = pd.DataFrame({'latitude': latitude})
lon_df = pd.DataFrame({'longitude': longitude})
# print(lat_df)

unique_latitudes = np.unique(lat_df)
unique_longitudes = np.unique(lon_df)

# # Display the unique latitudes and longitudes
# print("Unique Latitudes:")
# print(unique_latitudes)
# print("\nUnique Longitudes:")
# print(unique_longitudes)


# Convert latitude and longitude columns to one-hot encoded matrices
latitude_one_hot = pd.get_dummies(lat_df['latitude']).values.astype(np.float32)
longitude_one_hot = pd.get_dummies(lon_df['longitude']).values.astype(np.float32)


# Display the one-hot encoded matrices
print("Latitude One-Hot Encoded Matrix:")
print(latitude_one_hot)

print("\nLongitude One-Hot Encoded Matrix:")
print(longitude_one_hot)

