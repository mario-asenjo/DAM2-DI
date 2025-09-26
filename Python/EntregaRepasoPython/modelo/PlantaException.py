class PlantaException(Exception):
    def __init__(self, message):
        super().__init__("Error: " + message)