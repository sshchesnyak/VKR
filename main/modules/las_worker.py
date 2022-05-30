import laspy as lp
import numpy as np
import geopy.distance as distance
import os
import sys
import traceback
import main.modules.geo_utils as g
from main.modules.aggregator_worker import LandingSpot
import main.modules.consts as c


class lasWorker:

    def __init__(self, basedir):
        self.coordinate_info = None
        self.lon_max = None
        self.lat_max = None
        self.lon_min = None
        self.lat_min = None
        self.z_max = None
        self.z_min = None
        self.y_max = None
        self.y_min = None
        self.x_max = None
        self.x_min = None
        self.point_count = None
        self.dim_info = None
        self.dims = None
        self.las_header = None
        self.las_file = None
        self.filename = None
        self.cells = None
        self.directory = basedir

    def get_files(self):
        try:
            las_files = []

            def laz_to_las(input_laz, output_las):
                las = lp.read(input_laz)
                las = lp.convert(las)
                las.write(output_las)

            for dirpath, dirnames, filenames in os.walk(self.directory):
                for index, file in enumerate(filenames):
                    if file.endswith('.laz'):
                        input_laz = os.path.join(dirpath, file)
                        output_las = input_laz.replace('laz', 'las')
                        if not (os.path.exists(output_las)):
                            print("Working on file no ", index, " :", os.path.dirname(os.path.realpath(input_laz)))
                            laz_to_las(input_laz, output_las)
                            print("Completed")
                        else:
                            realpath = os.path.basename(output_las)
                            print("File no ", filenames.index(realpath), " (", realpath, ") already exists!")
                        las_files.append(os.path.basename(output_las))
            return las_files

        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            print('Error in read_xmp.py')
            print("PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1]))

    def set_las_parameters(self, filename):
        self.las_file = lp.read(self.directory + filename)
        self.las_header = self.las_file.header
        self.filename = filename
        self.dims = list(self.las_file.point_format.dimension_names)
        self.dim_info = list(self.las_file.point_format.standard_dimensions)
        self.coordinate_info = self.las_header.vlrs
        self.point_count = self.las_header.point_count
        self.x_min = self.las_header.x_min
        self.x_max = self.las_header.x_max
        self.y_min = self.las_header.y_min
        self.y_max = self.las_header.y_max
        self.z_min = self.las_header.z_min
        self.z_max = self.las_header.z_max
        self.lat_min, self.lon_min = g.tm_to_gc(self.x_min, self.y_min)
        self.lat_max, self.lon_max = g.tm_to_gc(self.x_max, self.y_max)

    def get_rectangle(self):
        return [
            {self.lat_min, self.lon_min},
            {self.lat_max, self.lon_min},
            {self.lat_max, self.lon_max},
            {self.lat_min, self.lon_max},
            {self.lat_min, self.lon_min},
        ]

    def estimate_ground_roughness(self):
        x_limit, y_limit = g.get_corner_xy(self.lat_min, self.lon_min)
        request = np.logical_and(self.las_file.x <= x_limit, self.las_file.y <= y_limit)
        point_group = self.las_file.points[request]
        print(len(point_group))
        print(point_group.x)
        print(point_group.y)
        print(point_group.z)

    def primary_category(self, landing_spot):
        most_common_index = 0
        grade = 0
        point_classes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for point in landing_spot.point_group:
            current_index = 0
            current_grade = 0
            if point.classification == 1:
                point_classes[0] += 1
                current_index = 0
                current_grade = 0
            if point.classification == 2:
                point_classes[1] += 1
                current_index = 1
                current_grade = 1
            if point.classification == 3:
                point_classes[2] += 1
                current_index = 2
                current_grade = 0.75
            if point.classification == 4:
                point_classes[3] += 1
                current_index = 3
                current_grade = 0.44
            if point.classification == 5:
                point_classes[4] += 1
                current_index = 4
                current_grade = 0.13
            if point.classification == 6:
                point_classes[5] += 1
                current_index = 5
                current_grade = 0
            if point.classification == 7:
                point_classes[6] += 1
                current_index = 6
                current_grade = 0
            if point.classification == 8:
                point_classes[7] += 1
                current_index = 7
                current_grade = 0
            if point.classification == 9:
                point_classes[8] += 1
                current_index = 8
                current_grade = 0
            if point.classification == 12:
                point_classes[9] += 1
                current_index = 9
                current_grade = 0
            if point.classification == 17:
                point_classes[10] += 1
                current_index = 10
                current_grade = 0
            if point.classification == 41:
                point_classes[11] += 1
                current_index = 11
                current_grade = 0
            if point_classes[current_index] > point_classes[most_common_index]:
                most_common_index = current_index
                grade = current_grade
        landing_spot.category = grade

    def height_diff(self, landing_spot):
        heights = []
        base_height = min(landing_spot.point_group.z)
        grade = 0
        for z in landing_spot.point_group.z:
            current_height = z - base_height
            heights.append(current_height)
        max_diff = max(heights)*100
        if max_diff < 20:
            grade = -0.05*max_diff+1
        else:
            grade = 0
        landing_spot.height_diff = grade

    def angle(self, landing_spot):
        tmp_a = []
        tmp_b = []
        grade = 0
        for x, y, z in zip(landing_spot.point_group.x, landing_spot.point_group.y, landing_spot.point_group.z):
            current_lat, current_lon = g.tm_to_gc(x, y)
            tmp_a.append([current_lon, current_lat, 1])
            tmp_b.append(z)
        a = np.matrix(tmp_a)
        b = np.matrix(tmp_b).T
        phi = 0
        if len(landing_spot.point_group.x) < 3:
            grade = 0
        if len(landing_spot.point_group.x) == 3:
            coefficients = a.I * b
            phi = np.rad2deg(np.arccos(abs(coefficients[2])/np.sqrt(coefficients[0]**2+coefficients[1]**2+coefficients[2]**2))).item()
            if 0 <= phi < 10:
                grade = -0.08*phi+1
            if 10 <= phi < 15:
                grade = -0.04*phi+0.6
            if phi >= 15:
                grade = 0
        if len(landing_spot.point_group.x) > 3:
            try:
                coefficients = (a.T * a).I * a.T * b
                phi = np.rad2deg(np.arccos(abs(coefficients[2]) / np.sqrt(coefficients[0] ** 2 + coefficients[1] ** 2 + coefficients[2] ** 2))).item()
                if 0 <= phi < 10:
                    grade = -0.08 * phi + 1
                if 10 <= phi < 15:
                    grade = -0.04 * phi + 0.6
                if phi >= 15:
                    grade = 0
            except np.linalg.LinAlgError as err:
                if 'Singular matrix' in str(err):
                    grade = 0
                else:
                    grade = 0
        landing_spot.angle = grade

    def get_grade_grid(self, aggregator, lds, flight, weather):
        current_lat = self.lat_min
        current_lon = self.lon_min
        source_lon = self.lon_min
        aggregator.alternatives = []

        i = 0
        print(self.lon_min, self.lat_min)
        print(self.lon_max, self.lat_max)
        while current_lat < self.lat_max:
            if current_lat >= self.lat_max:
                break
            while current_lon < self.lon_max:
                new_lat, new_lon = g.get_corner_coords(current_lat, current_lon)
                if new_lon >= self.lon_max:
                    new_lon = self.lon_max
                    aggregator.alternatives.append(LandingSpot(current_lat, current_lon, new_lat, new_lon))
                    current_lon = source_lon
                    current_lat = new_lat
                    break
                else:
                    aggregator.alternatives.append(LandingSpot(current_lat, current_lon, new_lat, new_lon))
                    current_lon = new_lon
                i = i+1
                if i % 20000 == 0:
                    print(i)
                    print(current_lon, current_lat)
        print(len(aggregator.alternatives))
        i = 0
        results = []
        overall_results = []
        overall_indices = []
        for alternative in aggregator.alternatives:
            part_x = np.logical_and(alternative.x_min <= self.las_file.x, self.las_file.x <= alternative.x_max)
            part_y = np.logical_and(alternative.y_min <= self.las_file.y, self.las_file.y <= alternative.y_max)
            request = np.logical_and(part_x, part_y)
            point_group = self.las_file.points[request]
            alternative.point_group = point_group[::100]
            if len(alternative.point_group.x)>0:
                self.primary_category(alternative)
                self.height_diff(alternative)
                self.angle(alternative)
            else:
                alternative.category = 0
                alternative.height_diff = 0
                alternative.angle = 0
            lds.residential_grade(alternative)
            lds.relaxation_grade(alternative)
            lds.protected_grade(alternative)
            lds.private_property_grade(alternative)
            lds.roads_grade(alternative)
            flight.aviation_grade(alternative)
            weather.wind_grade(alternative)
            weather.precipitation_grade(alternative)
            aggregator.aggregate(alternative)
            results.append(alternative.result)
            i = i+1
            if i % 100 == 0:
                best_result = max(results)
                overall_results.append(best_result)
                best_index = i-100+results.index(best_result)
                overall_indices.append(best_index)
                results = []
                print(i, best_result, best_index)
        the_best_result = max(overall_results)
        index = overall_results.index(the_best_result)
        the_best_index = overall_indices[index]
        aggregator.alternatives[the_best_index].best = True
        print(overall_results)
        print(overall_indices)
        print(the_best_result)
        print(the_best_index)





