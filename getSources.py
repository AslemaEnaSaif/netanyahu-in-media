import requests

nazifa_key = '8d1ef3a971f1422aac484c57ddba03b0'

url = 'https://newsapi.org/v2/sources'
country = "us"

params = {
    'language': 'en',
    'country': country,
    'apiKey': nazifa_key
}

response = requests.get(url, params=params)

if (response.status_code == 200):
    data = response.json()
    sources = data.get('sources', [])
    
    for source in sources:
        print(f"{source['id']}", end=",")
else:
    print('failed')        