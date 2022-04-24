import requests

url = "https://api-football-beta.p.rapidapi.com/timezone"

headers = {
	"X-RapidAPI-Host": "api-football-beta.p.rapidapi.com",
	"X-RapidAPI-Key": "18222134ecmsh6ecdd1171f1abedp130975jsn929db9efc17a"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
