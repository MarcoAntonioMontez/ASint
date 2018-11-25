class Log:
    def __init__(self, new_type, new_timestamp):
        self.type = new_type
        self.timestamp = new_timestamp

    def get_type(self):
        return self.type

    def get_timestamp(self):
        return self.timestamp
