import pandas as pd

# Function to standardize the format of 'publishedAt'
def format_date(date_str):
    try:
        # Attempt to parse the date and convert it to 'YYYY-MM-DD'
        return pd.to_datetime(date_str).strftime('%Y-%m-%d')
    except Exception:
        # Return the original string if parsing fails
        return date_str

# Load the CSV files
file_paths = [
    'data/processed/alia_processed_complete.csv'
]

for file_path in file_paths:
    try:
        # Attempt to read the CSV file with proper encoding
        df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')

        # Check if 'publishedAt' column exists
        if 'publishedAt' in df.columns:
            # Apply the function to the 'publishedAt' column
            df['publishedAt'] = df['publishedAt'].apply(format_date)

            # Save the modified DataFrame back to the CSV file
            output_path = file_path.replace('.csv', '_adjusted.csv')
            df.to_csv(output_path, index=False)
            print(f"Adjusted file saved at: {output_path}")
        else:
            print(f"'publishedAt' column not found in {file_path}.")
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError: Could not process {file_path}. Attempting with 'latin1' encoding.")
        try:
            df = pd.read_csv(file_path, encoding='latin1', on_bad_lines='skip')
            
            # Repeat the processing steps with 'latin1' encoding
            if 'publishedAt' in df.columns:
                df['publishedAt'] = df['publishedAt'].apply(format_date)
                output_path = file_path.replace('.csv', '_adjusted_latin1.csv')
                df.to_csv(output_path, index=False)
                print(f"Adjusted file saved at: {output_path} (latin1 encoding used)")
            else:
                print(f"'publishedAt' column not found in {file_path}.")
        except Exception as e:
            print(f"Error processing file {file_path} with latin1 encoding: {e}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
