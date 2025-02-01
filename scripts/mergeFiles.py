import pandas as pd

# File paths for the input files
file_paths = [
    'data/processed/alia_processed_complete_adjusted_latin1.csv',
    'data/processed/naz_processed_complete_adjusted.csv',
    'data/processed/saif_processed_complete_adjusted.csv'
]

# Initialize an empty list to hold DataFrames
dataframes = []

# Read each file and append the DataFrame to the list
for file_path in file_paths:
    try:
        # Adjust encoding if necessary
        if 'latin1' in file_path:
            df = pd.read_csv(file_path, encoding='latin1')
        else:
            df = pd.read_csv(file_path)
        dataframes.append(df)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Combine all DataFrames
combined_df = pd.concat(dataframes, ignore_index=True)

# Convert 'publishedAt' column to datetime
combined_df['publishedAt'] = pd.to_datetime(combined_df['publishedAt'], errors='coerce')

# Drop rows with invalid 'publishedAt' values
combined_df = combined_df.dropna(subset=['publishedAt'])

# Sort the DataFrame by 'publishedAt'
sorted_df = combined_df.sort_values(by='publishedAt')

# Save the sorted DataFrame to a CSV file
output_file_path = 'data/processed/all_processed_completed.csv'
sorted_df.to_csv(output_file_path, index=False)

print(f"Sorted articles saved to {output_file_path}")
