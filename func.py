import random, string

def get_route(departure, arrival):
    with open("routes.txt", "r") as file:
        routes = file.readlines()
        for route in routes:
            route_comp = route.strip().split(" ")
            if route_comp[0] == departure and route_comp[-1] == arrival:
                print(route[5:-6])
                return route[5:-6]
        return f"{departure} DIRECT {arrival}"

def get_dep_for_route(departure, first_wp, config):
    with open("departure_routes.txt", "r") as file:
        routes = file.readlines()
        for route in routes:
            route_comp = route.strip().split(",")
            if route_comp[0] == departure and route_comp[1] == config and route_comp[2] == first_wp:
                return route_comp[3]
        return first_wp

def generate_random_pilot(dep, config, vfr_factor):
    if random.randint(1,100) <= int(vfr_factor):
        with open("callsignsVFR.txt", "r") as file:
            callsigns = file.readlines()
            chosen_callsign = random.choice(callsigns).split(",")
            cs = chosen_callsign[0]
            rules = "V"
            dest = random.choice(chosen_callsign[0:])
            with open("aircrafttypes.txt", "r") as typefile:
                ac_type = random.choice(["P28A", "C172", "C152", "DA42"])
            user_stand = input("Enter stand number: ").upper()
            with open("stands.txt", "r") as standfile:
                stands = standfile.readlines()
                for stand in stands:
                    stand = stand.split(",")
                    if stand[0] == dep and stand[1] == user_stand:
                        lat = stand[2]
                        long = stand[3]
                        hdg = stand[4].strip()
            crz = (500 * random.randint(1,3)) + 1000
            rmk = "v"
            rte = "VFR"
            pseudo_route = ""
            return cs, lat, long, hdg, ac_type, crz, dest, rmk, rules, rte, pseudo_route
    else:
        with open("callsignsIFR.txt", "r") as file:
            callsigns = file.readlines()
            chosen_callsign = random.choice(callsigns).split(",")
            cs = chosen_callsign[0] + str(random.randint(10,99)) + random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase)
            rules = "I"
            dest = random.choice(chosen_callsign[0:])
            with open("aircrafttypes.txt", "r") as typefile:
                for type in typefile:
                    type = type.strip()
                    if str(type.split(",")[0]) == str(cs[:3]):
                        print(type.split(",")[1:])
                        ac_type = random.choice(type.split(",")[1:])

            validStand = False
            while validStand == False:
                user_stand = input("Enter stand number: ").upper()
                with open("stands.txt", "r") as standfile:
                    stands = standfile.readlines()
                    for stand in stands:
                        stand = stand.split(",")
                        if stand[0] == dep and stand[1] == user_stand:
                            validStand = True
                            lat = stand[2]
                            long = stand[3]
                            hdg = stand[4].strip()
                if validStand == False:
                    print("Please enter a valid stand number.")
                            
            rmk = "v"
            rte = str(get_route(dep, dest))
            pseudo_route = ""
            return cs, lat, long, hdg, ac_type, crz, dest, rmk, rules, rte, pseudo_route
