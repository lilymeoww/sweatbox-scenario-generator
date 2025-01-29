import random
import string

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
            if route_str.split(" ")[0].strip() == departure.strip() and route_str.split(" ")[-1].strip() == arrival.strip():
                # print(f"Route found: {route.split(',')[1].strip()}")
                poss_routes.append([route_str.replace("\n", ""), route.split(",")[1].strip()])
                # print(poss_routes)
        route_chosen = random.choice(poss_routes)
        return route_chosen[0], route_chosen[1]

    except FileNotFoundError:
        print("Error: routes.txt file not found.")
    return f"{departure} {arrival}", "E"


def get_dep_for_route(departure, first_wp, config):
    try:
        with open("departure_routes.txt", "r") as file:
            routes = file.readlines()
            for route in routes:
                route_comp = route.strip().split(",")
                if route_comp[0] == departure and route_comp[1] == config and route_comp[2] == first_wp:
                    return route_comp[3]
    except FileNotFoundError:
        print("Error: departure_routes.txt file not found.")
    return first_wp


def validate_stand(dep):
    while True:
        user_stand = input("Enter stand number: ").upper()
        try:
            with open("stands.txt", "r") as standfile:
                stands = standfile.readlines()
                for stand in stands:
                    stand = stand.split(",")
                    if stand[0] == dep and stand[1] == user_stand:
                        return stand[2], stand[3], stand[4].strip()
            print("Please enter a valid stand number.")
        except FileNotFoundError:
            print("Error: stands.txt file not found.")
            break


def generate_random_pilot(dep, vfr_factor: int, incorrect_factor: int, level_factor: int, entry_error_factor: int):
    try:
        if random.randint(1, 100) <= int(vfr_factor):
            with open("callsignsVFR.txt", "r") as file:
                callsigns = file.readlines()
                chosen_callsign = random.choice(callsigns).split(",")
                cs = chosen_callsign[0]
                rules = "V"
                dest = random.choice(["EGPF","EGPB","EGNX","EGPC","EGAA","EGPH","EGLK","EGLF","EGMA","EGFF"])

                ac_type = random.choice(["P28A", "C172", "C152", "DA42"])

                adep = dep

                lat, long, hdg = validate_stand(dep)
                hdg = int(((int(hdg) * 2.88) + 0.5)) << 2
                crz = (500 * random.randint(1, 3)) + 1000
                rmk = "v"
                rte = "VFR"
                pseudo_route = ""
                return cs, lat, long, hdg, ac_type, crz, adep, dest, rmk, rules, rte, pseudo_route
        else:
            with open("callsignsIFR.txt", "r") as file:
                callsigns = file.readlines()
                chosen_callsign = random.choice(callsigns).split(",")
                cs = chosen_callsign[0] + str(random.randint(10, 99)) + random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
                rules = "I"
                dest = chosen_callsign[1].strip()

        with open("aircrafttypes.txt", "r") as typefile:
            for type in typefile:
                type = type.strip()
                if type.split(",")[0] == cs[:3]:
                    ac_type = random.choice(type.split(",")[1:])
                    break
            else:
                ac_type = "UNKNOWN"  # Default if not found

        lat, long, hdg = validate_stand(dep)
        hdg = int(((int(hdg) * 2.88) + 0.5)) << 2

        rmk = "v"
        rte, crz = get_route(dep, dest, incorrect_factor)
        if random.randint(1,100) <= level_factor:
            with open("invalidAltitudes.txt", "r") as file:
                invalidAlts = file.readlines()
                found = False
                for alt in invalidAlts:
                    if not found and alt.split(",")[0] == dep and alt.split(",")[1] == dest:
                        crz = alt.split(",")[2].strip()
                        found = True
        pseudo_route = ""

        if random.randint(1, 100) <= entry_error_factor:
            entry_error_options = ["type", "dep"]
            chosen_error = random.choice(entry_error_options)
            if chosen_error == "type":
                with open("errorTypes.txt", "r") as file:
                    bad_types = file.readlines()
                    for bad_type in bad_types:
                        if bad_type.split(",")[0] == ac_type:
                            new_type = bad_type.split(",")[1].split()
                ac_type = new_type
            elif chosen_error == "dep":
                with open("adepError.txt", "r") as f:
                    lines = f.readlines()
                    dep = random.choice(lines).strip()
        return cs, lat, long, hdg, ac_type, crz.strip(), dep, dest, rmk, rules, rte, pseudo_route

    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")