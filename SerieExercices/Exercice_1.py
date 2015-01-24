class CalculGeo():

    def __init__(self,donnes):
         self.info = donnes
    def getStationCordinate(self, name):
        name = name.upper()
        #if name in info:
        for element in self.info:
            station = element[0][0] + element[0][1]
            if station == name:
                x = element[1]
                y = element[2]
                break
        return x, y
        #else:
         #   return None
    def calculDistance(self, station1, station2):
        x1 = self.getStationCordinate(station1)[0]
        y1 = self.getStationCordinate(station1)[1]

        x2 = self.getStationCordinate(station2)[0]
        y2 = self.getStationCordinate(station2)[1]

        import math
        return math.sqrt(math.pow((x1-x2), 2) + math.pow((y1-y2), 2))

    def selectProcheStation(self):
        liste = []
        for element in self.info:
            station1 = element[0][0] + element[0][1]
            for element2 in self.info:
                station2 = element2[0][0] + element2[0][1]
                dist = self.calculDistance(station1, station2)
                tup = (dist, station1, station2)
                if dist != 0:
                    liste.append(tup)
        return min(liste)

