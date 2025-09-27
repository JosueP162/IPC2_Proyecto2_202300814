from data_structures.simple_list import SimpleList

class Configuration:
    def __init__(self):
        self.all_drones = SimpleList()  # Todos los drones disponibles
        self.greenhouses = SimpleList()  # Todos los invernaderos
    
    def add_drone(self, drone):
        self.all_drones.add(drone)
    
    def add_greenhouse(self, greenhouse):
        self.greenhouses.add(greenhouse)
    
    def get_drone_by_id(self, drone_id):
        """Buscar dron por ID"""
        for i in range(self.all_drones.get_size()):
            drone = self.all_drones.get(i)
            if drone.id == drone_id:
                return drone
        return None
    
    def get_greenhouse_by_name(self, name):
        """Buscar invernadero por nombre"""
        for i in range(self.greenhouses.get_size()):
            greenhouse = self.greenhouses.get(i)
            if greenhouse.name == name:
                return greenhouse
        return None