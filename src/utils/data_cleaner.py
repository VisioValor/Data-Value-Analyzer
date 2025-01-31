import pandas as pd
import numpy as np

# Load the dataset
file_path = 'datasets_metadata_all_categories_filtered.xlsx'
df = pd.read_excel(file_path)

# Display the first few rows of the dataset
print(df.head())

# Check for missing values
print(df.isnull().sum())

# Handle missing values
# Fill missing numerical values with the median
numerical_columns = df.select_dtypes(include=[np.number]).columns
df[numerical_columns] = df[numerical_columns].fillna(df[numerical_columns].median())

# Fill missing categorical values with the mode
categorical_columns = df.select_dtypes(include=[object]).columns
df[categorical_columns] = df[categorical_columns].fillna(df[categorical_columns].mode().iloc[0])

# Convert categorical variables to numerical using one-hot encoding
df = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

# Normalize numerical data
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

# Check the cleaned dataset
print(df.head())

# Save the cleaned dataset to a new file
df.to_csv('cleaned_datasets_metadata.csv', index=False)