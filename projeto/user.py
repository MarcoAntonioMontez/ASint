class User:
    #User radius is optional in constructed
    #If a radius is not given, its default value is 0
    def __init__(self, new_id, new_latitude, new_longitude,radius=0):
        self.id = new_id
        self.latitude = float(new_latitude)
        self.longitude = float(new_longitude)
        self.radius=float(radius)

    def get_id(self):
        return self.id

    def radius(self):
        return self.radius

    def get_position(self):
        return [self.latitude, self.longitude]

    def set_position(self, new_latitude, new_longitude):
        self.latitude = float(new_latitude)
        self.longitude = float(new_longitude)
        return 1

    def __repr__(self):
        return ("\nid: " + str(self.id) + "\nlatitude: " + str(self.latitude) + "\nlongitude: " + \
                str(self.longitude) + "\nradius: " + str(self.radius) + "\n")

    def get_dict(self):
        dict = {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude
            }
        return dict

