import requests
from requests.exceptions import HTTPError

temp = 0.0
appt = 0.0
hum  = 0
wind = 0
rain = 0.0

try:
    response = requests.get('http://www.bom.gov.au/fwo/XXX.json') # Edit this match the json file at the bottom of the observation page for the target location you want to display
    response.raise_for_status()
    # access JSOn content
    jsonResponse = response.json()
    #print("Entire JSON response")
    #print(jsonResponse)
    temp = float(jsonResponse["observations"]["data"][0]["air_temp"])
    appt = float(jsonResponse["observations"]["data"][0]["apparent_t"])
    hum  = int(jsonResponse["observations"]["data"][0]["rel_hum"])
    wind = int(jsonResponse["observations"]["data"][0]["wind_spd_kmh"])
    rain = float(jsonResponse["observations"]["data"][0]["rain_trace"])

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')

# 16x2 display
outL1 = f"{temp:2.1f}C      {rain:3.1f}mm" # this assumes no negative temperatures and less than 1000mm of rain in one day
outL2 = f"{appt:2.1f}c {hum:2d}% {wind:3d}kmh" # this assumes no negative apparent temperature, two digit humidity and max three digit wind speed

# Conversions to make the URL safe
outL1 = outL1.replace(" ", "+")
outL2 = outL2.replace(" ", "+")
outL2 = outL2.replace("%", "%25")

print(str(len(outL1)) + " " + str(len(outL2)) + " [" + outL1 + "] [" + outL2 + "]")
#print(f"[{temp:2.1f}C   {rain:3.1f}mm]")
#print(f"[{hum:2d}% {wind:3d}kmh      ]")

try:
    response = requests.get('http://192.168.1.111/?L1=' + outL1 + '&L2=' + outL2) # Edit this IP address to match your Arduino

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
