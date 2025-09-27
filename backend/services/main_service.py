from utils.xml_parser import XMLParser
from services.simulator import DiscreteSimulator
from utils.xml_generator import XMLGenerator

class IrrigationSystemService:
    """Servicio principal que coordina todo el sistema"""
    
    def __init__(self):
        self.parser = XMLParser()
        self.xml_generator = XMLGenerator()
        self.current_configuration = None
        self.simulation_results = {}  # Resultados por invernadero y plan
    
    def load_configuration(self, xml_file_path):
        """Cargar configuración desde archivo XML"""
        print(f"Cargando configuración desde: {xml_file_path}")
        
        self.current_configuration = self.parser.parse_configuration_file(xml_file_path)
        
        if self.current_configuration:
            print("✅ Configuración cargada exitosamente")
            self._print_configuration_summary()
            return True
        else:
            print("❌ Error al cargar configuración")
            return False
    
    def simulate_greenhouse_plan(self, greenhouse_name, plan_name):
        """Simular un plan específico de un invernadero"""
        if not self.current_configuration:
            print("❌ No hay configuración cargada")
            return None
        
        # Buscar invernadero
        greenhouse = self.current_configuration.get_greenhouse_by_name(greenhouse_name)
        if not greenhouse:
            print(f"❌ Invernadero '{greenhouse_name}' no encontrado")
            return None
        
        # Buscar plan
        irrigation_plan = self._find_plan_in_greenhouse(greenhouse, plan_name)
        if not irrigation_plan:
            print(f"❌ Plan '{plan_name}' no encontrado en '{greenhouse_name}'")
            return None
        
        print(f"🚀 Iniciando simulación: {greenhouse_name} - {plan_name}")
        
        # Crear simulador
        simulator = DiscreteSimulator(greenhouse)
        
        # Ejecutar simulación
        result = simulator.simulate_plan(irrigation_plan)
        
        # Guardar resultado
        key = f"{greenhouse_name}_{plan_name}"
        self.simulation_results[key] = result
        
        print(" Simulación completada")
        self._print_simulation_summary(result)
        
        return result
    
    def simulate_all_plans(self):
        """Simular todos los planes de todos los invernaderos"""
        if not self.current_configuration:
            print("❌ No hay configuración cargada")
            return
        
        print("Simulando todos los planes...")
        
        total_simulations = 0
        
        # Para cada invernadero
        for i in range(self.current_configuration.greenhouses.get_size()):
            greenhouse = self.current_configuration.greenhouses.get(i)
            
            print(f"\n📍 Procesando invernadero: {greenhouse.name}")
            
            # Para cada plan del invernadero
            for j in range(greenhouse.irrigation_plans.get_size()):
                irrigation_plan = greenhouse.irrigation_plans.get(j)
                
                result = self.simulate_greenhouse_plan(greenhouse.name, irrigation_plan.name)
                if result:
                    total_simulations += 1
        
        print(f"\n Completadas {total_simulations} simulaciones")
    
    def generate_output_file(self, output_path="salida.xml"):
        """Generar archivo XML de salida con todos los resultados"""
        if not self.current_configuration:
            print(" No hay configuración cargada")
            return False
        
        if not self.simulation_results:
            print(" No hay resultados de simulación")
            return False
        
        print(f" Generando archivo de salida: {output_path}")
        
        try:
            # Generar XML de salida
            self.xml_generator.generate_output_xml(
                self.current_configuration, 
                self.simulation_results, 
                output_path
            )
            
            print(" Archivo de salida generado exitosamente")
            return True
            
        except Exception as e:
            print(f" Error generando archivo de salida: {e}")
            return False
    
    def get_available_greenhouses(self):
        """Obtener lista de invernaderos disponibles"""
        if not self.current_configuration:
            return []
        
        greenhouses = []
        for i in range(self.current_configuration.greenhouses.get_size()):
            greenhouse = self.current_configuration.greenhouses.get(i)
            greenhouses.append(greenhouse.name)
        
        return greenhouses
    
    def get_available_plans(self, greenhouse_name):
        """Obtener planes disponibles para un invernadero"""
        if not self.current_configuration:
            return []
        
        greenhouse = self.current_configuration.get_greenhouse_by_name(greenhouse_name)
        if not greenhouse:
            return []
        
        plans = []
        for i in range(greenhouse.irrigation_plans.get_size()):
            plan = greenhouse.irrigation_plans.get(i)
            plans.append(plan.name)
        
        return plans
    
    def get_simulation_result(self, greenhouse_name, plan_name):
        """Obtener resultado de simulación específico"""
        key = f"{greenhouse_name}_{plan_name}"
        return self.simulation_results.get(key)
    
    def _find_plan_in_greenhouse(self, greenhouse, plan_name):
        """Buscar plan específico en un invernadero"""
        for i in range(greenhouse.irrigation_plans.get_size()):
            plan = greenhouse.irrigation_plans.get(i)
            if plan.name == plan_name:
                return plan
        return None
    
    def _print_configuration_summary(self):
        """Imprimir resumen de configuración cargada"""
        print("\n=== RESUMEN DE CONFIGURACIÓN ===")
        
        print(f" Drones disponibles: {self.current_configuration.all_drones.get_size()}")
        for i in range(self.current_configuration.all_drones.get_size()):
            drone = self.current_configuration.all_drones.get(i)
            print(f"   - {drone.name} (ID: {drone.id})")
        
        print(f"\n Invernaderos: {self.current_configuration.greenhouses.get_size()}")
        for i in range(self.current_configuration.greenhouses.get_size()):
            greenhouse = self.current_configuration.greenhouses.get(i)
            print(f"   - {greenhouse.name}")
            print(f"     Dimensiones: {greenhouse.num_rows}x{greenhouse.plants_per_row}")
            print(f"     Plantas: {greenhouse.plants.get_size()}")
            print(f"     Drones: {greenhouse.drones.get_size()}")
            print(f"     Planes: {greenhouse.irrigation_plans.get_size()}")
    
    def _print_simulation_summary(self, result):
        """Imprimir resumen de simulación"""
        print(f"   Tiempo total: {result.total_time} segundos")
        print(f"   Agua total: {result.total_water} litros")
        print(f"   Fertilizante total: {result.total_fertilizer} gramos")
        
        print("    Estadísticas por dron:")
        for i in range(result.drone_statistics.get_size()):
            stat = result.drone_statistics.get(i)
            print(f"      {stat.drone_name}: {stat.water_used}L, {stat.fertilizer_used}g")


# Función principal para testing
def main():
    """Función principal para probar el sistema completo"""
    service = IrrigationSystemService()
    
    # Cargar configuración
    if service.load_configuration("entrada.xml"):
        
        # Simular plan específico
        result = service.simulate_greenhouse_plan("Invernadero Zacapa", "Semana 1")
        
        if result:
            # Generar archivo de salida
            service.generate_output_file("salida.xml")

if __name__ == "__main__":
    main()