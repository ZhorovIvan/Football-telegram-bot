import requests

url = "https://sportscore1.p.rapidapi.com/teams/1/events"

querystring = {"page":"1"}

headers = {
	"X-RapidAPI-Host": "sportscore1.p.rapidapi.com",
	"X-RapidAPI-Key": "18222134ecmsh6ecdd1171f1abedp130975jsn929db9efc17a"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
