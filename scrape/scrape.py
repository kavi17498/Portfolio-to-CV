import requests
baseURL = "https://r.jina.ai/"
@app.get("/scrape/{url}")
def getwebcontent(url):
        url = baseURL + url
        response = requests.get(url)
        return response.json()