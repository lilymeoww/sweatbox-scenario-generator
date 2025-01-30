import os
import string
import random
import json
# from dotenv import load_dotenv

# load_dotenv()

# print(os.environ["MAP_API_KEY"])


class Airport:
    """Represents an airport

    Attributes:
    -----------
    icao : str
        ICAO code of the airport
    altitude : int
        Integer representation of the altitude in feet
    config : str
        runway in use, e.g. 24
    facility : str
        The position of the student, e.g. GND for OBS -> S1
    """

    def __init__(self, icao: str, altitude: int, config: str, facility: str):
        self.icao = icao
        self.altitude = altitude
        self.config = config
        self.facility = facility


class Controller:
    """Represents a controller

    Attributes:
    -----------
    airport_icao : str
        ICAO code of the airport, e.g. EGPH
    facility : str
        Position of the Mentor, e.g. GND for OBS -> S1
    name : str
        Log-on callsign of the controller e.g. EGPH_TWR
    frequency : str
        Channel of the controller, e.g. 118.705
    """

    def __init__(self, airport_icao: str, facility: str, name: str, frequency: str):
        self.airport_icao = airport_icao
        self.facility = facility
        self.name = name  # TODO is this needed?
        self.frequency = frequency

    def __str__(self):
        return f"PSEUDOPILOT:{self.airport_icao}_M_{self.facility}\nCONTROLLER:{self.name}:{self.frequency}"


class Pilot:
    """Represents a Pilot

    Attributes:
    -----------
    cs : str
        Callsign of pilot, e.g. RYR100T
    lat : str
        Latitude of pilot in decimal degrees
    long : str
        Longitude of pilot in decimal degrees
    alt : str
        Altitude of pilot in feet
    hdg : str
        Heading of the pilot, encoded using `int(((hdg * 2.88) + 0.5)) << 2`
    dep : str
        Departure ICAO
    sq : str
        Aircraft squawk code
    rules : str
        I or V, for IFR, or VFR
    ac_type : str
        Pilot aircraft type ICAO, e.g. B738
    crz : str
        Cruise level in feet, e.g. 37000
    dest : str
        Destination ICAO
    rmk : str
        Flight-plan remarks
    rte : str
        Pilot's route
    pseudo_route : str
        Pseudo route for aircraft
    """

    def __init__(self, cs: str, lat: str, long: str, alt: str, hdg: str, dep: str, sq: str, rules: str, ac_type: str, crz: str, dest: str, rmk: str, rte: str, pseudo_route: str):
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


# class Stand:
#     """Represents a Stand at an airport

#     Attributes:
#     -----------
#     airport : str
#         ICAO code of the airport the stand is at
#     number : str
#         Identifier of the stand, e.g 5 or 45C
#     lat : str
#         Latitude of the stand
#     long : str
#         Longitude of the stand
#     heading : str
#         Heading of the stand between 0 and 359 degrees
#     """

#     def __init__(self, number, lat, long, heading):

#         # TODO: Moved to dictionary object. Class no longer required.

#     def __init__(self, airport: str, number: str, lat: str, long: str, heading: str):
#         self.airport = airport

#         self.number = number
#         self.lat = lat
#         self.long = long
#         self.heading = heading

#     def __repr__(self):
#         return f"Stand(number={self.number}, lat={self.lat}, long={self.long}, heading={self.heading})"


class Scenario:
    """Represents a sweatbox scenario

    Attributes:
    -----------
    airport : Airport
        The airport where the scenario takes place
    app_data : str
        Airport approach data
    controllers : list[Controller]
        List of controllers involved in the scenario
    pilots : list[Pilot]
        List of pilots involved in the scenario
    """

    def __init__(self, airport: Airport, app_data: str):
        self.airport = airport
        self.app_data = app_data
        self.controllers: list[Controller] = []
        self.pilots: list[Pilot] = []

    def add_controller(self, controller: Controller) -> None:
        """Adds a Controller to scenario file

        Args:
            controller (Controller): Controller to be added
        """
        self.controllers.append(controller)

    def add_pilot(self, pilot: Pilot) -> None:
        """Adds pilot to scenario file

        Args:
            pilot (Pilot): Pilot to be added
        """
        self.pilots.append(pilot)

    def generate_scenario(self) -> str:
        """Generates contents of scenario file

        Returns:
            str: string containing the contents of scenario file
        """
        scenario_file_str = f"PSEUDOPILOT:ALL\n\nAIRPORT_ALT:{
            self.airport.altitude}\n\n{self.app_data}\n\n"
        scenario_file_str += "".join(str(controller) +
                                     "\n" for controller in self.controllers)
        scenario_file_str += "\n".join(str(pilot) for pilot in self.pilots)
        return scenario_file_str


def generateSweatboxText(airport: Airport, app_data: str, vfrP: int, invalidRouteP: int, invalidLevelP: int, fplanErrorsP: int, controllers: list[Controller], autoPilots: int, manualPilots: list[Pilot]) -> str:
    """Generates pilots and controllers, adds them to a scenario and generates the resulting text

    Args:
        airport (Airport): Airport the sweatbox is based at
        app_data (str): Approach data for the airport
        vfrP (int): Percentage of VFR aircraft
        invalidRouteP (int): Percentage of aircraft with invalid routes
        invalidLevelP (int): Percentage of aircraft with invalid levels
        fplanErrorsP (int): Percentage of general flightplan errors
        controllers (list[Controller]): List of controllers
        autoPilots (int): Number of pilots to generate automatically
        manualPilots (list[Pilot]): List of manual pilots to add

    Returns:
        str: Returns string of scenario
    """
    scenario = Scenario(airport, app_data)

    for controller in controllers:
        scenario.add_controller(controller)

    pilots = generate_random_plans(autoPilots, airport, vfrP,
                                   invalidRouteP, invalidLevelP, fplanErrorsP)
    for pilot in pilots:
        scenario.add_pilot(pilot)

    for pilot in manualPilots:
        scenario.add_pilot(pilot)

    return scenario.generate_scenario()


def generate_random_plans(amount: int, dep: Airport, vfr_factor: int, incorrect_factor: int, level_factor: int, entry_error_factor: int) -> list[Pilot]:
    """Generates a given number of VFR and IFR flightplans

    Args:
        amount (int): Total number of flightplans
        dep (Airport): Airport Scenario is based at
        vfr_factor (int): Percentage of VFR aircraft
        incorrect_factor (int): Percentage of incorrect routes
        level_factor (int): Percentage of incorrect levels
        entry_error_factor (int): Percentage of general flightplan errors 

    Returns:
        list[Pilot]: Returns a list of pilots with the required settings
    """
    numberOfVfr = int(amount * vfr_factor/100)

    standsUsed = set()
    vfrCallsignsUsed = set()
    pilots = []

    with open("rsc/stands.json") as jsonData:
        temp = json.load(jsonData)
        stands = temp.get(dep.icao)

    with open("rsc/callsignsVFR.json") as jsonData:
        temp = json.load(jsonData)
    callsigns = temp.get("callsigns")

    current_sq = 0
    for _ in range(numberOfVfr):
        current_sq += 1
        # callsigns = callsigns - vfrCallsignsUsed
        # stands = stands - standsUsed
        cs = random.choice(list(callsigns))
        callsigns.pop(cs, None)
        # vfrCallsignsUsed.add(cs)
        rules = "V"
        dest = random.choice(
            ["EGPF", "EGPB", "EGNX", "EGPC", "EGAA", "EGPH", "EGLK", "EGLF", "EGMA", "EGFF"])
        ac_type = random.choice(["P28A", "C172", "C152", "DA42", "SR22"])
        stand = random.choice(list(stands))
        print(stand)
        selectedStand = stands.get(stand)
        stands.pop(stand)
        lat, long, hdg = selectedStand.split(",")[0], selectedStand.split(
            ",")[1], int(((int(selectedStand.split(",")[2]) * 2.88) + 0.5)) << 2
        sq = sq = f"{current_sq:04}"
        crz = (500 * random.randint(1, 3)) + 1000
        rmk = "v"
        rte = "VFR"
        pilots.append(Pilot(cs, lat, long, dep.altitude, hdg,
                      dep.icao, sq, rules, ac_type, crz, dest, rmk, rte, ""))

    with open("rsc/callsignsIFR.json") as jsonData:
        temp = json.load(jsonData)
    callsigns = temp.get("callsigns")

    with open("aircrafttypes.txt", "r")as f:
        types = f.read().splitlines()

    for _ in range(amount - numberOfVfr):
        current_sq += 1
        sq = f"{current_sq:04}"
        depAirport = dep.icao

        # stands = stands - standsUsed
        chosenCallsign = random.choice(list(callsigns))
        cs = chosenCallsign + str(random.randint(10, 99)) + random.choice(
            string.ascii_uppercase) + random.choice(string.ascii_uppercase)
        rules = "I"
        possDest = callsigns[chosenCallsign].split(",")
        dest = random.choice(possDest)

        for type_ in types:
            if type_.split(",")[0] == chosenCallsign:
                ac_type = random.choice(type_.split(",")[1:])
                break
        else:
            ac_type = "UNKNOWN"

        stand = random.choice(list(stands))
        selectedStand = stands.get(stand)
        stands.pop(stand)
        lat, long, hdg = selectedStand.split(",")[0], selectedStand.split(
            ",")[1], int(((int(selectedStand.split(",")[2]) * 2.88) + 0.5)) << 2
        standsUsed.add(stand)  # TODO: Remove.
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


def get_route(departure: str, arrival: str, incorrect_factor: int) -> tuple[str, str]:
    """Gets a route between 2 airports, with a chance of the route being invalid

    Args:
        departure (str): Departure ICAO 
        arrival (str): Arrival ICAO
        incorrect_factor (int): Percentage of incorrect routes

    Returns:
        tuple[str, str]: Returns the route and the cruise level
    """
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
