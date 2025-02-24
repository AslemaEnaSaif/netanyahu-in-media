import requests
import csv
import os
import time
from datetime import datetime, timedelta

saif_key = "bf293b62915341ab96753bafd9e2da75"
nazifa_key = "8d1ef3a971f1422aac484c57ddba03b0"
alia_key = "7a42207e01934347aaeb6ccdf82aaf05"

def getArticles(url, params):
    print("sending request")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print("successfully received articles")
        return response.json()
    else:
        print(f"Ran into error: {response.status_code}")
        print("Error details:", response.text)  # Print the full error message
        return None

def initializeCSV(filename, headers):
    if not os.path.exists(filename):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Adding the headers

def writeInCSV(filename, data, not_accepted_sources):
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for article in data["articles"]:
            if article["source"]["name"] in not_accepted_sources:
                continue
            
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
                article.get("publishedAt")
            ])

def generate_date_intervals(start_date, end_date, interval_days=3):
    """Generate a list of (from, to) date tuples for the given date range split by interval_days."""
    intervals = []
    current_start = start_date
    while current_start < end_date:
        current_end = min(current_start + timedelta(days=interval_days), end_date)
        intervals.append((current_start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d')))
        current_start = current_end + timedelta(days=1)
    return intervals

def generate_half_day_intervals(start_date, end_date):
    """Generate a list of (from, to) datetime tuples for half-day intervals."""
    intervals = []
    current_start = start_date
    while current_start < end_date:
        current_end = min(current_start + timedelta(hours=12), end_date)
        intervals.append((current_start.isoformat(), current_end.isoformat()))
        current_start = current_end
    return intervals

def main():
    api_key = saif_key
    url = 'https://newsapi.org/v2/everything'
    key_words = "netanyahu OR Netanyahu"
    
    headers = ["source", "title", "description", "content", "url", "publishedAt"]
    not_accepted_sources = [
        "Ibtimes.com.au",
        "Bangkok Post",
        "Protothema.gr",
        "Dagospia.com",
        "Ibtimes.com.au",
        "Www.gov.uk",
        "Checkyourfact.com",
        "Nakedcapitalism.com",
        # "BBC News", #?
        # "The-sun.com", #?
        "Nakedcapitalism.com",
        "RT",
        "Sputnikglobe.com",
        # "The Week Magazine", #?
        "Juancole.com",
        "[Removed]",
        # "DW (English)", #?
        "Politicalwire.com",
        "CNA",
        "Globalsecurity.org",
        "Hurriyet Daily News",
        "Legalinsurrection.com",
        "Independent.ie",
        "TheJournal.ie",
        # "The Jerusalem Post", #?
        # "Americanthinker.com", #?
        "NDTV News",
        "The Times of India",
        "Israelnationalnews.com",
        "Omny.fm",
        "Slashdot.org",
        "Inter Press Service",
        "Setopati.com",
        "Dianeravitch.net",
        # "Electronicintifada.net", # not sure about this one #?
        "Jewishnews.co.uk",
        "Times of Malta",
        "Tbsnews.net",
        "Japan Today",
        # "Sky.com", #?
        "ABC News (AU)",
        "The Punch",
        "The Online Citizen",
        "The Irish Times"
        ]
    
    
    data_dir = "data/raw"
    os.makedirs(data_dir, exist_ok=True)  # create the data directory if it doesn't exist
    file = "duplicated_articles_16oct_16nov.csv"
    filename = os.path.join(data_dir, file)  # full path to the CSV file
    initializeCSV(filename, headers)  # initialize CSV file with headers

    start_date = datetime(2024, 10, 16)
    end_date = datetime(2024, 11, 16)
    
    # generating date intervals
    date_intervals = generate_half_day_intervals(start_date, end_date)

    print(date_intervals)
    
    # fetch for each date interval
    for from_date, to_date in date_intervals:
        params = {
            "apiKey": api_key,
            "q": key_words,
            "searchIn": "title",
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 100,
            "from": from_date,
            "to": to_date
        }
        
        data = getArticles(url, params)
        print(data["totalResults"])

        if data:
            print(f"Data accessed for date range {from_date} to {to_date}")
            writeInCSV(filename, data, not_accepted_sources)
            time.sleep(1) 
        else:
            print(f"Failed to retrieve data for date range {from_date} to {to_date}")
        
if (__name__ == "__main__"):
    main()
    