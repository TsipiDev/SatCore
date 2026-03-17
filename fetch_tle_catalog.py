import requests

url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=TLE"
response = requests.get(url)

with open("data/tle_data/active.tle", "w") as f:
    f.write(response.text)

lines = response.text.strip().splitlines()
total = len(lines) // 3
print(f"Downloaded {total} satellites")