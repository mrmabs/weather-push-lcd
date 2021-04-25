import requests, time
from requests.exceptions import HTTPError

timer = 300 # sleep for timer seconds

while True:
    temp = 0.0
    appt = 0.0
    hum  = 0
    wind = 0
    rain = 0.0
    dewpt = 0.0

    try:
        response = requests.get('http://reg.bom.gov.au/fwo/IDQ60901/IDQ60901.94419.json')
        response.raise_for_status()
        # access JSOn content
        jsonResponse = response.json()
        #print("Entire JSON response")
        #print(jsonResponse)
        temp  = float(jsonResponse["observations"]["data"][0]["air_temp"])
        appt  = float(jsonResponse["observations"]["data"][0]["apparent_t"])
        hum   = int(jsonResponse["observations"]["data"][0]["rel_hum"])
        wind  = int(jsonResponse["observations"]["data"][0]["wind_spd_kmh"])
        rain  = float(jsonResponse["observations"]["data"][0]["rain_trace"])
        dewpt = float(jsonResponse["observations"]["data"][0]["dewpt"])

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    # 16x2 display
    outL1 = f"{temp:4.1f}C    {rain:5.1f}mm"
    outL2 = f"{appt:4.1f}c {dewpt:4.1f}d {wind:3d}k"

    print(str(len(outL1)) + " " + str(len(outL2)) + " [" + outL1 + "] [" + outL2 + "]")
    #print(f"[{temp:2.1f}C   {rain:3.1f}mm]")
    #print(f"[{hum:2d}% {wind:3d}kmh      ]")

    outL1 = outL1.replace(" ", "+")
    outL2 = outL2.replace(" ", "+")
    outL2 = outL2.replace("%", "%25")

    try:
        response = requests.get('http://10.33.20.101/?L1=' + outL1 + '&L2=' + outL2)

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

    time.sleep(timer)
