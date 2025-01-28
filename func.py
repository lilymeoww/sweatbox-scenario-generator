import random

def get_route(departure, arrival):
    with open("routes.txt", "r") as file:
        routes = file.readlines()
        for route in routes:
            route_comp = route.strip().split()
            if route_comp[0] == departure and route_comp[-1] == arrival:
                return route
        return f"{departure} DIRECT {arrival}"

def get_dep_for_route(departure, first_wp, config):
    with open("departure_routes.txt", "r") as file:
        routes = file.readlines()
        for route in routes:
            route_comp = route.strip().split(",")
            if route_comp[0] == departure and route_comp[1] == config and route_comp[2] == first_wp:
                return route_comp[3]
        return first_wp

def generate_random_pilot(airport):
    if random.randint(1,10) <= 20:
        with open("callsignsVFR.txt", "r") as file:
            callsigns = file.readlines()
            chosen_callsign = random.choice(callsigns).split(",")
            cs = chosen_callsign[0]
            rules = "V"
            dest = random.choice(chosen_callsign[0:])
            with open("aircrafttypes.txt", "r") as typefile:
                type = random.choice(typefile.readline().split(","))
            user_stand = input("Enter stand number: ").upper()
            with open("stands.txt", "r") as standfile:
                stands = standfile.readlines()
                for stand in stands:
                    stand = stand.split(",")
                    if stand[0] == airport and stand[1] == user_stand:
                        lat = stand[2]
                        long = stand[3]
                        hdg = stand[4].strip()
            crz = (500 * random.randint(1,3)) + 1000
            rmk = "v"
            return cs, lat, long, hdg, type, crz, dest, rmk, rules
