class Message:
    #User radius is optional in constructed
    #If a radius is not given, its default value is 0
    def __init__(self, dict):
        self.id = dict['id']
        self.message = dict['message']
        self.radius = float(dict['radius'])
        self.latitude = float(dict['latitude'])
        self.longitude = float(dict['longitude'])

    def __repr__(self):
        return ("\nid: " + str(self.id) + "\nmessage: " + str(self.message) + "\nradius: " + \
                str(self.radius) + "\nlatitude: " + str(self.latitude) + "\nlongitude: " + \
                str(self.longitude) + "\n")

    def get_dict(self):
        dict = {
            'id': self.id,
            'message': self.message,
            'radius': self.radius,
            'latitude': self.latitude,
            'longitude': self.longitude
            }
        return dict