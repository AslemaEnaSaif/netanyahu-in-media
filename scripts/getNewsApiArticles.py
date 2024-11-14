import requests
import csv
import os
import time

def getArticle(url, params):
    print("sending request")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("successfully received articles")
        return response.json()
    else:
        print("ran into error")
        return None

def initializeCSV(filename, headers):
    if not os.path.exists(filename):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Adding the headers

def writeInCSV(filename, data):
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        for article in data["articles"]:
            # removing all new line and returns, and if none is returned by content, or description, it will be an empty string.
            content = article.get("content", "")
            if content:
                content = content.replace("\n", " ").replace("\r", " ")

            description = article.get("description", "")
            if description:
                description = description.replace("\n", " ").replace("\r", " ")
            
            writer.writerow([
                article["source"]["name"], 
                article.get("title",""),
                description,
                content,
                article.get("url"),
                article.get("published")
            ])

def main():
    api_key = '8d1ef3a971f1422aac484c57ddba03b0'
    url = 'https://newsapi.org/v2/everything'
    
    sources = "Fox News,The American Conservative,Washington Times,Financial Post,The Globe And Mail,The Hill,ABC News,CBC News,CNN,NBC"
    key_words = "netanyahu OR Netanyahu"
    
    params = {
        "apiKey": api_key,
        "q": key_words,
        "searchIn": "title",
        "language": "en",
        "sortBy": "relevancy",
    }
    headers = ["source", "title", "description", "content", "url", "publishedAt"]
    
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)  # Create the data directory if it doesn't exist
    filename = os.path.join(data_dir, "articles.csv")  # Full path to the CSV file
    
    data = getArticle(url, params)
    
    for results in range (0,7):
        data = getArticle(url, params)
    
        if data:
            print("data accessed")
            initializeCSV(filename, headers)
            writeInCSV(filename, data)
            
            time.sleep(1)
        
if (__name__ == "__main__"):
    main()
    