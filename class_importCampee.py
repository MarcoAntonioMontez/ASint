from class_campus import Campus
from class_builds import Building
import urllib3
import json

class ImportCampee:
    campeeList = []

    def __init__(self,campeeUrls):
        self.campeeUrls = campeeUrls

    def jsonToBuilding(self,data):
        new_id = data['id']
        new_name = data['name'].encode('utf-8')
        toplevel_id = data['topLevelSpace']['id']
        latitude = 0
        longitude = 0
        radius = 0
        b = Building(new_id, new_name, toplevel_id, latitude, longitude, radius)
        return b

    def jsonToCampus(self,data):
        type = data['type']
        id = data['id']
        name = data['name'].encode('utf-8')
        campus = Campus(type, id, name)
        return campus

    def get_campee(self):
        self.campeeList = []
        http = urllib3.PoolManager()
        for url in self.campeeUrls:
            request = http.request('GET', url)
            data = json.loads(request.data.decode("utf-8"))

            newCampus = self.jsonToCampus(data)
            newCampus.reset_buildings()

            buildings = data['containedSpaces']
            for building in buildings:
                new_building = self.jsonToBuilding(building)
                newCampus.add_building(new_building)
            self.campeeList.append(newCampus)
        return self.campeeList

