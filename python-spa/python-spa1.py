import requests

url = 'https://spa1.scrape.center/api/movie/?limit=10&offset=0'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

response = requests.get(url, headers=headers)