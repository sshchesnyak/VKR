import main.modules.geo_utils as g
import json


class LandingSpot:
    def __init__(self, lat_min, lon_min, lat_max, lon_max):
        self.lat_min = lat_min
        self.lon_min = lon_min
        self.lat_max = lat_max
        self.lon_max = lon_max
        self.x_min, self.y_min = g.gc_to_tm(self.lat_min, self.lon_min)
        self.x_max, self.y_max = g.gc_to_tm(self.lat_max, self.lon_max)
        self.point_group = []
        self.residential = 0
        self.relaxation = 0
        self.protected = 0
        self.private_property = 0
        self.roads = 0
        self.aviation = 0
        self.category = 0
        self.height_diff = 0
        self.angle = 0
        self.wind = 0
        self.precipitation = 0
        self.result = 0
        self.best = False
        self.polygon = [
            [self.lon_min, self.lat_min],
            [self.lon_max, self.lat_min],
            [self.lon_max, self.lat_max],
            [self.lon_min, self.lat_max],
            [self.lon_min, self.lat_min]
        ]


class LandingJSON:
    def __init__(self, polygon, result, best):
        self.polygon = polygon
        self.a_result = result
        self.best = best

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class AggregatorWorker:
    def __init__(self):
        self.alternatives = []

    def operator_121_function(self, alternative):
        coefficients = [0.921773, 0.110987, 0.008098, 0.960317, 0.969553, 0.110988, 1]
        criteria_set = [[alternative.category, 1], [alternative.height_diff, 2], [alternative.angle, 3]]
        for i in range(0, 3):
            for j in range(0, 2-i):
                if criteria_set[j][0] > criteria_set[j+1][0]:
                    criteria_set[j][0], criteria_set[j+1][0] = criteria_set[j+1][0], criteria_set[j][0]
        result = criteria_set[0][0]
        previous = criteria_set[0][0]
        criteria_set.pop(0)
        result = result+(criteria_set[0][0]-previous)*coefficients[criteria_set[0][1]+criteria_set[1][1]]
        previous = criteria_set[0][0]
        criteria_set.pop(0)
        result = result+(criteria_set[0][0]-previous)*coefficients[criteria_set[0][1]-1]
        criteria_set.pop(0)
        return result

    def operator_11_function(self, operator_111, alternative):
        coefficients = [0.909866, 0.222899, 1]
        criteria_set = [[operator_111, 1], [alternative.aviation, 2]]
        for i in range(0, 2):
            for j in range(0, 1 - i):
                if criteria_set[j][0] > criteria_set[j + 1][0]:
                    criteria_set[j][0], criteria_set[j + 1][0] = criteria_set[j + 1][0], criteria_set[j][0]
        result = criteria_set[0][0]
        previous = criteria_set[0][0]
        criteria_set.pop(0)
        result = result + (criteria_set[0][0] - previous) * coefficients[criteria_set[0][1] - 1]
        criteria_set.pop(0)
        return result

    def aggregate(self, alternative):
        operator_1111 = min(alternative.residential, alternative.relaxation)
        operator_1112 = min(alternative.protected, alternative.private_property, alternative.roads)
        if operator_1111 == 0 or operator_1112 == 0:
            operator_111 = 0
        else:
            operator_111 = (0.53*operator_1111**(-9.061)+0.47*operator_1112**(-9.061))**(-1/9.061)
        operator_121 = self.operator_121_function(alternative)
        if alternative.wind == 0:
            operator_122 = 0
        else:
            operator_122 = ((0.125*alternative.wind+0.875*alternative.precipitation)*alternative.wind)/(0.429*alternative.wind+(0.125*alternative.wind+0.875*alternative.precipitation)*0.571)
        operator_11 = self.operator_11_function(operator_111, alternative)
        if operator_121 == 0:
            operator_12 = 0
        else:
            operator_12 = ((0.333*operator_121+0.667*operator_122)*operator_121)/(0.5*operator_121+(0.333*operator_121+0.667*operator_122)*0.5)
        if operator_11 == 0:
            operator_1 = 0
        else:
            operator_1 = ((0.2*operator_11+0.8*operator_12)*operator_11)/(0.75*operator_11+(0.2*operator_11+0.8*operator_12)*0.25)
        alternative.result = operator_1

    def aggregator_json(self):
        aggregated_data = []
        for alternative in self.alternatives:
            json_object = LandingJSON(alternative.polygon, alternative.result, alternative.best)
            aggregated_data.append(json_object.to_json())
        return aggregated_data
