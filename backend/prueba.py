# prueba.py - Prueba del sistema completo (CORREGIDO)
import sys
import os

# Agregar el directorio backend al path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_xml():
    """Crear archivo XML de prueba"""
    xml_content = """<?xml version="1.0"?>
<configuracion>
<listaDrones>
<dron id="1" nombre="DR01"/>
<dron id="2" nombre="DR02"/>
<dron id="3" nombre="DR03"/>
<dron id="4" nombre="DR04"/>
</listaDrones>
<listaInvernaderos>
<invernadero nombre="Invernadero San Marcos">
<numeroHileras>4</numeroHileras>
<plantasXhilera>3</plantasXhilera>
<listaPlantas>
<planta hilera="1" posicion="1" litrosAgua="3" gramosFertilizante="200">matilisguate</planta>
<planta hilera="1" posicion="2" litrosAgua="4" gramosFertilizante="100">ciprés</planta>
<planta hilera="1" posicion="3" litrosAgua="3" gramosFertilizante="200">matilisguate</planta>
<planta hilera="2" posicion="1" litrosAgua="1" gramosFertilizante="25">ciprés italiano</planta>
<planta hilera="2" posicion="2" litrosAgua="2" gramosFertilizante="125">ciprés de tarout</planta>
<planta hilera="2" posicion="3" litrosAgua="1" gramosFertilizante="25">ciprés italiano</planta>
<planta hilera="3" posicion="1" litrosAgua="3" gramosFertilizante="200">matilisguate</planta>
<planta hilera="3" posicion="2" litrosAgua="4" gramosFertilizante="100">ciprés</planta>
<planta hilera="3" posicion="3" litrosAgua="3" gramosFertilizante="200">matilisguate</planta>
<planta hilera="4" posicion="1" litrosAgua="1" gramosFertilizante="25">ciprés italiano</planta>
<planta hilera="4" posicion="2" litrosAgua="2" gramosFertilizante="125">ciprés de tarout</planta>
<planta hilera="4" posicion="3" litrosAgua="1" gramosFertilizante="25">ciprés italiano</planta>
</listaPlantas>
<asignacionDrones>
<dron id="1" hilera="1"/>
<dron id="2" hilera="2"/>
<dron id="3" hilera="3"/>
<dron id="4" hilera="4"/>
</asignacionDrones>
<planesRiego>
<plan nombre="Dia 1">H4-P1, H3-P2, H2-P3, H1-P3</plan>
<plan nombre="Dia 2">H1-P2, H4-P2, H2-P3, H3-P3, H2-P1, H3-P1</plan>
<plan nombre="Dia 3">H2-P1, H4-P1, H1-P2, H3-P2, H2-P2, H4-P2, H1-P2, H3-P2, H2-P3, H4-P3</plan>
</planesRiego>
</invernadero>
<invernadero nombre="Invernadero Guatemala">
<numeroHileras>2</numeroHileras>
<plantasXhilera>10</plantasXhilera>
<listaPlantas>
<planta hilera="1" posicion="1" litrosAgua="7" gramosFertilizante="75">pino</planta>
<planta hilera="1" posicion="2" litrosAgua="5" gramosFertilizante="50">ciprés italiano</planta>
<planta hilera="1" posicion="3" litrosAgua="2" gramosFertilizante="25">ciprés de tarout</planta>
<planta hilera="1" posicion="4" litrosAgua="7" gramosFertilizante="75">pino</planta>
<planta hilera="1" posicion="5" litrosAgua="5" gramosFertilizante="50">ciprés italiano</planta>
<planta hilera="1" posicion="6" litrosAgua="2" gramosFertilizante="25">ciprés de tarout</planta>
<planta hilera="1" posicion="7" litrosAgua="7" gramosFertilizante="75">pino</planta>
<planta hilera="1" posicion="8" litrosAgua="5" gramosFertilizante="50">ciprés italiano</planta>
<planta hilera="1" posicion="9" litrosAgua="2" gramosFertilizante="25">ciprés de tarout</planta>
<planta hilera="1" posicion="10" litrosAgua="7" gramosFertilizante="75">pino</planta>
<planta hilera="2" posicion="1" litrosAgua="2" gramosFertilizante="100">limón</planta>
<planta hilera="2" posicion="2" litrosAgua="1" gramosFertilizante="200">naranja</planta>
<planta hilera="2" posicion="3" litrosAgua="2" gramosFertilizante="100">limón</planta>
<planta hilera="2" posicion="4" litrosAgua="1" gramosFertilizante="200">naranja</planta>
<planta hilera="2" posicion="5" litrosAgua="2" gramosFertilizante="100">limón</planta>
<planta hilera="2" posicion="6" litrosAgua="1" gramosFertilizante="200">naranja</planta>
<planta hilera="2" posicion="7" litrosAgua="2" gramosFertilizante="100">limón</planta>
<planta hilera="2" posicion="8" litrosAgua="1" gramosFertilizante="200">naranja</planta>
<planta hilera="2" posicion="9" litrosAgua="2" gramosFertilizante="100">limón</planta>
<planta hilera="2" posicion="10" litrosAgua="1" gramosFertilizante="200">naranja</planta>
</listaPlantas>
<asignacionDrones>
<dron id="2" hilera="1"/>
<dron id="4" hilera="2"/>
</asignacionDrones>
<planesRiego>
<plan nombre="Final"> H1-P1, H2-P1, H1-P2, H2-P2, H1-P3, H2-P3, H1-P4, H2-P4, H1-P5, H2-P5, H1-P6, H2-P6, H1-P7, H2-P7, H1-P8, H2-P8, H1-P9, H2-P9, H1-P10, H2-P10 </plan>
</planesRiego>
</invernadero>
</listaInvernaderos>
</configuracion> """
    
    with open('entrada_test.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(" Archivo de prueba creado: entrada_test.xml")


def test_data_structures():
    """Probar TDAs individuales"""
    try:
        from data_structures.simple_list import SimpleList
        from data_structures.queue import Queue
        from data_structures.list_of_lists import ListOfLists
        
        print(" === PRUEBA DE TDAs ===\n")
        
        # Probar SimpleList
        print(" Probando SimpleList...")
        lista = SimpleList()
        lista.add("A")
        lista.add("B")
        lista.add("C")
        print(f"   Lista: {lista.to_string()}")
        print(f"   Tamaño: {lista.get_size()}")
        print(f"   Elemento 1: {lista.get(1)}")
        
        # Probar Queue
        print("\n Probando Queue...")
        cola = Queue()
        cola.enqueue("H1-P2")
        cola.enqueue("H2-P1") 
        cola.enqueue("H3-P3")
        print(f"   Cola: {cola.to_string()}")
        print(f"   Peek: {cola.peek()}")
        print(f"   Dequeue: {cola.dequeue()}")
        print(f"   Después dequeue: {cola.to_string()}")
        
        # Probar ListOfLists
        print("\n Probando ListOfLists...")
        timeline = ListOfLists()
        timeline.add_action_to_second(1, "DR01: Adelante")
        timeline.add_action_to_second(1, "DR02: Adelante")
        timeline.add_action_to_second(2, "DR01: Regar")
        print(f"   Timeline:\n{timeline.to_string()}")
        
        print(" Pruebas de TDAs completadas")
        return True
        
    except ImportError as e:
        print(f" Error importando TDAs: {e}")
        return False


def test_basic_system():
    """Probar sistema básico sin simulación completa"""
    try:
        from utils.xml_parser import XMLParser
        from models.configuration import Configuration
        
        print("🚀 === PRUEBA BÁSICA DEL SISTEMA ===\n")
        
        # 1. Crear archivo de prueba
        create_test_xml()
        
        # 2. Probar parser
        print(" Probando parser XML...")
        parser = XMLParser()
        config = parser.parse_configuration_file('entrada_test.xml')
        
        if config:
            print("Parser funcionando correctamente")
            print(f"   Drones cargados: {config.all_drones.get_size()}")
            print(f"   Invernaderos cargados: {config.greenhouses.get_size()}")
            
            # Mostrar primer invernadero
            if config.greenhouses.get_size() > 0:
                greenhouse = config.greenhouses.get(0)
                print(f"   Nombre invernadero: {greenhouse.name}")
                print(f"   Plantas: {greenhouse.plants.get_size()}")
                print(f"   Planes: {greenhouse.irrigation_plans.get_size()}")
                
                # Mostrar primer plan
                if greenhouse.irrigation_plans.get_size() > 0:
                    plan = greenhouse.irrigation_plans.get(0)
                    print(f"   Plan '{plan.name}': {plan.plan_string}")
            
            return True
        else:
            print(" Error en el parser")
            return False
            
    except Exception as e:
        print(f" Error en prueba básica: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_simple_simulation():
    """Probar simulación simple"""
    try:
        from utils.xml_parser import XMLParser
        from services.simulator import DiscreteSimulator
        
        print("\n === PRUEBA DE SIMULACIÓN ===\n")
        
        # Cargar configuración
        parser = XMLParser()
        config = parser.parse_configuration_file('entrada_test.xml')
        
        if not config:
            print(" No se pudo cargar configuración")
            return False
        
        # Obtener primer invernadero
        greenhouse = config.greenhouses.get(0)
        print(f" Simulando: {greenhouse.name}")
        
        # Obtener primer plan
        plan = greenhouse.irrigation_plans.get(0)
        print(f" Plan: {plan.name} - {plan.plan_string}")
        
        # Crear simulador
        simulator = DiscreteSimulator(greenhouse)
        
        # Ejecutar simulación
        print(" Ejecutando simulación...")
        result = simulator.simulate_plan(plan)
        
        # Mostrar resultados
        print("\n RESULTADOS:")
        print(f"    Tiempo total: {result.total_time} segundos")
        print(f"    Agua total: {result.total_water} litros")
        print(f"    Fertilizante total: {result.total_fertilizer} gramos")
        
        print("\n👥 Estadísticas por dron:")
        for i in range(result.drone_statistics.get_size()):
            stat = result.drone_statistics.get(i)
            print(f"   {stat.drone_name}: {stat.water_used}L, {stat.fertilizer_used}g, {stat.plants_irrigated} plantas")
        
        print("\n Timeline (primeros 5 segundos):")
        max_show = min(5, result.timeline.get_max_seconds())
        for second in range(1, max_show + 1):
            actions = result.timeline.get_actions_at_second(second)
            print(f"   Segundo {second}:")
            for j in range(actions.get_size()):
                action = actions.get(j)
                print(f"      {action.drone_name}: {action.description}")
        
        if result.timeline.get_max_seconds() > 5:
            print(f"   ... y {result.timeline.get_max_seconds() - 5} segundos más")
        
        print("\n Simulación completada exitosamente")
        return True
        
    except Exception as e:
        print(f"Error en simulación: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("SISTEMA DE PRUEBAS - GuateRiegos 2.0")
    print("=" * 50)
    
    # Probar TDAs primero
    if test_data_structures():
        print("\n" + "="*50 + "\n")
        
        # Probar sistema básico
        if test_basic_system():
            print("\n" + "="*50 + "\n")
            
            # Probar simulación
            test_simple_simulation()
        else:
            print(" Prueba básica falló, no se puede continuar")
    else:
        print(" Pruebas de TDAs fallaron, no se puede continuar")
    
    print("\n Fin de las pruebas")