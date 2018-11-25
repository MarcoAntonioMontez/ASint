class Building:
    def __init__(self, new_id, new_name, toplevel_id, latitude, longitude, radius):
        self.id = new_id
        self.name = new_name
        self.toplevel_id = toplevel_id
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius

    def get_building(self):
        return self

    def set_building(self, new_id, new_name, toplevel_id, latitude, longitude, radius):
        if new_id is not None:
            self.id = new_id
        if new_name is not None:
            self.name = new_name
        if toplevel_id is not None:
            self.toplevel_id = toplevel_id
        if latitude is not None:
            self.latitude = latitude
        if longitude is not None:
            self.longitude = longitude
        if new_id is not None:
            self.radius = radius
        return 1


class Campus:
    def __init__(self, new_id, new_name):
        self.id = new_id
        self.name = new_name

    list_of_buildings = []

    def set_campus(self, new_id, new_name):
        self.id = new_id
        self.name = new_name
        return 1

    def add_building(self, building):
        for build in self.list_of_buildings:
            if build.id == building.id:
                build.set_building(build, building.id, building.name, building.toplevel_id, building.latitude,
                                   building.longitude, building.radius)
                return 1
        self.list_of_buildings.append(building)
        return 1

    def remove_building(self, building):
        self.list_of_buildings.remove(building)
        return 1