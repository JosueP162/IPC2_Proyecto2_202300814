class Plant:
    def __init__(self, row, position, water_liters, fertilizer_grams, plant_type):
        self.row = row
        self.position = position
        self.water_liters = water_liters
        self.fertilizer_grams = fertilizer_grams
        self.plant_type = plant_type
        self.irrigated = False
    
    def get_location_id(self):
        """Retorna H1-P2 format"""
        return f"H{self.row}-P{self.position}"
