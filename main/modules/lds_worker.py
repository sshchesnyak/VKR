import json
import requests
from shapely import geometry, ops
from geopy import distance as dist
import random


class LandUse:
    def __init__(self, object_type, use_type, distance, geo_type, polygons):
        self.object_type = object_type
        self.use_type = use_type
        self.distance = distance
        self.geo_type = geo_type
        self.no_of_polygons = len(polygons)
        self.polygons = polygons
        self.rand = random.random()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Relaxation:
    def __init__(self, intent, geo_type, polygon):
        self.intent = intent
        self.geo_type = geo_type
        self.polygon = polygon

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Protected:
    def __init__(self, object_type, geo_type, polygons):
        self.object_type = object_type
        self.geo_type = geo_type
        self.polygons = polygons

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class PrivateProperty:
    def __init__(self, geo_type, polygons):
        self.geo_type = geo_type
        self.polygons = polygons

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Road:
    def __init__(self, object_type, geo_type, lines):
        self.object_type = object_type
        self.geo_type = geo_type
        self.object_lines = lines

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class LdsWorker:
    def __init__(self):
        self.mfe_key = "cf3bd4a556614df9913e49f5d4ae80c7"
        self.lds_key = "e2d1463853794644a6b0a35056ac411d"
        self.land_use = []
        self.residential = []
        self.relaxation = []
        self.protected = []
        self.private_property = []
        self.roads = []

    def get_land_use(self, lat, lon, max_dim):
        self.land_use.clear()
        response = requests.get("https://data.mfe.govt.nz/services/query/v1/vector.json?key=" + str(self.mfe_key) + "&layer=52375&x=" + str(lon) + "&y=" + str(lat) + "&max_results=" + str(30) + "&radius=" + str(max_dim) + "&geometry=true&with_field_names=true")
        raw_data = response.json()
        features_array = list(raw_data.get('vectorQuery').get('layers').get('52375').get('features'))
        for feature in features_array:
            object_type = feature.get('type')
            use_type = feature.get('properties').get('LUCNA_2016')
            distance = feature.get('distance')
            geo_type = feature.get('geometry').get('type')
            polygons = feature.get('geometry').get('coordinates')[0]
            self.land_use.append(LandUse(object_type, use_type, distance, geo_type, polygons))

    def land_use_json(self):
        land_use_data = []
        for area in self.land_use:
            land_use_data.append(area.to_json())
        return land_use_data

    def get_residential(self, lat, lon, max_dim):
        self.residential.clear()
        response = requests.get("https://data.linz.govt.nz/services/query/v1/vector.json?key=" + str(self.lds_key) + "&layer=52375&x=" + str(lon) + "&y=" + str(lat) + "&max_results=" + str(30) + "&radius=" + str(max_dim) + "&geometry=true&with_field_names=true")
        raw_data = response.json()
        layers = raw_data.get('vectorQuery').get('layers')
        if len(layers) == 0:
            print("Residential list empty")
        else:
            features = layers.get('52375').get('features')
            print(features)
        print("Residential complete")

    def residential_json(self):
        residential_data = []
        for area in self.residential:
            residential_data.append(area.to_json())
        return residential_data

    def get_relaxation(self, lat, lon, max_dim):
        self.relaxation.clear()
        response = requests.get("https://data.linz.govt.nz/services/query/v1/vector.json?key=" + str(self.lds_key) + "&layer=50782&x=" + str(lon) + "&y=" + str(lat) + "&max_results=" + str(30) + "&radius=" + str(max_dim) + "&geometry=true&with_field_names=true")
        raw_data = response.json()
        features = raw_data.get('vectorQuery').get('layers').get('50782').get('features')
        if len(features) == 0:
            print("Relaxation list empty")
        else:
            for feature in features:
                properties = feature.get('properties')
                intent = properties.get('parcel_intent')
                geo_type = feature.get('geometry').get('type')
                polygon = feature.get('geometry').get('coordinates')[0]
                self.relaxation.append(Relaxation(intent, geo_type, polygon))
        print("Relaxation complete")

    def relaxation_json(self):
        relaxation_data = []
        for area in self.relaxation:
            relaxation_data.append(area.to_json())
        return relaxation_data

    def get_protected(self, lat, lon, max_dim):
        self.protected.clear()
        response = requests.get("https://data.linz.govt.nz/services/query/v1/vector.json?key=" + str(self.lds_key) + "&layer=53564&x=" + str(lon) + "&y=" + str(lat) + "&max_results=" + str(50) + "&radius=" + str(max_dim) + "&geometry=true&with_field_names=true")
        raw_data = response.json()
        layers = raw_data.get('vectorQuery').get('layers')
        if len(layers) == 0:
            print("Protected list empty")
        else:
            features = layers.get('53564').get('features')
            for feature in features:
                object_type = feature.get('properties').get('type')
                geo_type = feature.get('geometry').get('type')
                polygons = feature.get('geometry').get('coordinates')[0]
                self.protected.append(Protected(object_type, geo_type, polygons))
        print("Protected complete")

    def protected_json(self):
        protected_data = []
        for area in self.protected:
            protected_data.append(area.to_json())
        return protected_data

    def get_properties(self, lat, lon, max_dim):
        self.private_property.clear()
        response = requests.get("https://data.linz.govt.nz/services/query/v1/vector.json?key=" + str(self.lds_key) + "&layer=50772&x=" + str(lon) + "&y=" + str(lat) + "&max_results=" + str(50) + "&radius=" + str(max_dim) + "&geometry=true&with_field_names=true")
        raw_data = response.json()
        layers = raw_data.get('vectorQuery').get('layers')
        if len(layers) == 0:
            print("Property list empty")
        else:
            features = layers.get('50772').get('features')
            for feature in features:
                if feature.get('properties').get('parcel_intent') == 'Fee Simple Title':
                    geo_type = feature.get('geometry').get('type')
                    polygons = feature.get('geometry').get('coordinates')[0]
                    self.private_property.append(PrivateProperty(geo_type, polygons))
        print("Property complete")

    def properties_json(self):
        properties_data = []
        for area in self.private_property:
            properties_data.append(area.to_json())
        return properties_data

    def get_roads(self, lat, lon, max_dim):
        self.roads.clear()
        response = requests.get("https://data.linz.govt.nz/services/query/v1/vector.json?key=" + str(self.lds_key) + "&layer=53378&x=" + str(lon) + "&y=" + str(lat) + "&max_results=" + str(50) + "&radius=" + str(max_dim) + "&geometry=true&with_field_names=true")
        raw_data = response.json()
        layers = raw_data.get('vectorQuery').get('layers')
        if len(layers) == 0:
            print("Road list empty")
        else:
            features = layers.get('53378').get('features')
            for feature in features:
                object_type = feature.get('properties').get('geometry_class')
                geo_type = feature.get('geometry').get('type')
                lines = feature.get('geometry').get('coordinates')
                self.roads.append(Road(object_type, geo_type, lines))
        print("Roads complete")

    def roads_json(self):
        roads_data = []
        for area in self.roads:
            roads_data.append(area.to_json())
        return roads_data

    def residential_grade(self, landing_spot):
        grade = 0
        if len(self.residential) == 0:
            grade = 1
        landing_spot.residential = grade

    def relaxation_grade(self, landing_spot):
        grade = 0
        if len(self.relaxation) == 0:
            grade = 1
        else:
            distances = []
            for area in self.relaxation:
                for polygon in area.polygon:
                    lon = (landing_spot.lon_min+landing_spot.lon_max)/2
                    lat = (landing_spot.lat_min+landing_spot.lat_max)/2
                    s_polygon = geometry.Polygon(polygon)
                    s_point = geometry.Point(lon, lat)
                    p1, p2 = ops.nearest_points(s_polygon, s_point)
                    delta = dist.distance((p1.y, p1.x), (p2.y, p2.x)).meters
                    distances.append(delta)
            distance = min(distances)
            if 0 <= distance < 150:
                grade = (0.02*distance)/3
            else:
                grade = 1
        landing_spot.relaxation = grade

    def protected_grade(self, landing_spot):
        grade = 0
        if len(self.protected) == 0:
            grade = 1
        else:
            distances = []
            for area in self.protected:
                for polygon in area.polygons:
                    lon = (landing_spot.lon_min+landing_spot.lon_max)/2
                    lat = (landing_spot.lat_min+landing_spot.lat_max)/2
                    s_polygon = geometry.Polygon(polygon)
                    s_point = geometry.Point(lon, lat)
                    p1, p2 = ops.nearest_points(s_polygon, s_point)
                    delta = dist.distance((p1.y, p1.x), (p2.y, p2.x)).meters
                    distances.append(delta)
            distance = min(distances)
            if 0 <= distance < 150:
                grade = (0.02*distance)/3
            else:
                grade = 1
        landing_spot.protected = grade

    def private_property_grade(self, landing_spot):
        grade = 0
        if len(self.private_property) == 0:
            grade = 1
        else:
            distances = []
            for area in self.private_property:
                for polygon in area.polygons:
                    lon = (landing_spot.lon_min+landing_spot.lon_max)/2
                    lat = (landing_spot.lat_min+landing_spot.lat_max)/2
                    s_polygon = geometry.Polygon(polygon)
                    s_point = geometry.Point(lon, lat)
                    p1, p2 = ops.nearest_points(s_polygon, s_point)
                    delta = dist.distance((p1.y, p1.x), (p2.y, p2.x)).meters
                    distances.append(delta)
            distance = min(distances)
            if 0 <= distance < 150:
                grade = (0.02*distance)/3
            else:
                grade = 1
        landing_spot.private_property = grade

    def roads_grade(self, landing_spot):
        grade = 0
        if len(self.roads) == 0:
            grade = 1
        else:
            distances = []
            for road in self.roads:
                for line in road.object_lines:
                    lon = (landing_spot.lon_min+landing_spot.lon_max)/2
                    lat = (landing_spot.lat_min+landing_spot.lat_max)/2
                    s_line = geometry.LineString(line)
                    s_point = geometry.Point(lon, lat)
                    p1, p2 = ops.nearest_points(s_line, s_point)
                    delta = dist.distance((p1.y, p1.x), (p2.y, p2.x)).meters
                    distances.append(delta)
            distance = min(distances)
            if 0 <= distance < 150:
                grade = (0.02*distance)/3
            else:
                grade = 1
        landing_spot.roads = grade
