class LogEntry:
    def __init__(self, type, timestamp):
        self.type = type
        self.timestamp = timestamp

    def get_type(self):
        return self.type

    def get_timestamp(self):
        return self.timestamp
