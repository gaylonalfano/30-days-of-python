import requests

# NOTE ngrok will change each startup
ngrok_url: str = "http://a8a7ca3ccc62.ngrok.io"
endpoint: str = f"{ngrok_url}/box-office-mojo-scraper"

r = requests.post(endpoint)

"""
NOTES:
    - Return r.text since server is set up to return HTML ("Done")
      instead of JSON (Dict).
"""
# print(r.text)
print(r.json()["data"])
