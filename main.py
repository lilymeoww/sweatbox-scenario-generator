from func import get_route, generate_random_pilot

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
                f"@N:{self.cs}:{self.sq.rjust(4, '0')}:1:{self.lat}:{self.long}:{self.alt}:0:{self.hdg}:0\n"
                f"$FP{self.cs}:*A:{self.rules}:{self.ac_type}:420:{self.dep}:0000::{self.crz}:{self.dest.strip()}:00:00:0:0::/{self.rmk}/:{self.rte.strip()}\n"
                f"SIMDATA:{self.cs}:*:*:25.1.0.000\n"
                f"$ROUTE:{self.pseudo_route}\n"
                f"DELAY:1:2\n"
                f"REQALT::7000\n"
                f"INITIALPSEUDOPILOT:{self.dep}_M_GND")


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
        scenario_file_str = f"PSEUDOPILOT:ALL\n\nAIRPORT_ALT:{self.airport.altitude}\n\n{self.app_data}\n\n"
        scenario_file_str += "".join(str(controller) + "\n" for controller in self.controllers)
        scenario_file_str += "\n".join(str(pilot) for pilot in self.pilots)
        return scenario_file_str


if __name__ == "__main__":
    airport = Airport("EGPH", 136, "24", "GND")
    app_data = """ILS24:55.9560884:-3.3546135:55.9438540:-3.3907010
    ILS06:55.9437922:-3.3908724:55.9561296:-3.3544421
    ILS:55.9513586:-3.3594437:118.0
    ILS:55.9436373:-3.3341400:298.0"""
    scenario = Scenario(airport, app_data)

    # Handle VFR Factor Input
    while True:
        try:
            vfr_factor = int(input("Percentage VFR (integer 0-100): "))
            if 0 <= vfr_factor <= 100:
                break
            else:
                print("Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            incorrect_factor = int(input("Percentage of IFR with invalid routes (integer 0-100): "))
            if 0 <= incorrect_factor <= 100:
                break
            else:
                print("Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            level_factor = int(input("Percentage of IFR with invalid levels (integer 0-100): "))
            if 0 <= level_factor <= 100:
                break
            else:
                print("Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    while True:
        try:
            entry_error_factor = int(input("Percentage of IFR with flight plan entry errors, such as filing from wrong airport, typo on a/c type etc. (integer 0-100): "))
            if 0 <= entry_error_factor <= 100:
                break
            else:
                print("Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # Adding Controllers
    while input("Add more controllers? (y/n): ").lower() == "y":
        try:
            name = input("Enter controller callsign: ").upper().strip()
            freq = input("Enter controller freq: ").strip()
            controller = Controller(airport.icao, "GND", name, freq)
            scenario.add_controller(controller)
        except Exception as e:
            print(f"Error adding controller: {e}. Please try again.")

    current_sq = 0

    # Adding Pilots
    while True:
        add_more = input("Add more pilots? (M)anual, (A)uto, (N)o: ").lower()
        if add_more in ['m', 'a', 'n']:
            break
        print("Invalid option. Please enter 'm', 'a', or 'n'.")

    while add_more != "n":
        try:
            current_sq += 1
            if add_more == "m":
                cs = input("Enter c/s: ")
                lat = input("Enter latitude: ")
                long = input("Enter longitude: ")
                alt = airport.altitude
                hdg = int(input("Enter a/c heading (0-359): ")) % 360
                dep = airport.icao
                sq = f"{current_sq:04}"
                rules = input("Enter a/c flight rules (I/V): ").upper()
                input_ac_type = input("Enter a/c type as displayed on fpln: ")
                cruise_fl = input("Enter cruise level as altitude: ")
                dest = input("Enter aircraft destination airport: ")
                rmk = input("Enter voice rules (v, r, t, or empty): ")

                route, pseudo_route = ("", "")
                if rules == "I":
                    route, pseudo_route = get_route(dep, dest)

                pilot = Pilot(cs, lat, long, alt, hdg, dep, sq, rules, input_ac_type, cruise_fl, dest, rmk, route, pseudo_route)
                scenario.add_pilot(pilot)

            elif add_more == "a":
                try:
                    cs, lat, long, hdg, ac_type, crz, dest, rmk, rules, rte, pseudo_route = generate_random_pilot(airport.icao, vfr_factor, incorrect_factor, level_factor, entry_error_factor)
                    alt = airport.altitude
                    dep = airport.icao
                    sq = f"{current_sq:04}"
                    pilot = Pilot(cs, lat, long, alt, hdg, dep, sq, rules, ac_type, crz, dest, rmk, rte, pseudo_route)
                    scenario.add_pilot(pilot)
                except Exception as e:
                    print(f"Error generating random pilot: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        add_more = input("Add more pilots? (M)anual, (A)uto, (N)o: ").lower()

    # Save scenario to file
    try:
        with open("testsb.txt", "w") as scenario_file:
            scenario_file.write(scenario.generate_scenario())
        print("Written to file!")
    except IOError as e:
        print(f"Error writing to file: {e}")
