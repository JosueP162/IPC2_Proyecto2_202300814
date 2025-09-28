import sys
import os

# Agregar paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_structures'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from utils.xml_parser import XMLParser
from services.simulator import DiscreteSimulator
from data_structures.simple_list import SimpleList

# Clase para almacenar pares clave-valor usando TDAs propios
class KeyValuePair:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class SimulationResultsStorage:
    """Almacena resultados usando SimpleList en lugar de dict"""
    def __init__(self):
        self.results = SimpleList()  # Lista de KeyValuePair
    
    def add_result(self, greenhouse_name, plan_name, result):
        key = f"{greenhouse_name}_{plan_name}"
        pair = KeyValuePair(key, result)
        self.results.add(pair)
    
    def get_result(self, greenhouse_name, plan_name):
        key = f"{greenhouse_name}_{plan_name}"
        for i in range(self.results.get_size()):
            pair = self.results.get(i)
            if pair.key == key:
                return pair.value
        return None
    
    def has_results(self):
        return not self.results.is_empty()
    
    def clear(self):
        self.results = SimpleList()
    
    def get_all_results(self):
        """Retorna SimpleList de todos los resultados"""
        all_results = SimpleList()
        for i in range(self.results.get_size()):
            pair = self.results.get(i)
            all_results.add(pair)
        return all_results

class GreenhouseInfo:
    """Info de invernadero para frontend usando TDAs"""
    def __init__(self, name, rows, plants_per_row, total_plants, drones_count):
        self.name = name
        self.rows = rows
        self.plants_per_row = plants_per_row
        self.total_plants = total_plants
        self.drones_count = drones_count
        self.plans = SimpleList()  # Lista de PlanInfo

class PlanInfo:
    """Info de plan para frontend"""
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence

class CompleteIrrigationService:
    """Servicio principal usando solo TDAs propios"""
    
    def __init__(self):
        self.xml_parser = XMLParser()
        self.current_configuration = None
        self.simulation_results = SimulationResultsStorage()
    
    def generate_tda_graph(self, greenhouse_name, plan_name, time_t):
        """Generar gráfico Graphviz para un plan simulado"""
        try:
            result = self.get_simulation_result(greenhouse_name, plan_name)
            if not result:
                return None
            
            # Importar el generador de gráficos
            from utils.graphviz_generator import GraphvizTDAGenerator
            
            generator = GraphvizTDAGenerator()
            output_dir = "graphs"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generar nombre de archivo único
            filename_base = f"tda_{greenhouse_name}_{plan_name}_t{time_t}"
            filename_base = filename_base.replace(" ", "_").replace("/", "_")
            output_path = os.path.join(output_dir, f"{filename_base}.dot")
            
            # Generar el gráfico
            png_path, dot_path = generator.generate_tda_graph(result, time_t, output_path)
            
            return png_path or dot_path  # Retornar PNG si existe, sino DOT
            
        except Exception as e:
            print(f"Error generando gráfico TDA: {e}")
            return None

    def load_configuration_file(self, xml_file_path):
        """Cargar configuración desde archivo XML"""
        try:
            self.current_configuration = self.xml_parser.parse_configuration_file(xml_file_path)
            if self.current_configuration:
                self.simulation_results.clear()
                return True
            return False
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return False
    
    def get_available_greenhouses(self):
        """Obtener lista de invernaderos usando TDAs"""
        if not self.current_configuration:
            return SimpleList()
        
        greenhouses_list = SimpleList()
        
        for i in range(self.current_configuration.greenhouses.get_size()):
            greenhouse = self.current_configuration.greenhouses.get(i)
            
            # Crear info del invernadero
            greenhouse_info = GreenhouseInfo(
                greenhouse.name,
                greenhouse.num_rows,
                greenhouse.plants_per_row,
                greenhouse.plants.get_size(),
                greenhouse.drones.get_size()
            )
            
            # Agregar planes
            for j in range(greenhouse.irrigation_plans.get_size()):
                plan = greenhouse.irrigation_plans.get(j)
                plan_info = PlanInfo(plan.name, plan.plan_string)
                greenhouse_info.plans.add(plan_info)
            
            greenhouses_list.add(greenhouse_info)
        
        return greenhouses_list
    
    def simulate_specific_plan(self, greenhouse_name, plan_name):
        """Simular plan específico"""
        if not self.current_configuration:
            return None
        
        # Buscar invernadero
        greenhouse = self.current_configuration.get_greenhouse_by_name(greenhouse_name)
        if not greenhouse:
            return None
        
        # Buscar plan
        target_plan = None
        for i in range(greenhouse.irrigation_plans.get_size()):
            plan = greenhouse.irrigation_plans.get(i)
            if plan.name == plan_name:
                target_plan = plan
                break
        
        if not target_plan:
            return None
        
        try:
            # Ejecutar simulación
            simulator = DiscreteSimulator(greenhouse)
            result = simulator.simulate_plan(target_plan)
            
            # Guardar resultado usando TDA propio
            self.simulation_results.add_result(greenhouse_name, plan_name, result)
            
            return result
        except Exception as e:
            print(f"Error en simulación: {e}")
            return None
    
    def simulate_all_plans(self):
        """Simular todos los planes usando TDAs"""
        if not self.current_configuration:
            return False
        
        try:
            for i in range(self.current_configuration.greenhouses.get_size()):
                greenhouse = self.current_configuration.greenhouses.get(i)
                
                for j in range(greenhouse.irrigation_plans.get_size()):
                    plan = greenhouse.irrigation_plans.get(j)
                    self.simulate_specific_plan(greenhouse.name, plan.name)
            
            return True
        except Exception as e:
            print(f"Error simulando todos los planes: {e}")
            return False
    
    def generate_xml_output(self, output_path="salida.xml"):
        """Generar XML usando solo TDAs"""
        if not self.current_configuration or not self.simulation_results.has_results():
            return False
        
        try:
            # Generar XML manualmente sin usar dict
            xml_content = '<?xml version="1.0"?>\n<datosSalida>\n  <listaInvernaderos>\n'
            
            for i in range(self.current_configuration.greenhouses.get_size()):
                greenhouse = self.current_configuration.greenhouses.get(i)
                xml_content += f'    <invernadero nombre="{greenhouse.name}">\n'
                xml_content += '      <listaPlanes>\n'
                
                for j in range(greenhouse.irrigation_plans.get_size()):
                    plan = greenhouse.irrigation_plans.get(j)
                    result = self.simulation_results.get_result(greenhouse.name, plan.name)
                    
                    if result:
                        xml_content += self._generate_plan_xml(plan, result)
                
                xml_content += '      </listaPlanes>\n    </invernadero>\n'
            
            xml_content += '  </listaInvernaderos>\n</datosSalida>'
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            return True
        except Exception as e:
            print(f"Error generando XML: {e}")
            return False
    
    def _generate_plan_xml(self, plan, result):
        """Generar XML para un plan específico"""
        xml = f'        <plan nombre="{plan.name}">\n'
        xml += f'          <tiempoOptimoSegundos> {result.total_time} </tiempoOptimoSegundos>\n'
        xml += f'          <aguaRequeridaLitros> {int(result.total_water)} </aguaRequeridaLitros>\n'
        xml += f'          <fertilizanteRequeridoGramos> {int(result.total_fertilizer)} </fertilizanteRequeridoGramos>\n'
        
        # Eficiencia de drones
        xml += '          <eficienciaDronesRegadores>\n'
        for i in range(result.drone_statistics.get_size()):
            stat = result.drone_statistics.get(i)
            xml += f'            <dron nombre="{stat.drone_name}" litrosAgua="{int(stat.water_used)}" gramosFertilizante="{int(stat.fertilizer_used)}"/>\n'
        xml += '          </eficienciaDronesRegadores>\n'
        
        # Instrucciones
        xml += '          <instrucciones>\n'
        max_seconds = result.timeline.get_max_seconds()
        
        for second in range(1, max_seconds + 1):
            actions = result.timeline.get_actions_at_second(second)
            if not actions.is_empty():
                xml += f'            <tiempo segundos="{second}">\n'
                for k in range(actions.get_size()):
                    action = actions.get(k)
                    xml += f'              <dron nombre="{action.drone_name}" accion="{action.description}"/>\n'
                xml += '            </tiempo>\n'
        
        xml += '          </instrucciones>\n        </plan>\n'
        return xml
    
    def get_simulation_result(self, greenhouse_name, plan_name):
        """Obtener resultado específico"""
        return self.simulation_results.get_result(greenhouse_name, plan_name)
    
    def has_simulation_results(self):
        """Verificar si hay resultados"""
        return self.simulation_results.has_results()
    
    def count_total_simulations(self):
        """Contar total de simulaciones"""
        return self.simulation_results.results.get_size()
    
    def calculate_statistics(self):
        """Calcular estadísticas generales usando TDAs"""
        if not self.simulation_results.has_results():
            return None
        
        total_time = 0
        total_water = 0
        total_fertilizer = 0
        count = 0
        
        all_results = self.simulation_results.get_all_results()
        for i in range(all_results.get_size()):
            pair = all_results.get(i)
            result = pair.value
            total_time += result.total_time
            total_water += result.total_water
            total_fertilizer += result.total_fertilizer
            count += 1
        
        return {
            'total_simulations': count,
            'average_time': total_time / count if count > 0 else 0,
            'total_water': total_water,
            'total_fertilizer': total_fertilizer
        }