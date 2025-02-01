import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import string

def calculate_tfidf_by_category(data, category_filter, output_dir):
    # Filter data by category
    filtered_data = data[data['category'].str.contains(category_filter, case=False, na=False)]
    
    if filtered_data.empty:
        print(f"No articles found for category: {category_filter}")
        return

    # Combine titles and descriptions
    filtered_data = filtered_data.copy()
    filtered_data.loc[:, 'Text'] = filtered_data['title'].fillna('') + ' ' + filtered_data['description'].fillna('')

    def custom_tokenizer(text):
        # Normalize apostrophes
        text = text.replace("’", "'").replace("‘", "'")  # Replace smart quotes with standard apostrophe
        text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
        text = text.lower()  # Convert text to lowercase
        text = text.replace("prime minister", "")  # Remove specific phrases

        # Tokenize
        tokens = text.split()

        # Normalize words
        normalized_tokens = []
        for word in tokens:
            if word == "says" or word == "said":
                normalized_tokens.append("said")  # Combine "says" and "said" into "say"
            elif word.endswith("'s") or (word.endswith("s") and word[:-1].lower() == "israel"):
                # Normalize possessive 's or plural 's for "Israel"
                normalized_tokens.append("israel")
            else:
                normalized_tokens.append(word)

        # Exclude specific words
        return [word for word in normalized_tokens if word not in {'netanyahu', 'benjamin'}]


    # Calculate TF-IDF
    vectorizer = TfidfVectorizer(tokenizer=custom_tokenizer, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(filtered_data['Text'])
    
    # Get feature names (words) and their scores
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.sum(axis=0).A1  # Sum scores across all documents
    word_scores = dict(zip(feature_names, tfidf_scores))

    # Find top 10 words
    top_words = Counter(word_scores).most_common(10)

    # Prepare data for CSV
    words, scores = zip(*top_words)
    tfidf_data = pd.DataFrame({'word': words, 'score': [round(score, 4) for score in scores]})

    # Replace space characters in filenames
    safe_category_name = category_filter.replace(' ', '_').replace('/', '_')
    file_name = f"{safe_category_name}_tfidf.csv"
    output_path = os.path.join(output_dir, file_name)

    # Save
    tfidf_data.to_csv(output_path, index=False)
    print(f"Saved TF-IDF results to {output_path}")

def main():
    # Load
    file_path = '/Users/nazifaahmed/Desktop/netanyahu-in-media/data/processed/all_processed_completed.csv'
    data = pd.read_csv(file_path)
    
    output_dir = '/Users/nazifaahmed/Desktop/netanyahu-in-media/data/tfidf'
    os.makedirs(output_dir, exist_ok=True)
    
    categories = [
        "Non-American Israel Relations",
        "Israel Local Affairs",
        "Israel American Relations",
        "Non-Governmental Opinion",
        "Israel Iran/Lebanon Conflict",
        "Israel Palestine Conflict",
        "Israel Political Affairs",
        "Legal Affairs"
    ]
    
    for category in categories:
        categoryInput = category
        calculate_tfidf_by_category(data, categoryInput, output_dir)

if __name__ == "__main__":
    main()
