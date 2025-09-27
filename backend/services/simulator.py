
from data_structures.list_of_lists import ListOfLists
from data_structures.simple_list import SimpleList

class DroneAction:
    def __init__(self, drone_name, action_type, description):
        self.drone_name = drone_name
        self.action_type = action_type  # 'move_forward', 'move_backward', 'irrigate', 'wait', 'finish'
        self.description = description  # 'Adelante (H1P2)', 'Regar', 'Esperar', etc.

class SimulationResult:
    def __init__(self):
        self.timeline = ListOfLists()
        self.total_time = 0
        self.total_water = 0
        self.total_fertilizer = 0
        self.drone_statistics = SimpleList()  # Lista de estadísticas por dron

class DroneStatistics:
    def __init__(self, drone_name):
        self.drone_name = drone_name
        self.water_used = 0
        self.fertilizer_used = 0
        self.plants_irrigated = 0

class DiscreteSimulator:
    def __init__(self, greenhouse):
        self.greenhouse = greenhouse
        self.current_time = 0
        self.simulation_finished = False
    
    def simulate_plan(self, irrigation_plan):
        """Ejecutar simulación completa del plan de riego"""
        # Reiniciar estado
        self._reset_simulation()
        
        # Crear resultado
        result = SimulationResult()
        
        # Inicializar estadísticas de drones
        drone_stats = self._initialize_drone_statistics()
        
        # Clonar el plan para no modificar el original
        current_plan = self._clone_irrigation_plan(irrigation_plan)
        
        # Simulación paso a paso
        while not self._is_simulation_complete(current_plan):
            self.current_time += 1
            
            # Calcular acciones para este segundo
            actions_this_second = self._calculate_actions_for_second(current_plan, drone_stats)
            
            # Guardar acciones en timeline
            for i in range(actions_this_second.get_size()):
                action = actions_this_second.get(i)
                result.timeline.add_action_to_second(self.current_time, action)
            
            # Ejecutar acciones (actualizar estados)
            self._execute_actions(actions_this_second, current_plan, drone_stats)
        
        # Finalizar resultado
        result.total_time = self.current_time
        result.drone_statistics = drone_stats
        self._calculate_totals(result, drone_stats)
        
        return result
    
    def _reset_simulation(self):
        """Reiniciar estado de simulación"""
        self.current_time = 0
        self.simulation_finished = False
        
        # Resetear posiciones de drones
        for i in range(self.greenhouse.drones.get_size()):
            drone = self.greenhouse.drones.get(i)
            drone.reset_position()
    
    def _initialize_drone_statistics(self):
        """Crear estadísticas iniciales para cada dron"""
        stats = SimpleList()
        
        for i in range(self.greenhouse.drones.get_size()):
            drone = self.greenhouse.drones.get(i)
            drone_stat = DroneStatistics(drone.name)
            stats.add(drone_stat)
        
        return stats
    
    def _clone_irrigation_plan(self, original_plan):
        """Crear copia del plan para no modificar el original"""
        # CAMBIAR ESTE IMPORT:
        from models.irrigation_plan import IrrigationPlan
        return IrrigationPlan(original_plan.name, original_plan.plan_string)
    
    def _calculate_actions_for_second(self, current_plan, drone_stats):
        """Calcular qué debe hacer cada dron en este segundo"""
        actions = SimpleList()
        
        current_task = current_plan.get_next_task()  # H1-P2, H2-P1, etc.
        
        for i in range(self.greenhouse.drones.get_size()):
            drone = self.greenhouse.drones.get(i)
            action = self._decide_drone_action(drone, current_task, current_plan)
            actions.add(action)
        
        return actions
    
    def _decide_drone_action(self, drone, current_task, current_plan):
        """Decidir qué acción debe realizar un dron específico"""
        
        # Si no hay más tareas, terminar
        if current_task is None:
            return DroneAction(drone.name, "finish", "FIN")
        
        # Parsear tarea actual (H1-P2 -> row=1, position=2)
        target_row, target_position = self._parse_task(current_task)
        
        # ¿Es tarea para este dron?
        if target_row != drone.assigned_row:
            # No es su turno, esperar
            return DroneAction(drone.name, "wait", "Esperar")
        
        # ¿Está en la posición correcta?
        if drone.current_position == target_position:
            # Puede regar
            return DroneAction(drone.name, "irrigate", "Regar")
        
        # Necesita moverse
        if drone.current_position < target_position:
            # Moverse adelante
            next_pos = drone.current_position + 1
            description = f"Adelante (H{drone.assigned_row}P{next_pos})"
            return DroneAction(drone.name, "move_forward", description)
        else:
            # Moverse atrás
            next_pos = drone.current_position - 1
            description = f"Atrás (H{drone.assigned_row}P{next_pos})"
            return DroneAction(drone.name, "move_backward", description)
    
    def _parse_task(self, task):
        """Convertir 'H1-P2' a row=1, position=2"""
        if not task:
            return None, None
        
        # H1-P2 -> ["H1", "P2"]
        parts = task.split("-")
        row = int(parts[0][1:])  # H1 -> 1
        position = int(parts[1][1:])  # P2 -> 2
        
        return row, position
    
    def _execute_actions(self, actions, current_plan, drone_stats):
        """Ejecutar las acciones calculadas"""
        
        for i in range(actions.get_size()):
            action = actions.get(i)
            drone = self._get_drone_by_name(action.drone_name)
            
            if action.action_type == "move_forward":
                drone.move_forward()
            
            elif action.action_type == "move_backward":
                drone.move_backward()
            
            elif action.action_type == "irrigate":
                drone.irrigate()
                # Actualizar estadísticas
                self._update_drone_statistics(drone, drone_stats)
                # Completar tarea actual
                current_plan.complete_current_task()
            
            elif action.action_type == "wait":
                drone.wait()
            
            elif action.action_type == "finish":
                drone.finish()
    
    def _get_drone_by_name(self, drone_name):
        """Buscar dron por nombre"""
        for i in range(self.greenhouse.drones.get_size()):
            drone = self.greenhouse.drones.get(i)
            if drone.name == drone_name:
                return drone
        return None
    
    def _update_drone_statistics(self, drone, drone_stats):
        """Actualizar estadísticas cuando un dron riega"""
        # Buscar estadísticas del dron
        for i in range(drone_stats.get_size()):
            stat = drone_stats.get(i)
            if stat.drone_name == drone.name:
                # Obtener planta regada
                plant = self.greenhouse.get_plant_at(drone.assigned_row, drone.current_position)
                if plant:
                    stat.water_used += plant.water_liters
                    stat.fertilizer_used += plant.fertilizer_grams
                    stat.plants_irrigated += 1
                break
    
    def _calculate_totals(self, result, drone_stats):
        """Calcular totales de agua y fertilizante"""
        total_water = 0
        total_fertilizer = 0
        
        for i in range(drone_stats.get_size()):
            stat = drone_stats.get(i)
            total_water += stat.water_used
            total_fertilizer += stat.fertilizer_used
        
        result.total_water = total_water
        result.total_fertilizer = total_fertilizer
    
    def _is_simulation_complete(self, current_plan):
        """Verificar si la simulación ha terminado"""
        return current_plan.is_completed()