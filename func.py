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

def generate_random_pilot():
    if random.randint(1,10) <= 20:
        with open("callsignsVFR.txt", "r") as file:
            callsigns = file.readlines()
            chosen_callsign = random.choice(callsigns).split(",")
            cs = chosen_callsign[0]
            dest = random.choice(chosen_callsign[0:])
            with open("aircrafttypes.txt", "r") as typefile:
                type = random.choice(typefile.readline().split(","))
            stand = input("Enter stand number: ")