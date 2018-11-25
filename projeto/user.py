class User:
    def __init__(self, new_id, new_latitude, new_longitude):
        self.id = new_id
        self.latitude = new_latitude
        self.longitude = new_longitude

    def get_id(self):
        return self.id

    def get_position(self):
        return [self.latitude, self.longitude]

    def set_position(self, new_latitude, new_longitude):
        self.latitude = new_latitude
        self.longitude = new_longitude
        return 1



