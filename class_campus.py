from class_builds import Building

class Campus:
    def __init__(self,new_type, new_id, new_name):
        self.type = new_type
        self.id = new_id
        self.name = new_name

    list_of_buildings = []

    def set_campus(self, new_id, new_name):
        self.id = new_id
        self.name = new_name
        return 1

    def reset_buildings(self):
        self.list_of_buildings=[]
        return

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

    def __repr__(self):
        build_str=""
        for build in self.list_of_buildings:
            build_str=build_str + build.__repr__()

        return "\n#############\n#############" + "\nType: " + str(self.type) + "\n Id: " + str(self.id) + "\n Name: " \
               + str(self.name) + "\nList of buildings:\n " + build_str + "\n-----"