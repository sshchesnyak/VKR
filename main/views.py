from django.shortcuts import render
from .modules.las_worker import lasWorker
from .modules.lds_worker import LdsWorker
from .modules.flight_zone_worker import FlightZone
from .modules.weather_worker import WeatherWorker
from .modules.aggregator_worker import AggregatorWorker
from json import dumps, encoder
import json
import geopy.distance as dist
from django.http import HttpResponseBadRequest, JsonResponse

basedir = "C:/Users/sshch_6pmzvii/Documents/Education/BMSTU/FinalPaper/LidarData/"
las = lasWorker(basedir)
lds = LdsWorker()
flight = FlightZone()
weather = WeatherWorker()
aggregator = AggregatorWorker()


class SetEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)


def main_view(request):
    las_files = las.get_files()
    data_dictionary = {
        'las_data': las_files
    }
    data_json = dumps(data_dictionary)
    return render(request, "MainPage.html", {'data': data_json})


def structure_view(request):
    return render(request, "AggregatorStructure.html")


def las_file_update(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("POST Request arrived!")

    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            las_file = data.get('payload')
            las.set_las_parameters(las_file)
            # las.estimate_ground_roughness()
            lat = (las.lat_min+las.lat_max)/2
            lon = (las.lon_min+las.lon_max)/2
            max_dim = round(dist.distance((las.lat_min, las.lon_min), (las.lat_max, las.lon_max)).meters)
            lds.get_land_use(lat, lon, max_dim)
            lds.get_residential(lat, lon, max_dim+150)
            lds.get_relaxation(lat, lon, max_dim+150)
            lds.get_protected(lat, lon, max_dim + 150)
            lds.get_properties(lat, lon, max_dim + 150)
            lds.get_roads(lat, lon, max_dim + 150)
            flight.get_air_zones(las.lat_min, las.lon_min, las.lat_max, las.lon_max)
            weather.get_weather(lat, lon)
            las.get_grade_grid(aggregator, lds, flight, weather)
            return JsonResponse({'status': 'Payload added!'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def get_las_rectanle(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("GET Las Rectangle Request arrived!")

    if is_ajax:
        if request.method == 'GET':
            data = json.dumps(las.get_rectangle(), cls=SetEncoder)
            return JsonResponse({'context': data, 'visible': "visible!"})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def get_land_use(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("GET Land Use Request arrived!")

    if is_ajax:
        if request.method == 'GET':
            data = lds.land_use_json()
            return JsonResponse({'context': json.dumps(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def get_residential(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("GET Residential Request arrived!")

    if is_ajax:
        if request.method == 'GET':
            data = lds.residential_json()
            return JsonResponse({'context': json.dumps(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def get_relaxation(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("GET Relaxation Request arrived!")

    if is_ajax:
        if request.method == 'GET':
            data = lds.relaxation_json()
            return JsonResponse({'context': json.dumps(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def get_protected(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("GET Protected Request arrived!")

    if is_ajax:
        if request.method == 'GET':
            data = lds.protected_json()
            return JsonResponse({'context': json.dumps(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def get_properties(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("GET Properties Request arrived!")

    if is_ajax:
        if request.method == 'GET':
            data = lds.properties_json()
            return JsonResponse({'context': json.dumps(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')


def get_roads(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("GET Roads Request arrived!")

    if is_ajax:
        if request.method == 'GET':
            data = lds.roads_json()
            return JsonResponse({'context': json.dumps(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')

def get_results(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    print("GET Results Request arrived!")

    if is_ajax:
        if request.method == 'GET':
            data = aggregator.aggregator_json()
            return JsonResponse({'context': json.dumps(data)})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')