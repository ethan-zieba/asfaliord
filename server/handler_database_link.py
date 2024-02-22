class DatabaseRequest:
    def __init__(self, type):
        type = type.lower() if type.lower() in ["get", "set", "flush"] else None