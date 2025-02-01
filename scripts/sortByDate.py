import pandas as pd

# Load the input CSV file
file_path = 'data/processed/all.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Ensure the 'publishedAt' column is in date format
data['publishedAt'] = pd.to_datetime(data['publishedAt']).dt.date

# Group by date and sentiment, count occurrences
sentiment_counts = (
    data.groupby(['publishedAt', 'sentiment'])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# Rename columns for clarity
sentiment_counts.columns.name = None  # Remove hierarchical index names (if any)
sentiment_counts = sentiment_counts.rename(columns={
    'publishedAt': 'Date'
})

# Ensure columns for all sentiment types
for sentiment in ['Positive', 'Negative', 'Neutral']:
    if sentiment not in sentiment_counts.columns:
        sentiment_counts[sentiment] = 0

# Rearrange columns to match desired output order
sentiment_counts = sentiment_counts[['Date', 'Positive', 'Negative', 'Neutral']]

# Save the results to a CSV file
output_file_path = 'data/processed/graphs/dataByTime.csv'  # Desired output file name
sentiment_counts.to_csv(output_file_path, index=False)

print(f"Data saved to {output_file_path}")
