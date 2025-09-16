def loadFile():
    with open("demo.txt") as file:
        sbScenario = file.read()

    scenarioSections = [p for p in sbScenario.split('\n\n') if p.strip()]
    dataBlocks = [[line.rstrip() for line in para.splitlines()] for para in scenarioSections]

    pilots = processPilots(dataBlocks)
    return

def processPilots(dataBlocks: list):
    foundPilots = []
    for block in dataBlocks:
        if len(block) >= 2:
            if block[1][:2] == "@N":
                foundPilots.append(block)

    pilots = []
    print(foundPilots[0])
    for pilot in foundPilots:
        cs = pilot[1].split(":")[1]
        lat = pilot[1].split(":")[4]
        long = pilot[1].split(":")[5]
        alt = pilot[1].split(":")[6]
        hdg = round((int(pilot[1].split(":")[8]) / 4 - 0.5) / 2.88)
        dep = pilot[2].split(":")[5]
        sq = pilot[1].split(":")[2]
        rules = pilot[2].split(":")[2]
        ac_type = pilot[2].split(":")[3]
        crz = pilot[2].split(":")[8]
        dest = pilot[2].split(":")[9]
        rmk = pilot[2].split(":")[14]
        rte = pilot[2].split(":")[16]


        pilots.append(Pilot(cs, lat, long, alt, hdg, dep, sq, rules, ac_type, crz, dest, rmk, rte, ""))

    return pilots

#loadFile()