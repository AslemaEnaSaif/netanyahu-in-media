import requests
import json

# for mediastack.com
access_key = "497ffbadc2c6eca8a8893b7834bfb343"
url = 'http://api.mediastack.com/v1/news'

params = {
    'access_key': access_key, 
    'countries': 'us,ca',
    'languages': 'en',
    'keywords': 'Netanyahu',
    'sources': 'The New York Times, Google News World US, cnn, jewishpress, reporter herald, dailymail, latimes, bostonherald',
    'date': '2023-07-15,2024-08-14',
    'sort': 'popularity',
    'limit': 100
    }

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    formatted_json = json.dumps(data, indent=4, ensure_ascii=False)
    print(formatted_json)
    
    # Save formatted JSON to a file
    with open("formatted_results.json", "w", encoding="utf-8") as f:
        f.write(formatted_json)
    
else:
    print("failed request")
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)