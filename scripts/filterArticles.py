import csv
import os
from getArticles import initializeCSV
    

def filterArticles(input_path, output_path, start_line, end_line):
    with open(input_path, "r") as input_file:
        reader = csv.DictReader(input_file)
        
        with open(output_path, "a", newline="") as output_file: 
            writer = csv.writer(output_file)
            
            for lineNum, row in enumerate(reader, start=1):
                if lineNum < start_line:
                    continue 
                
                if lineNum > end_line:
                    break
                writer.writerow([
                    "",  # placeholder
                    row["source"],
                    row["title"],
                    row["description"],
                    row["content"],
                    row["url"],
                    row["publishedAt"],
                ])
                
def remove_duplicate_articles(input_path, output_path):
    seen_titles= set()
    with open(input_path, "r", encoding="utf-8") as input_file, open(output_path, "w", newline="", encoding="utf-8") as output_file :
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            title = row["title"]
            if title not in seen_titles:
                seen_titles.add(title)
                writer.writerow(row)  # Write non-duplicate row
            else:
                print("this title is duplicate: ", title)


    
def main():
    duplicated_articles_path = "../data/raw/duplicated_articles.csv"
    unique_articles_file = "../data/raw/articles.csv"
    names = ["saif", "alia", "naz"]
    headers = ["sentiment","category", "source", "title", "description", "content", "url", "publishedAt"]
    print("exists?",os.path.exists(duplicated_articles_path))
    remove_duplicate_articles(duplicated_articles_path, unique_articles_file)

    # for name in names:
    #     filename = f"{name}FullUnprocessedData.csv"
    #     outputFilePath = "data/raw/" + filename
    #     initializeCSV(outputFilePath, headers)
    
    #naz
    # start = 1
    # end = 233
    
    #alia
    # start = 234
    # end = 466
    
    #saif
    start = 467
    end = 700
    # filterArticles(duplicate_articles_path, output_file_path, start, end)           

if __name__ == "__main__":
    main()