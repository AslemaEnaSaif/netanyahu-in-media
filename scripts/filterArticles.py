import csv
import os
from getArticles import initializeCSV
    
headers = ["sentiment","category", "source", "title", "description", "content", "url", "publishedAt"]

def write_articles_slice(input_path, output_path, start_line, end_line):
    with open(input_path, "r", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        
        with open(output_path, "a", newline="", encoding="utf-8") as output_file: 
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

def csv_lines_number(file_path):
    line_count = 0
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for _ in reader:
            line_count += 1
    return line_count

def split_articles(file_path, names):
    slices_number = len(names)
    articles_total_num = csv_lines_number(file_path)
    articles_slices = [(name, index*articles_total_num//slices_number + (1 if index > 0 else 0), (index+1)*articles_total_num//slices_number)  for index, name in enumerate(names) ] 

    for name, start_line, end_line in articles_slices:
        filename = f"{name}_unprocessed_data_oct15_nov15.csv"
        output_file_path = "../data/raw/" + filename
        initializeCSV(output_file_path, headers)
        write_articles_slice(file_path, output_file_path, start_line, end_line)



def main():
    duplicated_articles_path = "../data/raw/duplicated_articles_15oct_15nov.csv"
    unique_articles_file = "../data/raw/articles_15oct_15nov.csv"
    names = ["saif", "alia", "naz"]
    print("exists?",os.path.exists(duplicated_articles_path))
    # remove_duplicate_articles(duplicated_articles_path, unique_articles_file)

    split_articles(unique_articles_file,names)



if __name__ == "__main__":
    main()