from func import *

airport_alt = 136.0
airport_icao = "EGPH"
config = "24"
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
        aircraft_departure = airport_icao
        aircraft_squawk = str(oct(current_sq))[2:]
        aircraft_rules = input("Enter a/c flight rules (I/V)").upper()
        aircraft_type = input("Enter a/c type (as displayed in flight plan): ")
        aircraft_cruise_fl = input("Enter cruise fl as an altitude (i.e. 33000): ")
        aircraft_destination = input("Enter aircraft destination airport: ")
        aircraft_rmk = input("Enter voice rules of a/c (v, r, t, or empty): ")
        aircraft_route = str(get_route(airport_icao, aircraft_destination))
        pseudoplane_route = f"{get_dep_for_route(airport_icao,aircraft_route.split()[1],config)} {aircraft_route.split()[2]} {aircraft_route.split()[3]}"


        pilot_list += (f"PSEUDOPILOT:{airport_icao}_M_{facility}\n@N:{aircraft_cs}:{aircraft_squawk.rjust(4,"0")}:1:{aircraft_latitude}:{aircraft_longitude}:{aircraft_altitude}:0:{aircraft_heading}:0:\n"
                       f"$FP{aircraft_cs}:*A:{aircraft_rules}:{aircraft_type}/L:420:{airport_icao}:0000::{aircraft_cruise_fl}:{aircraft_destination}:00:00:0::/{aircraft_rmk}/:{aircraft_route}\n"
                       f"SIMDATA:{aircraft_cs}:*:*:25:1:0.010\n"
                       f"$ROUTE:{pseudoplane_route}\n"
                       f"DELAY:1:2\n"
                       f"REQALT::7000\n"
                       f"INITALPSEUDOPILOT:{airport_icao}_M_{facility}\n\n")
    else:
        add_more_pilots = False
        scenario_file_str += f"\n\n{pilot_list}"

print(scenario_file_str)

