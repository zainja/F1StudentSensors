


import datetime
class data_sent:
    def __init__(self, data):
        self.rpm = data[0] << 8 + data[1]
        self.speed10 = data[11] << 8 + data[10]
        self.fuel_pressure = (data[3] << 8 + data[12])/100
        self.wt = data[5]
        self.tps = data[9]
        self.a_t = data[7]
        self.map = data[6]
        self.o_t = data[4]
        self.hertz = data[12]
        self.tsp1 = data[9]
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def return_dict(self):
        return {"Current Time": self.date,"RPM": self.rpm,
                "Speed": self.speed10,
                "Fuel Pressure": self.fuel_pressure, "WT": self.wt,
                "TPS": self.tps, "AT": self.a_t, "Map": self.map,
                "OT": self.o_t, "Hertz": self.hertz, "TSP1": self.tsp1}
