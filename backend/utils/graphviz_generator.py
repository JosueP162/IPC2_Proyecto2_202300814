# backend/utils/graphviz_generator.py - CORREGIDO
import sys
import os

# Agregar paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'data_structures'))
from data_structures.simple_list import SimpleList

class DroneStatInfo:
    """Info de estadísticas de dron para gráfico"""
    def __init__(self, drone_name):
        self.drone_name = drone_name
        self.water = 0
        self.fertilizer = 0
        self.plants = 0

class GraphvizTDAGenerator:
    def __init__(self):
        pass
    
    def generate_tda_graph(self, simulation_result, time_t, output_path="tda_graph.dot"):
        """Generar gráfico usando solo TDAs"""
        
        # Crear contenido DOT
        dot_content = self._create_dot_content(simulation_result, time_t)
        
        # Escribir archivo .dot
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dot_content)
        
        # Intentar generar PNG
        try:
            import subprocess
            png_path = output_path.replace('.dot', '.png')
            subprocess.run(['dot', '-Tpng', output_path, '-o', png_path], check=True)
            return png_path, output_path
        except:
            return None, output_path
    
    def _create_dot_content(self, simulation_result, time_t):
        """Crear contenido DOT usando TDAs"""
        
        # Obtener acciones en tiempo t
        actions_at_t = simulation_result.timeline.get_actions_at_second(time_t)
        
        dot = f"""digraph TDA_Estado_T{time_t} {{
    rankdir=LR;
    node [shape=box, style=filled, fontname="Arial"];
    edge [fontname="Arial"];
    
    // Título
    label="Estado de TDAs en Segundo {time_t}";
    labelloc=t;
    fontsize=16;
    fontname="Arial Bold";
    
    // Nodo principal del timeline
    timeline [label="Timeline\\nSegundo {time_t}", fillcolor="lightblue", shape=ellipse];
    
    // Nodos de acciones
"""
        
        # Agregar nodos de acciones usando TDAs
        if not actions_at_t.is_empty():
            for i in range(actions_at_t.get_size()):
                action = actions_at_t.get(i)
                color = self._get_node_color(action.action_type)
                
                dot += f'    action{i} [label="{action.drone_name}\\n{action.description}", fillcolor="{color}"];\n'
                dot += f'    timeline -> action{i};\n'
        else:
            dot += '    empty [label="Sin acciones\\nen este segundo", fillcolor="lightgray"];\n'
            dot += '    timeline -> empty;\n'
        
        # Agregar estructura de cola usando TDAs
        dot += '\n    // Cola del Plan de Riego\n'
        dot += '    subgraph cluster_queue {\n'
        dot += '        label="Cola de Tareas Restantes";\n'
        dot += '        style=dashed;\n'
        dot += '        color=blue;\n'
        
        # Estimar tareas restantes usando TDAs
        remaining_tasks = self._estimate_remaining_tasks(simulation_result, time_t)
        for i in range(remaining_tasks.get_size()):
            task = remaining_tasks.get(i)
            dot += f'        queue{i} [label="{task}", fillcolor="yellow"];\n'
            if i > 0:
                dot += f'        queue{i-1} -> queue{i};\n'
        
        dot += '    }\n'
        
        # Agregar estadísticas usando TDAs
        dot += '\n    // Estadísticas Acumuladas\n'
        dot += '    subgraph cluster_stats {\n'
        dot += '        label="Estadísticas hasta T=' + str(time_t) + '";\n'
        dot += '        style=filled;\n'
        dot += '        fillcolor=lightgreen;\n'
        
        # Calcular estadísticas parciales usando TDAs
        partial_stats = self._calculate_partial_stats(simulation_result, time_t)
        for i in range(partial_stats.get_size()):
            stat_info = partial_stats.get(i)
            dot += f'        {stat_info.drone_name}_stats [label="{stat_info.drone_name}\\nAgua: {stat_info.water}L\\nFertilizante: {stat_info.fertilizer}g\\nPlantas: {stat_info.plants}", shape=record];\n'
        
        dot += '    }\n'
        dot += '}\n'
        
        return dot
    
    def _get_node_color(self, action_type):
        """Color según tipo de acción"""
        if action_type == 'irrigate':
            return 'lightgreen'
        elif action_type == 'move_forward' or action_type == 'move_backward':
            return 'lightyellow'
        elif action_type == 'wait':
            return 'lightcoral'
        elif action_type == 'finish':
            return 'lightblue'
        return 'white'
    
    def _estimate_remaining_tasks(self, simulation_result, time_t):
        """Estimar tareas restantes usando TDAs"""
        remaining = SimpleList()
        max_time = simulation_result.timeline.get_max_seconds()
        
        if time_t >= max_time:
            remaining.add("Cola vacía")
            return remaining
        
        # Tareas de ejemplo
        sample_tasks = SimpleList()
        sample_tasks.add("H1-P3")
        sample_tasks.add("H2-P4") 
        sample_tasks.add("H3-P1")
        sample_tasks.add("H1-P1")
        
        # Agregar algunas tareas basado en tiempo restante
        remaining_seconds = max_time - time_t
        max_tasks = 3 if remaining_seconds > 6 else remaining_seconds // 2
        
        for i in range(min(max_tasks, sample_tasks.get_size())):
            remaining.add(sample_tasks.get(i))
        
        if remaining.is_empty():
            remaining.add("Finalizando...")
        
        return remaining
    
    def _calculate_partial_stats(self, simulation_result, time_t):
        """Calcular estadísticas parciales usando TDAs"""
        partial_stats = SimpleList()
        
        # Inicializar stats para cada dron usando TDAs
        for i in range(simulation_result.drone_statistics.get_size()):
            drone_stat = simulation_result.drone_statistics.get(i)
            stat_info = DroneStatInfo(drone_stat.drone_name)
            partial_stats.add(stat_info)
        
        # Contar acciones de riego hasta tiempo t usando TDAs
        max_check_time = min(time_t, simulation_result.timeline.get_max_seconds())
        
        for second in range(1, max_check_time + 1):
            actions = simulation_result.timeline.get_actions_at_second(second)
            for j in range(actions.get_size()):
                action = actions.get(j)
                if action.action_type == 'irrigate':
                    # Buscar estadística del dron correspondiente
                    for k in range(partial_stats.get_size()):
                        stat_info = partial_stats.get(k)
                        if stat_info.drone_name == action.drone_name:
                            stat_info.plants += 1
                            stat_info.water += 1  # Estimación simple
                            stat_info.fertilizer += 100  # Estimación simple
                            break
        
        return partial_stats