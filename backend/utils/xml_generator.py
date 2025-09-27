import xml.etree.ElementTree as ET
from xml.dom import minidom

class XMLGenerator:
    def __init__(self):
        pass
    
    def generate_output_xml(self, configuration, simulation_results, output_path="salida.xml"):
        """Generar archivo XML de salida con todos los resultados"""
        
        # Crear elemento raíz
        root = ET.Element("datosSalida")
        
        # Crear lista de invernaderos
        greenhouses_list = ET.SubElement(root, "listaInvernaderos")
        
        # Procesar cada invernadero
        for i in range(configuration.greenhouses.get_size()):
            greenhouse = configuration.greenhouses.get(i)
            greenhouse_elem = ET.SubElement(greenhouses_list, "invernadero")
            greenhouse_elem.set("nombre", greenhouse.name)
            
            # Lista de planes para este invernadero
            plans_list = ET.SubElement(greenhouse_elem, "listaPlanes")
            
            # Procesar cada plan del invernadero
            for j in range(greenhouse.irrigation_plans.get_size()):
                irrigation_plan = greenhouse.irrigation_plans.get(j)
                
                # Buscar resultado de simulación para este plan
                result = self._find_simulation_result(simulation_results, greenhouse.name, irrigation_plan.name)
                
                if result:
                    plan_elem = self._create_plan_element(plans_list, irrigation_plan, result)
        
        # Escribir archivo
        self._write_xml_file(root, output_path)
        return output_path
    
    def _find_simulation_result(self, simulation_results, greenhouse_name, plan_name):
        """Buscar resultado de simulación específico"""
        # simulation_results debería ser un diccionario o estructura que contenga
        # los resultados organizados por invernadero y plan
        # Por ahora, asumimos que recibimos el resultado directamente
        return simulation_results
    
    def _create_plan_element(self, parent, irrigation_plan, simulation_result):
        """Crear elemento XML para un plan específico"""
        plan_elem = ET.SubElement(parent, "plan")
        plan_elem.set("nombre", irrigation_plan.name)
        
        # Tiempo óptimo
        time_elem = ET.SubElement(plan_elem, "tiempoOptimoSegundos")
        time_elem.text = f" {simulation_result.total_time} "
        
        # Agua requerida
        water_elem = ET.SubElement(plan_elem, "aguaRequeridaLitros")
        water_elem.text = f" {simulation_result.total_water} "
        
        # Fertilizante requerido
        fertilizer_elem = ET.SubElement(plan_elem, "fertilizanteRequeridoGramos")
        fertilizer_elem.text = f" {simulation_result.total_fertilizer} "
        
        # Eficiencia de drones
        self._create_drone_efficiency_element(plan_elem, simulation_result)
        
        # Instrucciones detalladas
        self._create_instructions_element(plan_elem, simulation_result)
        
        return plan_elem
    
    def _create_drone_efficiency_element(self, parent, simulation_result):
        """Crear elemento de eficiencia de drones"""
        efficiency_elem = ET.SubElement(parent, "eficienciaDronesRegadores")
        
        # Para cada dron con estadísticas
        for i in range(simulation_result.drone_statistics.get_size()):
            drone_stat = simulation_result.drone_statistics.get(i)
            
            drone_elem = ET.SubElement(efficiency_elem, "dron")
            drone_elem.set("nombre", drone_stat.drone_name)
            drone_elem.set("litrosAgua", str(int(drone_stat.water_used)))
            drone_elem.set("gramosFertilizante", str(int(drone_stat.fertilizer_used)))
    
    def _create_instructions_element(self, parent, simulation_result):
        """Crear elemento de instrucciones detalladas"""
        instructions_elem = ET.SubElement(parent, "instrucciones")
        
        # Para cada segundo en el timeline
        max_seconds = simulation_result.timeline.get_max_seconds()
        
        for second in range(1, max_seconds + 1):
            actions = simulation_result.timeline.get_actions_at_second(second)
            
            if not actions.is_empty():
                time_elem = ET.SubElement(instructions_elem, "tiempo")
                time_elem.set("segundos", str(second))
                
                # Para cada acción en este segundo
                for i in range(actions.get_size()):
                    action = actions.get(i)
                    
                    drone_elem = ET.SubElement(time_elem, "dron")
                    drone_elem.set("nombre", action.drone_name)
                    drone_elem.set("accion", action.description)
    
    def _write_xml_file(self, root, output_path):
        """Escribir archivo XML con formato legible"""
        # Convertir a string
        rough_string = ET.tostring(root, 'unicode')
        
        # Formatear para que sea legible
        reparsed = minidom.parseString(rough_string)
        formatted_xml = reparsed.toprettyxml(indent="  ")
        
        # Escribir archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_xml)
        
        print(f"Archivo XML generado: {output_path}")


# Función de utilidad para testing
def test_xml_generation():
    """Función de prueba para generación XML"""
    from ..services.simulator import SimulationResult, DroneStatistics
    from ..data_structures.simple_list import SimpleList
    
    # Crear resultado simulado para prueba
    result = SimulationResult()
    result.total_time = 8
    result.total_water = 5
    result.total_fertilizer = 500
    
    # Estadísticas de drones simuladas
    drone_stats = SimpleList()
    
    stat1 = DroneStatistics("DR01")
    stat1.water_used = 2
    stat1.fertilizer_used = 200
    drone_stats.add(stat1)
    
    stat2 = DroneStatistics("DR02") 
    stat2.water_used = 2
    stat2.fertilizer_used = 200
    drone_stats.add(stat2)
    
    stat3 = DroneStatistics("DR03")
    stat3.water_used = 1
    stat3.fertilizer_used = 100
    drone_stats.add(stat3)
    
    result.drone_statistics = drone_stats
    
    # Generar XML
    generator = XMLGenerator()
    # generator.generate_output_xml(None, result, "test_salida.xml")

# if __name__ == "__main__":
#     test_xml_generation()