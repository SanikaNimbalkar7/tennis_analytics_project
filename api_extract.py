import requests
import json

API_KEY = "YOUR_SPORTRADAR_API_KEY"  # Replace with your API key

def fetch_data(endpoint):
    url = f"https://api.sportradar.com/tennis/trial/v3/en/{endpoint}?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {endpoint}: {response.status_code}")
        return None

if __name__ == "__main__":
    competitions = fetch_data("competitions.json")
    complexes = fetch_data("complexes.json")
    doubles_rankings = fetch_data("rankings/doubles.json")

    # Save JSON locally for later use
    with open("competitions.json", "w") as f:
        json.dump(competitions, f, indent=4)
    with open("complexes.json", "w") as f:
        json.dump(complexes, f, indent=4)
    with open("doubles_rankings.json", "w") as f:
        json.dump(doubles_rankings, f, indent=4)

    print("✅ API data fetched and saved locally")
