import csv

class RoomLayout:
    dimensions = None
    lights = []

    def __init__(FileName):
        with open(FileName, 'r') as input:
            reader = csv.reader(input, delimiter=' ')
            
            row1 = next(reader)
            dimensions = (float(row1[0]), float(row1[1]))
            
            for line in reader:
                lights.append(float(line[0]), float(line[1]))

