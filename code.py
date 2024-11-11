import requests 
import json

saif_key="bf293b62915341ab96753bafd9e2da75"

sources= f"https://newsapi.org/v2/top-headlines/sources?country=us&apiKey={saif_key}"
natenyahu= f'https://newsapi.org/v2/everything?q=+netanyahu&searchIn=title&apiKey={saif_key}'
# cannot specify a country filter with the endpoint /everything, we have to manually filter the sources
# Api defaults
    #gives one page worth of result and each page has 100 returns by default
    # sorts by publishedAt, newest articles come first
# we need to think about tweeking the paramters to suit our needs, a lot of decisions will be taken and need to be documented
    # diversify timings
    # diversify sources based on political spectrum


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