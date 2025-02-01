import pandas as pd
import math
from collections import Counter

def calculate_tfidf_by_category(data, category_filter):
    # Filter data by category
    filtered_data = data[data['category'].str.contains(category_filter, case=False, na=False)]
    
    if filtered_data.empty:
        print(f"No articles found for category: {category_filter}")
        return

    # Combine titles and descriptions
    filtered_data['text'] = filtered_data['title'].fillna('') + ' ' + filtered_data['description'].fillna('')

    # Tokenize and remove the word 'Netanyahu'
    documents = [
        [word.lower() for word in text.split() if word.lower() != 'netanyahu']
        for text in filtered_data['text']
    ]

    # Flatten the list of tokens per document into a single list
    document_strings = [' '.join(doc) for doc in documents]

    # Calculate Term Frequency (TF)
    def compute_tf(document):
        word_counts = Counter(document)
        total_words = len(document)
        return {word: count / total_words for word, count in word_counts.items()}

    # Calculate Inverse Document Frequency (IDF)
    def compute_idf(documents):
        total_docs = len(documents)
        word_doc_counts = Counter()
        for document in documents:
            unique_words = set(document)
            word_doc_counts.update(unique_words)
        return {word: math.log(total_docs / (1 + count)) for word, count in word_doc_counts.items()}

    # Calculate TF-IDF
    def compute_tf_idf(documents):
        tf_scores = [compute_tf(doc) for doc in documents]
        idf_scores = compute_idf(documents)
        tf_idf_scores = []
        for tf in tf_scores:
            tf_idf_scores.append({word: tf[word] * idf_scores[word] for word in tf})
        return tf_idf_scores

    # Calculate TF-IDF scores
    tf_idf_scores = compute_tf_idf(documents)

    # Combine all TF-IDF scores into a single dictionary and sum them across all documents
    combined_scores = Counter()
    for doc_scores in tf_idf_scores:
        combined_scores.update(doc_scores)

    # Get the top 10 words by TF-IDF score
    top_words = combined_scores.most_common(10)

    print(f"Top 10 TF-IDF words for category '{category_filter}':")
    for word, score in top_words:
        print(f"{word}: {score}")

def main():
    # Load the CSV file
    file_path = '/Users/nazifaahmed/Desktop/netanyahu-in-media/data/processed/naz_processed_complete.csv'
    data = pd.read_csv(file_path)
    
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
        calculate_tfidf_by_category(data, categoryInput)

if __name__ == "__main__":
    main()
