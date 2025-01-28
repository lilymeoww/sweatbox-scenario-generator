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
            route_comp = route.strip.split(",")
            if route_comp[0] == departure and route_comp[1] == config and route_comp[2] == first_wp:
                return route_comp[3]
        return first_wp