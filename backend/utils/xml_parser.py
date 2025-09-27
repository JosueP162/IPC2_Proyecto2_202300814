import xml.etree.ElementTree as ET

# Asegúrate de que estos imports sean absolutos:
from models.drone import Drone
from models.plant import Plant
from models.greenhouse import Greenhouse
from models.irrigation_plan import IrrigationPlan  # ← Este usa la Queue corregida
from models.configuration import Configuration

class XMLParser:
    def __init__(self):
        pass
    
    def parse_configuration_file(self, xml_file_path):
        """Parsear archivo XML completo y retornar Configuration"""
        try:
            # Parsear XML
            tree = ET.parse(xml_file_path)
            root = tree.getroot()
            
            # Crear configuración
            config = Configuration()
            
            # Parsear drones
            self._parse_drones(root, config)
            
            # Parsear invernaderos
            self._parse_greenhouses(root, config)
            
            return config
            
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return None
    
    def _parse_drones(self, root, config):
        """Parsear lista de drones disponibles"""
        drones_list = root.find('listaDrones')
        
        if drones_list is not None:
            for drone_elem in drones_list.findall('dron'):
                drone_id = int(drone_elem.get('id'))
                drone_name = drone_elem.get('nombre')
                
                drone = Drone(drone_id, drone_name)
                config.add_drone(drone)
    
    def _parse_greenhouses(self, root, config):
        """Parsear lista de invernaderos"""
        greenhouses_list = root.find('listaInvernaderos')
        
        if greenhouses_list is not None:
            for greenhouse_elem in greenhouses_list.findall('invernadero'):
                greenhouse = self._parse_single_greenhouse(greenhouse_elem, config)
                config.add_greenhouse(greenhouse)
    
    def _parse_single_greenhouse(self, greenhouse_elem, config):
        """Parsear un invernadero individual"""
        # Información básica
        name = greenhouse_elem.get('nombre')
        num_rows = int(greenhouse_elem.find('numeroHileras').text.strip())
        plants_per_row = int(greenhouse_elem.find('plantasXhilera').text.strip())
        
        # Crear invernadero
        greenhouse = Greenhouse(name, num_rows, plants_per_row)
        
        # Parsear plantas
        self._parse_plants(greenhouse_elem, greenhouse)
        
        # Parsear asignación de drones
        self._parse_drone_assignments(greenhouse_elem, greenhouse, config)
        
        # Parsear planes de riego
        self._parse_irrigation_plans(greenhouse_elem, greenhouse)
        
        return greenhouse
    
    def _parse_plants(self, greenhouse_elem, greenhouse):
        """Parsear lista de plantas"""
        plants_list = greenhouse_elem.find('listaPlantas')
        
        if plants_list is not None:
            for plant_elem in plants_list.findall('planta'):
                row = int(plant_elem.get('hilera'))
                position = int(plant_elem.get('posicion'))
                water_liters = float(plant_elem.get('litrosAgua'))
                fertilizer_grams = float(plant_elem.get('gramosFertilizante'))
                plant_type = plant_elem.text.strip() if plant_elem.text else ""
                
                plant = Plant(row, position, water_liters, fertilizer_grams, plant_type)
                greenhouse.add_plant(plant)
    
    def _parse_drone_assignments(self, greenhouse_elem, greenhouse, config):
        """Parsear asignación de drones a hileras"""
        assignments = greenhouse_elem.find('asignacionDrones')
        
        if assignments is not None:
            for assignment in assignments.findall('dron'):
                drone_id = int(assignment.get('id'))
                assigned_row = int(assignment.get('hilera'))
                
                # Buscar dron en configuración global
                drone = config.get_drone_by_id(drone_id)
                
                if drone:
                    # Asignar hilera
                    drone.assign_to_row(assigned_row)
                    # Agregar al invernadero
                    greenhouse.add_drone(drone)
    
    def _parse_irrigation_plans(self, greenhouse_elem, greenhouse):
        """Parsear planes de riego"""
        plans_elem = greenhouse_elem.find('planesRiego')
        
        if plans_elem is not None:
            for plan_elem in plans_elem.findall('plan'):
                plan_name = plan_elem.get('nombre')
                plan_string = plan_elem.text.strip() if plan_elem.text else ""
                
                irrigation_plan = IrrigationPlan(plan_name, plan_string)
                greenhouse.add_irrigation_plan(irrigation_plan)


# Ejemplo de uso:
def test_parser():
    """Función de prueba para el parser"""
    parser = XMLParser()
    config = parser.parse_configuration_file('entrada.xml')
    
    if config:
        print("=== CONFIGURACIÓN CARGADA ===")
        
        # Mostrar drones
        print(f"Drones disponibles: {config.all_drones.get_size()}")
        for i in range(config.all_drones.get_size()):
            drone = config.all_drones.get(i)
            print(f"  - {drone.name} (ID: {drone.id})")
        
        # Mostrar invernaderos
        print(f"\nInvernaderos: {config.greenhouses.get_size()}")
        for i in range(config.greenhouses.get_size()):
            greenhouse = config.greenhouses.get(i)
            print(f"  - {greenhouse.name}")
            print(f"    Hileras: {greenhouse.num_rows}, Plantas/hilera: {greenhouse.plants_per_row}")
            print(f"    Plantas: {greenhouse.plants.get_size()}")
            print(f"    Drones asignados: {greenhouse.drones.get_size()}")
            print(f"    Planes de riego: {greenhouse.irrigation_plans.get_size()}")
            
            # Mostrar planes
            for j in range(greenhouse.irrigation_plans.get_size()):
                plan = greenhouse.irrigation_plans.get(j)
                print(f"      Plan '{plan.name}': {plan.plan_string}")

# if __name__ == "__main__":
#     test_parser()