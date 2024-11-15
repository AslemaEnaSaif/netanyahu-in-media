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
                

def main():
    name = "saif"
    filename = f"{name}FullUnprocessedData.csv"
    headers = ["category", "source", "title", "description", "content", "url", "publishedAt"]
    
    outputFilePath = "data/raw/" + filename
    inputFilePath = "data/raw/articles.csv"
    initializeCSV(outputFilePath, headers)
    
    #naz
    # start = 1
    # end = 233
    
    #alia
    # start = 234
    # end = 466
    
    #saif
    start = 467
    end = 700
    
    filterArticles(inputFilePath, outputFilePath, start, end)           

if __name__ == "__main__":
    main()