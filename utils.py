import os
import string
import random
from dotenv import load_dotenv

# load_dotenv()

# print(os.environ["MAP_API_KEY"])


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
    def __init__(self, cs, lat, long, alt, hdg, dep, sq, rules, ac_type, crz, dest, rmk, rte, pseudo_route):
        self.cs = cs
        self.lat = lat
        self.long = long
        self.alt = alt
        self.hdg = hdg
        self.dep = dep
        self.sq = sq
        self.rules = rules
        self.ac_type = ac_type
        self.crz = crz
        self.dest = dest
        self.rmk = rmk
        self.rte = rte
        self.pseudo_route = pseudo_route

    def __str__(self):
        return (f"\nPSEUDOPILOT:{self.dep}_M_GND\n"
                f"@N:{self.cs}:{self.sq.rjust(4, '0')}:1:{self.lat}:{self.long}:{
            self.alt}:0:{self.hdg}:0\n"
            f"$FP{self.cs}:*A:{self.rules}:{self.ac_type}:420:{self.dep}:0000::{
                    self.crz}:{self.dest.strip()}:00:00:0:0::/{self.rmk}/:{self.rte.strip()}\n"
            f"SIMDATA:{self.cs}:*:*:25.1.0.000\n"
            f"$ROUTE:{self.pseudo_route}\n"
            f"DELAY:1:2\n"
            f"REQALT::7000\n"
            f"INITIALPSEUDOPILOT:{self.dep}_M_GND")


class Stand:
    def __init__(self, airport, number, lat, long, heading):
        self.airport = airport
        self.number = number
        self.lat = lat
        self.long = long
        self.heading = heading


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
        scenario_file_str = f"PSEUDOPILOT:ALL\n\nAIRPORT_ALT:{
            self.airport.altitude}\n\n{self.app_data}\n\n"
        scenario_file_str += "".join(str(controller) +
                                     "\n" for controller in self.controllers)
        scenario_file_str += "\n".join(str(pilot) for pilot in self.pilots)
        return scenario_file_str


def generateSweatboxText(airport: Airport, app_data: str, vfrP: int, invalidRouteP: int, invalidLevelP: int, fplanErrorsP: int, controllers: list[tuple[str, str]], autoPilots: int, manualPilots: list[Pilot]) -> str:
    app_data = """ILS24:55.9560884:-3.3546135:55.9438540:-3.3907010
    ILS06:55.9437922:-3.3908724:55.9561296:-3.3544421
    ILS:55.9513586:-3.3594437:118.0
    ILS:55.9436373:-3.3341400:298.0"""  # TODO get this from somewhere nice?? also what is this data :o
    scenario = Scenario(airport, app_data)

    for controller, frequency in controllers:
        facility = controller.split("_")[-1]
        scenario.add_controller(Controller(
            airport.icao, facility, controller, frequency))

    current_sq = len(manualPilots)
    pilots = generate_random_plans(autoPilots, airport, vfrP,
                                   invalidRouteP, invalidLevelP, fplanErrorsP)
    for pilot in pilots:
        scenario.add_pilot(pilot)

    for pilot in manualPilots:
        scenario.add_pilot(pilot)

    return scenario.generate_scenario()


def generate_random_plans(amount: int, dep: Airport, vfr_factor: int, incorrect_factor: int, level_factor: int, entry_error_factor: int) -> list[Pilot]:
    numberOfVfr = int(amount * vfr_factor/100)

    standsUsed = set()
    vfrCallsignsUsed = set()
    pilots = []

    with open("callsignsVFR.txt", "r")as f:
        callsigns = {data.split(",")[0] for data in f.read().splitlines()}

    with open("stands.txt", "r")as f:
        stands = {Stand(data.split(",")[0], data.split(",")[1], data.split(",")[2],
                        data.split(",")[3], data.split(",")[4]) for data in f.read().splitlines()}
    current_sq = 0
    for _ in range(numberOfVfr):
        current_sq += 1
        callsigns = callsigns - vfrCallsignsUsed
        stands = stands - standsUsed
        cs = random.choice(list(callsigns))
        vfrCallsignsUsed.add(cs)
        rules = "V"
        dest = random.choice(
            ["EGPF", "EGPB", "EGNX", "EGPC", "EGAA", "EGPH", "EGLK", "EGLF", "EGMA", "EGFF"])
        ac_type = random.choice(["P28A", "C172", "C152", "DA42", "SR22"])
        stand = random.choice(list(stands))
        standsUsed.add(stand)
        lat = stand.lat
        long = stand.long
        hdg = int(((int(stand.heading) * 2.88) + 0.5)) << 2
        sq = sq = f"{current_sq:04}"
        crz = (500 * random.randint(1, 3)) + 1000
        rmk = "v"
        rte = "VFR"
        pilots.append(Pilot(cs, lat, long, dep.altitude, hdg,
                      dep.icao, sq, rules, ac_type, crz, dest, rmk, rte, ""))

    with open("callsignsIFR.txt", "r")as f:
        callsigns = [d.split(",") for d in f.read().splitlines()]

    with open("aircrafttypes.txt", "r")as f:
        types = f.read().splitlines()

    for _ in range(amount - numberOfVfr):
        current_sq += 1
        sq = sq = f"{current_sq:04}"
        depAirport = dep.icao

        stands = stands - standsUsed
        chosenCallsign = random.choice(callsigns)
        cs = chosenCallsign[0] + str(random.randint(10, 99)) + random.choice(
            string.ascii_uppercase) + random.choice(string.ascii_uppercase)
        rules = "I"
        dest = random.choice(chosenCallsign[1:])

        for type_ in types:
            if type_.split(",")[0] == chosenCallsign[0]:
                ac_type = random.choice(type_.split(",")[1:])
                break
        else:
            ac_type = "UNKNOWN"

        stand = random.choice(list(stands))
        standsUsed.add(stand)
        lat = stand.lat
        long = stand.long
        hdg = int(((int(stand.heading) * 2.88) + 0.5)) << 2
        rmk = "v"
        rte, crz = get_route(dep.icao, dest, incorrect_factor)
        if random.randint(1, 100) <= level_factor:
            with open("invalidAltitudes.txt", "r") as file:
                invalidAlts = file.readlines()
                found = False
                for alt in invalidAlts:
                    if not found and alt.split(",")[0] == dep and alt.split(",")[1] == dest:
                        crz = alt.split(",")[2].strip()
                        found = True

        if random.randint(1, 100) <= entry_error_factor:
            entry_error_options = ["type", "dep"]
            chosen_error = random.choice(entry_error_options)
            if chosen_error == "type":
                with open("errorTypes.txt", "r") as file:
                    bad_types = file.readlines()
                    new_type = ac_type  # Initialize new_type with the original ac_type
                    for bad_type in bad_types:
                        if bad_type.split(",")[0] == ac_type:
                            new_type = bad_type.split(",")[1].strip()
                            break  # Exit the loop once a match is found
                ac_type = new_type
            elif chosen_error == "dep":
                with open("adepError.txt", "r") as f:
                    lines = f.readlines()
                    depAirport = random.choice(lines).strip()

        pilots.append(Pilot(cs, lat, long, dep.altitude, hdg,
                            depAirport, sq, rules, ac_type, crz, dest, rmk, rte, ""))

    return pilots


def get_route(departure, arrival, incorrect_factor: int):
    try:

        if random.randint(1, 100) <= incorrect_factor:
            with open("invalidRoutes.txt", "r") as file:
                poss_routes = []
                routes = file.readlines()
        else:
            with open("routes.txt", "r") as file:
                poss_routes = []
                routes = file.readlines()

        for route in routes:
            route_str = route.split(",")[0]

            if route_str.split(" ")[0].strip() == departure and route_str.split(" ")[-1].strip() == arrival:
                # print(f"Route found: {route.split(',')[1].strip()}")
                poss_routes.append(
                    [route_str.replace("\n", ""), route.split(",")[1].strip()])
                # print(poss_routes)
        route_chosen = random.choice(poss_routes)
        return route_chosen[0], route_chosen[1]

    except FileNotFoundError:
        print("Error: routes.txt file not found.")
    return f"{departure} {arrival}", "E"




# def validate_stand(dep):
#     while True:
#         user_stand = input("Enter stand number: ").upper()
#         try:
#             with open("stands.txt", "r") as standfile:
#                 stands = standfile.readlines()
#                 for stand in stands:
#                     stand = stand.split(",")
#                     if stand[0] == dep and stand[1] == user_stand:
#                         return stand[2], stand[3], stand[4].strip()
#             print("Please enter a valid stand number.")
#         except FileNotFoundError:
#             print("Error: stands.txt file not found.")
#             break


if __name__ == "__main__":
    ...
