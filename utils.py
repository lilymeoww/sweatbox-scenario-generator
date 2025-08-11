import string
import random
import json
import sys
import os


def resourcePath(relativePath: str) -> str:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        basePath = sys._MEIPASS
    except Exception as e:
        basePath = os.environ.get("_MEIPASS2", os.path.abspath("."))

    return os.path.join(basePath, relativePath)


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

    def __init__(self, cs: str, lat: str, long: str, alt: str, hdg: str, dep: str, sq: str, rules: str, ac_type: str, crz: str, dest: str, rmk: str, rte: str, pseudo_route: str, speed: str = "420", timeUntilSpawn: str = "0", levelByFix: str = '', levelByLevel: str = "3000",owner: str = None):
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
        self.speed = speed
        self.timeUntilSpawn = timeUntilSpawn
        self.levelByFix = levelByFix
        self.levelByLevel = levelByLevel
        if not owner:
            self.owner = self.dep
        else:
            self.owner = owner


    def __str__(self):
        return (f"\nPSEUDOPILOT:{self.owner}_M_GND\n"
                f"@N:{self.cs}:{self.sq.rjust(4, '0')}:1:{self.lat}:{self.long}:{
            self.alt}:0:{self.hdg}:0\n"
            f"$FP{self.cs}:*A:{self.rules}:{self.ac_type}:{self.speed}:{self.dep}:0000::{
                    self.crz}:{self.dest.strip()}:00:00:0:0::/{self.rmk}/:{self.rte.strip()}\n"
            f"SIMDATA:{self.cs}:*:*:25.1.0.000\n"
            f"$ROUTE:{self.pseudo_route}\n"
            f"START:{self.timeUntilSpawn}\n"
            f"DELAY:1:2\n"  # TODO - do mentors want this?
            f"REQALT:{self.levelByFix}:{self.levelByLevel}\n"  # Level by???
            f"INITIALPSEUDOPILOT:{self.owner}_M_GND")


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


def generateSweatboxText(airport: Airport, app_data: str, vfrP: int, invalidRouteP: int, invalidLevelP: int, fplanErrorsP: int, controllers: list[Controller], autoPilots: int, manualPilots: list[Pilot], arrivalOffsets: list[str], occupiedStands) -> str:
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
        arrivalOffsets (list[str]): List of offsets for arrival spawning (in minutes)

    Returns:
        str: Returns string of scenario
    """
    scenario = Scenario(airport, app_data)

    for controller in controllers:
        scenario.add_controller(controller)

    pilots, occupiedStands = generate_random_plans(autoPilots, airport, vfrP,
                                   invalidRouteP, invalidLevelP, fplanErrorsP, occupiedStands)
    pilots += generate_arrival_plans(airport, arrivalOffsets)
    for pilot in pilots:
        scenario.add_pilot(pilot)

    for pilot in manualPilots:
        scenario.add_pilot(pilot)

    return scenario.generate_scenario(), occupiedStands


def generate_arrival_plans(arrival: Airport, offsets: list[str]) -> list[Pilot]:
    pilots = []
    with open(resourcePath("rsc/callsignsIFR.json")) as jsonData:
        JSONInjest = json.load(jsonData)
    callsigns = JSONInjest.get("callsigns")

    with open(resourcePath("rsc/aircraftTypes.json")) as jsonData:
        JSONInjest = json.load(jsonData)
    types = JSONInjest.get("callsigns")

    with open(resourcePath("rsc/arrivalRoutes.json"))as jsonData:
        arrivalRoutes = json.load(jsonData)

    for offset in offsets:
        chosenCallsign = random.choice(list(callsigns))
        cs = chosenCallsign + str(random.randint(10, 99)) + random.choice(
            string.ascii_uppercase) + random.choice(string.ascii_uppercase)
        actype = random.choice((types[chosenCallsign].split(",")))
        print(f"SYSTEM: ARRIVAL {actype=}")
        rules = "I"
        lat = 55.717191666667  # TODO change from TARTN
        long = -3.1385361111111
        alt = 7000
        heading = int(((22 * 2.88) + 0.5)) << 2
        dep = "EGLL"
        sq = "0000"
        cruiseLevel = "38000"
        dest = arrival.icao
        rmk = "v"
        route = "ULTIB T420 TNT UN57 POL UN601 INPIP"
        pseudoRoute = f"{" ".join(arrivalRoutes[arrival.icao])} CF24 ILS24"
        levelByFix = "CF24"
        levelAtFix = "2500"

        pilot = Pilot(cs, lat, long, alt, heading, dep, sq,
                      rules, actype, cruiseLevel, dest, rmk, route, pseudoRoute, "180", offset, levelByFix, levelAtFix,owner="EGPH")
        pilots.append(pilot)

    return pilots


def generate_random_plans(amount: int, dep: Airport, vfr_factor: int, incorrect_factor: int, level_factor: int, entry_error_factor: int, occupiedStands) -> list[Pilot]:
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

    pilots = []

    stands = loadStand(dep.icao)

    if(dep.icao == "EGLL"):
        with open(resourcePath("rsc/heathrowTerminals.json")) as terminalData:
            heathrowTerminals = json.load(terminalData)

    for entry in occupiedStands:
        if entry in stands:
            blockingData = stands[entry]["blocks"]
            stands.pop(entry)
            print(f"SYSTEM: STAND {entry} REMOVED")
            for block in blockingData:
                if block in stands:
                    stands.pop(block)
                    print(f"SYSTEM: STAND {block} REMOVED")

    with open(resourcePath("rsc/callsignsVFR.json")) as jsonData:
        JSONInjest = json.load(jsonData)
    callsigns = JSONInjest.get("callsigns")

    with open(resourcePath("rsc/vfrDestinations.json")) as jsonData:
        JSONInjest = json.load(jsonData)
    possDest = JSONInjest.get(dep.icao)

    current_sq = 0
    for _ in range(numberOfVfr):
        current_sq += 1
        cs = random.choice(list(callsigns))
        rules = "V"
        dest = random.choice(possDest)
        ac_type = random.choice(callsigns[cs].split(","))
        callsigns.pop(cs, None)

        if(callsigns == {}):
            print(f"SYSTEM: NO MORE CALLSIGNS AVAILABLE | {current_sq} AIRCRAFT GENERATED")
            break

        stand = random.choice(list(stands))
        print(f"SYSTEM: VFR {cs} ASSIGNED TO STAND {stand}")
        selectedStand = stands.get(stand)
        occupiedStands.append(stand)
        stands.pop(stand)

        lat, long, hdg, block = selectedStand["lat"], selectedStand["long"], int(
            ((int(selectedStand["hdg"]) * 2.88) + 0.5)) << 2, selectedStand["blocks"]
        for standToRemove in block:
            if standToRemove in stands:
                stands.pop(standToRemove)

            print(f"SYSTEM: STAND {standToRemove} REMOVED")

        sq = sq = f"{current_sq:04}"
        crz = (500 * random.randint(1, 3)) + 1000
        rmk = "v"
        rte = "VFR"
        pilots.append(Pilot(cs, lat, long, dep.altitude, hdg,
                      dep.icao, sq, rules, ac_type, crz, dest, rmk, rte, ""))

    with open(resourcePath("rsc/callsignsIFR.json")) as jsonData:
        JSONInjest = json.load(jsonData)
    if(dep.icao == "EGLL"):
        callsigns = JSONInjest.get("EGLL")
    else:
        callsigns = JSONInjest.get("callsigns")

    with open(resourcePath("rsc/aircraftTypes.json")) as jsonData:
        JSONInjest = json.load(jsonData)
    types = JSONInjest.get("callsigns")

    if(dep.icao == "EGLL"):
        terminalStands = loadHeathrowTerminals(dep.icao)

    for _ in range(amount - numberOfVfr):

        current_sq += 1
        sq = f"{current_sq:04}"
        depAirport = dep.icao

        dest, rte, crz = get_route(depAirport, incorrect_factor)

        chosenCallsign, cs, rules = selectAirline(dest, callsigns)

        possTypes = types[chosenCallsign].split(",")
        acType = random.choice(possTypes)

        if(dep.icao == "EGLL"):
            terminal = findTerminal(heathrowTerminals, chosenCallsign)
            while True:
                if terminalStands[terminal] != {}:
                    stand = random.choice(list(terminalStands[terminal]))
                    for standToRemove in terminalStands[terminal][stand]["blocks"]:
                        if standToRemove in terminalStands[terminal]:
                            terminalStands[terminal].pop(standToRemove)
                            stands.pop(standToRemove)
                            print(f"SYSTEM: STAND {standToRemove} REMOVED")
                    terminalStands[terminal].pop(stand)
                    break
                else:
                    print(f"SYSTEM: NO MORE STANDS AVAILABLE FOR TERMINAL {terminal} | REGENERATING")
                    dest, rte, crz = get_route(depAirport, incorrect_factor)
                    chosenCallsign, cs, rules = selectAirline(dest, callsigns)
                    terminal = findTerminal(heathrowTerminals, chosenCallsign)
                    possTypes = types[chosenCallsign].split(",")
                    acType = random.choice(possTypes)
        else:
            stand = random.choice(list(stands))
        print(f"SYSTEM: IFR {cs} ASSIGNED TO STAND {stand}")

        selectedStand = stands.get(stand)
        occupiedStands.append(stand)
        stands.pop(stand)
        if(stands != {}):
            for standToRemove in selectedStand["blocks"]:
                if standToRemove in stands:
                    stands.pop(standToRemove)
                print(f"SYSTEM: STAND {standToRemove} REMOVED")
        else:
            print(f"SYSTEM: NO MORE STANDS AVAILABLE | {current_sq-1} AIRCRAFT GENERATED")
            return pilots, occupiedStands

        lat, long, hdg = selectedStand["lat"], selectedStand["long"], (
            int((int(selectedStand["hdg"]) * 2.88) + 0.5)) << 2
        rmk = "v"

        if random.randint(1, 100) <= level_factor:

            with open(resourcePath("rsc/invalidAltitudes.json")) as jsonData:
                JSONInjest = json.load(jsonData)
            alts = JSONInjest.get(dep.icao)
            crz = alts.get(dest)

        if random.randint(1, 100) <= entry_error_factor:
            entry_error_options = ["type", "dep"]
            chosen_error = random.choice(entry_error_options)
            if chosen_error == "type":

                with open(resourcePath("rsc/errorTypes.json")) as jsonData:
                    JSONInjest = json.load(jsonData)
                possTypes = JSONInjest.get("types")
                acType = possTypes.get(acType)
            elif chosen_error == "dep":
                with open(resourcePath("rsc/adepError.json")) as jsonData:
                    JSONInjest = json.load(jsonData)
                possAirports = JSONInjest.get(depAirport)
                depAirport = random.choice(possAirports).split(",")

        pilots.append(Pilot(cs, lat, long, dep.altitude, hdg,
                            depAirport, sq, rules, acType, crz, dest, rmk, rte, ""))

    return pilots, occupiedStands


def get_route(departure: str, incorrect_factor: int) -> tuple[str, str]:
    """Gets a route between 2 airports, with a chance of the route being invalid

    Args:
        departure (str): Departure ICAO 
        arrival (str): Arrival ICAO
        incorrect_factor (int): Percentage of incorrect routes

    Returns:
        tuple[str, str, str]: Returns the destination, route and cruise level
    """
    try:

        if random.randint(1, 100) <= incorrect_factor:
            with open(resourcePath("rsc/invalidRoutes.json")) as jsonData:
                JSONInjest = json.load(jsonData)
            routes = JSONInjest.get(departure)
            
            desitnation, route = random.choice(list(routes.items()))
            print(random.choice(list(route)))
            route = random.choice(list(route)).split(",")

        else:
            with open(resourcePath("rsc/routes.json")) as jsonData:
                JSONInjest = json.load(jsonData)
            routes = JSONInjest.get(departure)
            
            desitnation, route = random.choice(list(routes.items()))
            route = route.split(",")

        return desitnation, route[0], route[1]

    except FileNotFoundError:
        print("ERROR : file not found.")
    return f"{departure}", "E"


def selectAirline(dest: str, callsigns: dict) -> tuple[str, str, str]:
    """Selects an apropreate airline based on the destination
    
    Args:
        dest (str): Destination ICAO
        callsigns (dict): Dictionary of callsigns & destinations

    Returns:
        tuple[str, str, str]: Returns the chosen callsign, generated callsign and flight rules
    """
    airlines = []
    for airline, destinations in callsigns.items():
        if dest in destinations.split(","):
            airlines.append(airline)

    chosenCallsign = random.choice(list(airlines))
    cs = chosenCallsign + str(random.randint(11, 99)) + random.choice(
        string.ascii_uppercase) + random.choice(string.ascii_uppercase)
    rules = "I"
            
    return chosenCallsign, cs, rules


def loadHeathrowTerminals(icao) -> dict:
    #with open(resourcePath("rsc/heathrowTerminals.json")) as jsonData:
        #JSONInjest = json.load(jsonData)
    allStands = loadStand(icao)
    terminalStands = {}
    for stand_num, stand_data in allStands.items():
        if stand_num[0] not in terminalStands:
            terminalStands[stand_num[0]] = {}
        terminalStands[stand_num[0]][stand_num] = stand_data
    return terminalStands


def findTerminal(terminals: dict, airline: str) -> str:
    """Finds the terminal for a given airline at EGLL
    
    Args:
        terminals (dict): Dictionary of terminals and airlines
        airline (str): Airline being searched for

    Returns:
        str: Returns the terminal number
    """
    for parent, children in terminals.items():
        if airline in children:
            return parent
        

def loadStand(icao: str) -> dict:
    """Loads the stand information for a given airport

    Args:
        airport (Airport): The airport object containing the ICAO code

    Returns:
        dict: Dictionary of stand information for the airport
    """
    with open(resourcePath("rsc/stands.json")) as jsonData:
        JSONInjest = json.load(jsonData)
    return JSONInjest.get(icao)


def loadStandNums(icao: str) -> list:
    """Loads the stand numbers for a given airport

    Args:
        airport (Airport): The airport object containing the ICAO code

    Returns:
        list: List of stand numbers for the airport
    """
    stands = loadStand(icao.icao)

    standNums = []
    counter = 0
    for stand in stands:
        standNums.append(stand)
        counter += 1
    
    return standNums, stands


if __name__ == "__main__":
    ...
