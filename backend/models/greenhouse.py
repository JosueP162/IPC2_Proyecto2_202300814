from data_structures.simple_list import SimpleList

class Greenhouse:
    def __init__(self, name, num_rows, plants_per_row):
        self.name = name
        self.num_rows = num_rows
        self.plants_per_row = plants_per_row
        self.plants = SimpleList()  # Lista de plantas
        self.drones = SimpleList()  # Lista de drones asignados
        self.irrigation_plans = SimpleList()  # Lista de planes de riego
    
    def add_plant(self, plant):
        self.plants.add(plant)
    
    def add_drone(self, drone):
        self.drones.add(drone)
    
    def add_irrigation_plan(self, plan):
        self.irrigation_plans.add(plan)
    
    def get_plant_at(self, row, position):
        """Encontrar planta en posición específica"""
        for i in range(self.plants.get_size()):
            plant = self.plants.get(i)
            if plant.row == row and plant.position == position:
                return plant
        return None
    
    def get_drone_for_row(self, row):
        """Obtener dron asignado a una hilera"""
        for i in range(self.drones.get_size()):
            drone = self.drones.get(i)
            if drone.assigned_row == row:
                return drone
        return None
