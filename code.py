import requests 
import json

saif_key="bf293b62915341ab96753bafd9e2da75"

sources= f"https://newsapi.org/v2/top-headlines/sources?country=us&apiKey={saif_key}"
natenyahu= f"https://newsapi.org/v2/everything?q=netanyahu&apiKey={saif_key}"

response = requests.get(natenyahu)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    with open("results.json", "w") as f:
        json.dump(data, f)
    print(data)
else:
    print(f"Failed to retrieve data.\n {response}")