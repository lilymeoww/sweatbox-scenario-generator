import random
import string

def get_route(departure, arrival):
    with open("routes.txt", "r") as file:
        routes = file.readlines()
        for i, route in enumerate(routes, start=1):
            route_str = route.split(",")[0]
            if route_str.split(" ")[0].strip() == departure.strip() and route_str.split(" ")[-1].strip() == arrival.strip():
                print(route.split(",")[1])
                return route_str.replace("\n", ""), route.split(",")[1]
    return f"{departure} {arrival}", "E"

def get_dep_for_route(departure, first_wp, config):
    with open("departure_routes.txt", "r") as file:
        routes = file.readlines()
        for route in routes:
            route_comp = route.strip().split(",")
            if route_comp[0] == departure and route_comp[1] == config and route_comp[2] == first_wp:
                return route_comp[3]
    return first_wp

def generate_random_pilot(dep, config, vfr_factor):
    if random.randint(1, 100) <= int(vfr_factor):
        with open("callsignsVFR.txt", "r") as file:
            callsigns = file.readlines()
            chosen_callsign = random.choice(callsigns).split(",")
            cs = chosen_callsign[0]
            rules = "V"
            dest = random.choice(chosen_callsign[0:])
            ac_type = random.choice(["P28A", "C172", "C152", "DA42"])
            
            # Retry mechanism for getting stand number
            while True:
                user_stand = input("Enter stand number: ").upper()
                with open("stands.txt", "r") as standfile:
                    stands = standfile.readlines()
                    for stand in stands:
                        stand = stand.split(",")
                        if stand[0] == dep and stand[1] == user_stand:
                            lat = stand[2]
                            long = stand[3]
                            hdg = stand[4].strip()
                            break
                    else:
                        print("Please enter a valid stand number.")
                        continue  # Retry if the stand is invalid
                break  # Break the loop if a valid stand is found

            crz = (500 * random.randint(1, 3)) + 1000
            rmk = "v"
            rte = "VFR"
            pseudo_route = ""
            return cs, lat, long, hdg, ac_type, crz, dest, rmk, rules, rte, pseudo_route
    else:
        with open("callsignsIFR.txt", "r") as file:
            callsigns = file.readlines()
            chosen_callsign = random.choice(callsigns).split(",")
            cs = chosen_callsign[0] + str(random.randint(10, 99)) + random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
            rules = "I"
            dest = random.choice(chosen_callsign[1:])
            
            # Finding aircraft type based on the callsign
            with open("aircrafttypes.txt", "r") as typefile:
                for type in typefile:
                    type = type.strip()
                    if str(type.split(",")[0]) == str(cs[:3]):
                        ac_type = random.choice(type.split(",")[1:])
                        break
                else:
                    ac_type = "DEFAULT"  # Assign a default type if not matched

            # Retry mechanism for getting stand number
            while True:
                user_stand = input("Enter stand number: ").upper()
                with open("stands.txt", "r") as standfile:
                    stands = standfile.readlines()
                    for stand in stands:
                        stand = stand.split(",")
                        if stand[0] == dep and stand[1] == user_stand:
                            lat = stand[2]
                            long = stand[3]
                            hdg = stand[4].strip()
                            break
                    else:
                        print("Please enter a valid stand number.")
                        continue  # Retry if the stand is invalid
                break  # Break the loop if a valid stand is found

            rmk = "v"
            rte, crz = get_route(dep, dest)
            pseudo_route = ""
            return cs, lat, long, hdg, ac_type, crz.strip(), dest, rmk, rules, rte, pseudo_route
