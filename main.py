from func import *

class Airport:
    def __init__(self, icao, altitude, config, facility):
        self.icao = icao
        self.altitude = altitude
        self.config = config
        self.facility = facility

class Controller:
    def __init__(self, airport_icao, facility, name, frequency):
        self.airport_icao = airport_icao
        self.facility = facility
        self.name = name
        self.frequency = frequency

    def __str__(self):
        return f"PSEUDOPILOT:{self.airport_icao}_M_{self.facility}\nCONTROLLER:{self.name}:{self.frequency}"

class Pilot:
    def __init__(self, cs, lat, long, alt, hdg, dep, sq, rules, type, crz, dest, rmk, rte, pseudo_route):
        self.cs = cs
        self.lat = lat
        self.long = long
        self.alt = alt
        self.hdg = hdg
        self.dep = dep
        self.sq = sq
        self.rules = rules
        self.type = type
        self.crz = crz
        self.dest = dest
        self.rmk = rmk
        self.rte = rte
        self.pseudo_route = pseudo_route

    def __str__(self):
        return(f"\n\nPSEUDOPILOT:{self.dep}_M_GND\n"
               f"@N:{self.cs}:{self.sq.rjust(4,"0")}:1:{self.lat}:{self.long}:{self.alt}:0:{self.hdg}:0\n"
               f"$FP{self.cs}:*A:{self.rules}:{self.type}/L:420:{self.dep}:0000::{self.crz}:{self.dest}:00:00:0:0::/{self.rmk}/:{self.rte.strip()}\n"
               f"SIMDATA:{self.cs}:*:*:25.1.0.010\n"
               f"$ROUTE:{self.pseudo_route}\n"
               f"DELAY:1:2\n"
               f"REQALT::7000\n"
               f"INITIALPSEUDOPILOT:{self.dep}_M_GND\n\n")

class Scenario:
    def __init__(self, airport, app_data):
        self.airport = airport
        self.app_data = app_data
        self.controllers = []
        self.pilots = []

    def add_controller(self, controller):
        self.controllers.append(controller)

    def add_pilot(self, pilot):
        self.pilots.append(pilot)

    def generate_scenario(self):
        scenerio_file_str = f"PSEUDOPILOT:ALL\n\nAIRPORT_ALT:{self.airport.altitude}\n\n{self.app_data}\n\n"
        scenerio_file_str += "".join(str(controller) for controller in self.controllers)
        scenerio_file_str += "\n\n".join(str(pilot) for pilot in self.pilots)
        return scenerio_file_str

if __name__ == "__main__":
    airport = Airport("EGPH", 136, "24", "GND")
    app_data = """ILS24:55.9560884:-3.3546135:55.9438540:-3.3907010
ILS06:55.9437922:-3.3908724:55.9561296:-3.3544421
ILS:55.9513586:-3.3594437:118.0
ILS:55.9436373:-3.3341400:298.0"""
    scenario = Scenario(airport, app_data)

    while input("Add more controllers? (y/n): ").lower() == "y":
        name = input("Enter controller callsign: ").upper().strip()
        freq = input("Enter controller freq: ").strip()
        controller = Controller(airport.icao, "GND", name, freq)
        scenario.add_controller(controller)

    current_sq = 0
    while input("Add more pilots? (y/n): ").lower() == "y":
        current_sq += 1
        cs = input("Enter c/s: ")
        lat = input("Enter latitude: ")
        long = input("Enter longitude: ")
        alt = int(airport.altitude)
        hdg = int(input("Enter a/c heading: ")) % 360
        hdg = int(((hdg * 2.88) + 0.5)) << 2
        dep = airport.icao
        sq = str(oct(current_sq))[2:]
        rules = input("Enter a/c flight rules (I/V): ").upper()
        ac_type = input("Enter a/c type as displayed on fpln: ")
        cruise_fl = input("Enter cruise level as altitude: ")
        dest = input("Enter aircraft destination airport: ")
        rmk = input("Enter voice rules (v, r, t, or empty): ")
        route = str(get_route(dep, dest))
        pseudo_route = f"{get_dep_for_route(dep, route.split()[1], airport.config)}"
        pilot = Pilot(cs, lat, long, alt, hdg, dep, sq, rules, ac_type, cruise_fl, dest, rmk, route, pseudo_route)
        scenario.add_pilot(pilot)

    print(scenario.generate_scenario())