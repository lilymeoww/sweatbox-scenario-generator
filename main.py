airport_alt = 136.0
airport_icao = "EGPH"
facility = "GND"
airport_app_data = "ILS24:55.9560884:-3.3546135:55.9438540:-3.3907010\nILS06:55.9437922:-3.3908724:55.9561296:-3.3544421\nILS:55.9513586:-3.3594437:118.0\nILS:55.9436373:-3.3341400:298.0"

scenario_file_str = f"PSEUDOPILOT:ALL\n\nAIRPORT_ALT:{airport_alt}\n\n{airport_app_data}\n\n"

add_more_controllers = True
controller_list = ""
while add_more_controllers:
    if input("add more controllers? (y/n)").lower() == "y":
        controller_list += f"PSEUDOPILOT:{airport_icao}_M_{facility}\nCONTROLLER:{input('enter controller¬ ').upper().strip()}:{input('enter controller freq¬ ').upper().strip()}"
    else:
        add_more_controllers = False
        scenario_file_str += controller_list

add_more_pilots = True
pilot_list = ""
current_sq = 0
while add_more_pilots:
    if input("add more plen? (y/n)").lower() == "y":
        current_sq += 1
        aircraft_cs = input("Enter c/s: ")
        aircraft_latitude = input("Enter latitude of a/c: ")
        aircraft_longitude = input("Enter longitude of a/c: ")
        aircraft_altitude = int(airport_alt)
        aircraft_heading = int(input("Enter a/c heading: ")) % 360
        aircraft_heading = int(((aircraft_heading * 2.88) + 0.5)) << 2
        print(aircraft_heading)
        aircraft_departure = {airport_icao}
        aircraft_squawk = {oct(current_sq)}

        pilot_list += f"PSEUDOPILOT:{airport_icao}_M_{facility}\n@N:{aircraft_cs}:{aircraft_squawk:04}:1:{aircraft_latitude}:{aircraft_longitude}:{aircraft_altitude}:0:{aircraft_heading}:0:"
    else:
        add_more_pilots = False
        scenario_file_str += f"\n\n{pilot_list}"

print(scenario_file_str)

