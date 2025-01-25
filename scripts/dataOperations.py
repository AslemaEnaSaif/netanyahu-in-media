import pandas as pd

input_csv = 'all.csv'
df = pd.read_csv(input_csv)

summary = df['source'].value_counts()
print(summary)


def replace_wrong_categories():
    category_mapping = {
    'Legal affairs': 'Legal Affairs',
    'Local Affairs': 'Israel Local Affairs',
    'Non-Governmatal Opinions': 'Non-Governmental Opinion',
    'israel local affairs': 'Israel Local Affairs'
}
    df['category'] = df['category'].replace(category_mapping)
    output_csv = 'replaced_categories_output.csv'
    df.to_csv(output_csv, index=False)

def strip():
    df["sentiment"] = df["sentiment"].str.strip()
    output_csv = 'trimmed_all.csv'
    df.to_csv(output_csv, index=False)


def categorize(file):
    df = pd.read_csv(file)

    summary = df.groupby(['category', 'sentiment']).size().unstack(fill_value=0)

    summary['total_count'] = summary.sum(axis=1)

    summary.reset_index(inplace=True)

    output_csv = 'aggregated_output.csv'
    summary.to_csv(output_csv, index=False)

# categorize(input_csv)