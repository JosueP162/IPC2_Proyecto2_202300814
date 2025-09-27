
class HTMLReportGenerator:
    """Generador de reportes HTML para cada invernadero"""
    
    def __init__(self):
        pass
    
    def generate_greenhouse_report(self, greenhouse, simulation_results, output_path):
        """Generar reporte HTML completo para un invernadero"""
        
        html_content = self._create_html_structure(greenhouse, simulation_results)
        
        # Escribir archivo
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Reporte HTML generado: {output_path}")
        return output_path
    
    def _create_html_structure(self, greenhouse, simulation_results):
        """Crear estructura completa del HTML"""
        
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte - {greenhouse.name}</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1> {greenhouse.name}</h1>
            <p class="subtitle">Sistema de Riego Automatizado GuateRiegos 2.0</p>
        </header>
        
        <div class="greenhouse-info">
            <h2>Información del Invernadero</h2>
            <div class="info-grid">
                <div class="info-card">
                    <h3>Dimensiones</h3>
                    <p>{greenhouse.num_rows} hileras × {greenhouse.plants_per_row} plantas</p>
                </div>
                <div class="info-card">
                    <h3>Total Plantas</h3>
                    <p>{greenhouse.plants.get_size()} plantas</p>
                </div>
                <div class="info-card">
                    <h3>Drones Asignados</h3>
                    <p>{greenhouse.drones.get_size()} drones</p>
                </div>
                <div class="info-card">
                    <h3>Planes de Riego</h3>
                    <p>{greenhouse.irrigation_plans.get_size()} planes</p>
                </div>
            </div>
        </div>
        
        {self._create_drone_assignment_section(greenhouse)}
        
        {self._create_plans_section(greenhouse, simulation_results)}
        
        <footer>
            <p>Generado por GuateRiegos 2.0 - Sistema de Riego Automatizado</p>
        </footer>
    </div>
</body>
</html>"""
        
        return html
    
    def _get_css_styles(self):
        """Estilos CSS para el reporte"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .greenhouse-info {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .info-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #4CAF50;
        }
        
        .info-card h3 {
            color: #4CAF50;
            margin-bottom: 10px;
        }
        
        .info-card p {
            font-size: 1.1em;
            font-weight: bold;
        }
        
        .section {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .section h2 {
            color: #4CAF50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        tr:hover {
            background-color: #f5f5f5;
        }
        
        .timeline-table {
            font-size: 0.9em;
        }
        
        .timeline-table td {
            padding: 8px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #4CAF50;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
        }
        
        .plan-section {
            margin-bottom: 40px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .plan-header {
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .plan-content {
            padding: 20px;
        }
        
        .action-irrigate {
            background-color: #d4edda !important;
            color: #155724;
            font-weight: bold;
        }
        
        .action-move {
            background-color: #fff3cd !important;
            color: #856404;
        }
        
        .action-wait {
            background-color: #f8d7da !important;
            color: #721c24;
        }
        
        .action-finish {
            background-color: #d1ecf1 !important;
            color: #0c5460;
        }
        """
    
    def _create_drone_assignment_section(self, greenhouse):
        """Crear sección de asignación de drones"""
        
        html = """
        <div class="section">
            <h2>Asignación de Drones</h2>
            <table>
                <thead>
                    <tr>
                        <th>Hilera</th>
                        <th>Dron Asignado</th>
                        <th>ID Dron</th>
                    </tr>
                </thead>
                <tbody>"""
        
        # Ordenar drones por hilera asignada
        drones_info = []
        for i in range(greenhouse.drones.get_size()):
            drone = greenhouse.drones.get(i)
            drones_info.append((drone.assigned_row, drone.name, drone.id))
        
        # Ordenar por hilera
        drones_info.sort(key=lambda x: x[0])
        
        for row, name, drone_id in drones_info:
            html += f"""
                    <tr>
                        <td>H{row}</td>
                        <td>{name}</td>
                        <td>{drone_id}</td>
                    </tr>"""
        
        html += """
                </tbody>
            </table>
        </div>"""
        
        return html
    
    def _create_plans_section(self, greenhouse, simulation_results):
        """Crear sección de planes de riego"""
        
        html = """
        <div class="section">
            <h2>Planes de Riego y Simulaciones</h2>"""
        
        # Para cada plan
        for i in range(greenhouse.irrigation_plans.get_size()):
            plan = greenhouse.irrigation_plans.get(i)
            
            # Buscar resultado de simulación
            result_key = f"{greenhouse.name}_{plan.name}"
            result = simulation_results.get(result_key) if simulation_results else None
            
            html += f"""
            <div class="plan-section">
                <div class="plan-header">
                    <h3>{plan.name}</h3>
                    <p><strong>Secuencia:</strong> {plan.plan_string}</p>
                </div>
                <div class="plan-content">"""
            
            if result:
                html += self._create_plan_statistics(result)
                html += self._create_drone_efficiency_table(result)
                html += self._create_timeline_table(result)
            else:
                html += "<p><em>No se ha ejecutado simulación para este plan.</em></p>"
            
            html += """
                </div>
            </div>"""
        
        html += "</div>"
        return html
    
    def _create_plan_statistics(self, result):
        """Crear estadísticas del plan"""
        
        html = f"""
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{result.total_time}</div>
                <div class="stat-label">Segundos</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{result.total_water}</div>
                <div class="stat-label">Litros Agua</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{result.total_fertilizer}</div>
                <div class="stat-label">Gramos Fertilizante</div>
            </div>
        </div>"""
        
        return html
    
    def _create_drone_efficiency_table(self, result):
        """Crear tabla de eficiencia de drones"""
        
        html = """
        <h4>Uso de Recursos por Dron</h4>
        <table>
            <thead>
                <tr>
                    <th>Dron</th>
                    <th>Litros Agua</th>
                    <th>Gramos Fertilizante</th>
                    <th>Plantas Regadas</th>
                </tr>
            </thead>
            <tbody>"""
        
        for i in range(result.drone_statistics.get_size()):
            stat = result.drone_statistics.get(i)
            html += f"""
                <tr>
                    <td>{stat.drone_name}</td>
                    <td>{stat.water_used}</td>
                    <td>{stat.fertilizer_used}</td>
                    <td>{stat.plants_irrigated}</td>
                </tr>"""
        
        html += """
            </tbody>
        </table>"""
        
        return html
    
    def _create_timeline_table(self, result):
        """Crear tabla de timeline de instrucciones"""
        
        html = """
        <h4> Timeline de Instrucciones</h4>
        <table class="timeline-table">
            <thead>
                <tr>
                    <th>Tiempo (s)</th>"""
        
        # Obtener nombres de drones para headers
        drone_names = []
        if not result.drone_statistics.is_empty():
            for i in range(result.drone_statistics.get_size()):
                stat = result.drone_statistics.get(i)
                drone_names.append(stat.drone_name)
                html += f"<th>{stat.drone_name}</th>"
        
        html += """
                </tr>
            </thead>
            <tbody>"""
        
        # Para cada segundo
        max_seconds = result.timeline.get_max_seconds()
        
        for second in range(1, max_seconds + 1):
            actions = result.timeline.get_actions_at_second(second)
            
            html += f"<td><strong>{second}</strong></td>"
            
            # Crear diccionario de acciones por dron para este segundo
            actions_by_drone = {}
            for i in range(actions.get_size()):
                action = actions.get(i)
                actions_by_drone[action.drone_name] = action
            
            # Para cada dron, mostrar su acción
            for drone_name in drone_names:
                if drone_name in actions_by_drone:
                    action = actions_by_drone[drone_name]
                    css_class = self._get_action_css_class(action.action_type)
                    html += f'<td class="{css_class}">{action.description}</td>'
                else:
                    html += '<td>-</td>'
            
            html += "</tr>"
        
        html += """
            </tbody>
        </table>"""
        
        return html
    
    def _get_action_css_class(self, action_type):
        """Obtener clase CSS según tipo de acción"""
        if action_type == "irrigate":
            return "action-irrigate"
        elif action_type in ["move_forward", "move_backward"]:
            return "action-move"
        elif action_type == "wait":
            return "action-wait"
        elif action_type == "finish":
            return "action-finish"
        else:
            return ""


# Función para generar reportes de todos los invernaderos
def generate_all_reports(configuration, simulation_results, output_dir="reports/"):
    """Generar reportes HTML para todos los invernaderos"""
    import os
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    generator = HTMLReportGenerator()
    
    for i in range(configuration.greenhouses.get_size()):
        greenhouse = configuration.greenhouses.get(i)
        
        # Crear nombre de archivo
        filename = f"Reporte_{greenhouse.name.replace(' ', '_')}.html"
        output_path = os.path.join(output_dir, filename)
        
        # Generar reporte
        generator.generate_greenhouse_report(greenhouse, simulation_results, output_path)