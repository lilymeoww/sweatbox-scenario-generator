import json
import random

with open("callsignsIFR.json") as configData:
        callsign = json.load(configData)

test = callsign.get("callsigns")

randomAirline = random.choice(list(test))

#selectedAirline = test.get(randomAirline)

airport_list = test[randomAirline].split(",")
randomAirport = random.choice(airport_list)

print(randomAirline)
print(test.get(randomAirline))
print(len(airport_list))