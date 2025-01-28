from func import *

class Airport:
    def __init__(self, icao, altitude, config, facility):
        self.icao = icao
        self.altitude = altitude
        self.config = config

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
        return(f"PSEUDOPILOT:{self.dep}_M_GND\n"
               f"@N{self.cs}:{self.sq.rjust(4,"0")}:1:{self.lat}:{self.long}:{self.alt}:0:{self.hdg}:0\n"
               f"$FP{self.cs}:*A:{self.rules}:{self.type}/L:420:{self.dep}:0000::{self.crz}:{self.dest}:00:00:0:0::/{self.rmk}/:{self.rte.strip()}\n"
               f"SIMDATA:{self.cs}:*:*:25.1.0.010\n"
               f"$ROUTE:{self.pseudo_route}\n"
               f"DELAY:1:2\n"
               f"REQALT::7000\n"
               f"INITIALPSEUDOPILOT:{self.dep}_M_GND\n\n")