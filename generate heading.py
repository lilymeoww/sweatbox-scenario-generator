hdg = int(input("Enter a/c heading: ")) % 360
hdg = int(((hdg * 2.88) + 0.5)) << 2

print(hdg)