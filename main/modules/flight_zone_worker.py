import json
import requests


class FlightZone:
    def __init__(self):
        self.key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHxvUUU0V2FvdDRhYjhLbnN4QW92eTVpWGc0QU1nIiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnw0blA3NFhLaVp5YlJabHNiTG92RGx1d29RWDJlIiwib3JnYW5pemF0aW9uX2lkIjoiZGV2ZWxvcGVyfGV2THpxRHdTOVBlYkwzVHliQUxXSmZnQUJiWGwiLCJpYXQiOjE2NTMzMDU0NjN9.kAoTO2gMaWpT9vuXiHVEO_9m22-e098pISQkN8gRdIU"
        self.zones = []
        self.polygon = None

    def get_air_zones(self, lat_min, lon_min, lat_max, lon_max):
        headers = {
            'X-API-Key': self.key,
        }
        response = requests.get('https://api.airmap.com/airspace/v2/search?geometry='
                                '%7B%22type%22:%22Polygon%22,%22coordinates%22:%5B%5B%5B'
                                + str(lon_min) + ',' + str(lat_min) + '%5D,%5B'
                                + str(lon_min) + ',' + str(lat_max) + '%5D,%5B'
                                + str(lon_max) + ',' + str(lat_max) + '%5D,%5B'
                                + str(lon_max) + ',' + str(lat_min) + '%5D,%5B'
                                + str(lon_min) + ',' + str(lat_min) +
                                '%5D%5D%5D%7D&types=airport,controlled_airspace,tfr,special_use_airspace,heliport&full=true&geometry_format=wkt',
                                headers=headers)
        print(response.json())

    def aviation_grade(self, landing_spot):
        if len(self.zones) == 0:
            landing_spot.aviation = 1
