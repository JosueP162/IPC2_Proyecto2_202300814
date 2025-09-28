from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import sys
import os
from werkzeug.utils import secure_filename

# === CONFIGURACIÓN DE PATHS ===
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
backend_path = os.path.join(project_root, 'backend')

# Agregar todos los paths necesarios
sys.path.insert(0, project_root)
sys.path.insert(0, backend_path)

# === IMPORTACIÓN DIRECTA Y SIMPLE ===
try:
    # Intentar importación directa
    from services.main_service import CompleteIrrigationService
    print("✅ CompleteIrrigationService importado correctamente")
except ImportError as e:
    print(f"❌ Error importando desde services: {e}")
    
    # Debug: mostrar contenido
    print("🔍 Contenido de backend/services/:")
    services_dir = os.path.join(backend_path, 'services')
    if os.path.exists(services_dir):
        for file in os.listdir(services_dir):
            print(f"   - {file}")
    
    # Intentar importación alternativa
    try:
        sys.path.insert(0, os.path.join(backend_path, 'services'))
        from main_service import CompleteIrrigationService
        print("✅ CompleteIrrigationService importado desde services/main_service")
    except ImportError as e2:
        print(f"❌ Error en importación alternativa: {e2}")
        raise

# === DEFINIR LA CLASE CORRECTAMENTE EN EL NAMESPACE ===
# Asegurarnos de que la clase esté disponible
try:
    CompleteIrrigationService  # Verificar que existe
    print("✅ CompleteIrrigationService está definido")
except NameError:
    print("❌ CompleteIrrigationService no está definido")
    # Importar directamente como último recurso
    from ..backend.services.main_service import CompleteIrrigationService

app = Flask(__name__)
app.secret_key = 'guateriegos_2024_secretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Crear directorios necesarios
os.makedirs('uploads', exist_ok=True)
os.makedirs('reports', exist_ok=True)
os.makedirs('graphs', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# === INICIALIZAR EL SERVICIO ===
print("🔄 Inicializando CompleteIrrigationService...")
irrigation_service = CompleteIrrigationService()
print("✅ Servicio inicializado correctamente")
# Servicio principal
irrigation_service = CompleteIrrigationService()

@app.route('/')
def home():
    """Página principal"""
    stats = irrigation_service.calculate_statistics()
    greenhouses_sl = irrigation_service.get_available_greenhouses()
    
    # Convertir SimpleList a lista normal y contar
    greenhouses_list = simplelist_to_list(greenhouses_sl)
    greenhouse_count = len(greenhouses_list)
    
    return render_template('home.html', 
                         has_config=irrigation_service.current_configuration is not None,
                         stats=stats,
                         greenhouse_count=greenhouse_count,
                         greenhouses=greenhouses_list)

@app.route('/upload', methods=['GET', 'POST'])
def upload_configuration():
    """Cargar archivo XML de configuración"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó ningún archivo', 'error')
            return redirect(request.url)
        
        if file and file.filename.lower().endswith('.xml'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Cargar configuración
            if irrigation_service.load_configuration_file(filepath):
                flash('Configuración cargada exitosamente', 'success')
                return redirect(url_for('list_greenhouses'))
            else:
                flash('Error al procesar el archivo XML', 'error')
        else:
            flash('Solo se permiten archivos .xml', 'error')
    
    return render_template('upload.html')

@app.route('/greenhouses')
def list_greenhouses():
    """Listar todos los invernaderos"""
    if not irrigation_service.current_configuration:
        flash('Primero debe cargar un archivo de configuración', 'warning')
        return redirect(url_for('upload_configuration'))
    
    greenhouses_sl = irrigation_service.get_available_greenhouses()
    
    # Convertir SimpleList a lista normal
    greenhouses_list = simplelist_to_list(greenhouses_sl)
    
    # Procesar cada invernadero para el template
    greenhouses_for_template = []
    for greenhouse in greenhouses_list:
        # Convertir los planes de SimpleList a lista normal
        plans_list = simplelist_to_list(greenhouse.plans) if greenhouse.plans else []
        
        greenhouse_data = {
            'name': greenhouse.name,
            'rows': greenhouse.rows,
            'plants_per_row': greenhouse.plants_per_row,
            'total_plants': greenhouse.total_plants,
            'drones_count': greenhouse.drones_count,
            'plans': plans_list
        }
        greenhouses_for_template.append(greenhouse_data)
    
    return render_template('greenhouses.html', greenhouses=greenhouses_for_template)

@app.route('/greenhouse/<greenhouse_name>')
def greenhouse_detail(greenhouse_name):
    """Detalle de un invernadero específico"""
    if not irrigation_service.current_configuration:
        flash('Primero debe cargar un archivo de configuración', 'warning')
        return redirect(url_for('upload_configuration'))
    
    # Obtener información del invernadero
    greenhouses_sl = irrigation_service.get_available_greenhouses()
    
    # CORRECCIÓN: Convertir a lista normal ANTES de iterar
    greenhouses_list = simplelist_to_list(greenhouses_sl)
    
    # Ahora sí podemos iterar sobre la lista normal
    greenhouse_obj = next((g for g in greenhouses_list if g.name == greenhouse_name), None)
    
    if not greenhouse_obj:
        flash('Invernadero no encontrado', 'error')
        return redirect(url_for('list_greenhouses'))
    
    # Convertir planes a lista normal
    plans_data = []
    plans_list = simplelist_to_list(greenhouse_obj.plans)
    for plan in plans_list:
        plan_data = {
            'name': plan.name,
            'sequence': plan.sequence,
            'has_result': irrigation_service.get_simulation_result(greenhouse_name, plan.name) is not None
        }
        plans_data.append(plan_data)
    
    # Crear diccionario para el template
    greenhouse_data = {
        'name': greenhouse_obj.name,
        'rows': greenhouse_obj.rows,
        'plants_per_row': greenhouse_obj.plants_per_row,
        'total_plants': greenhouse_obj.total_plants,
        'drones_count': greenhouse_obj.drones_count,
        'plans': plans_data
    }
    
    return render_template('greenhouse_detail.html', 
                         greenhouse=greenhouse_data,
                         greenhouse_name=greenhouse_name)


@app.route('/simulate_all')
def simulate_all_plans():
    """Simular todos los planes de todos los invernaderos"""
    if irrigation_service.simulate_all_plans():
        flash('Todas las simulaciones completadas exitosamente', 'success')
    else:
        flash('Error al ejecutar las simulaciones', 'error')
    
    return redirect(url_for('list_greenhouses'))

@app.route('/report/<greenhouse_name>')
def generate_report(greenhouse_name):
    """Generar reporte HTML para un invernadero"""
    report_path = irrigation_service.generate_html_report(greenhouse_name)
    
    if report_path and os.path.exists(report_path):
        return send_file(report_path, as_attachment=False)
    else:
        flash('Error generando reporte o no hay datos de simulación', 'error')
        return redirect(url_for('greenhouse_detail', greenhouse_name=greenhouse_name))

@app.route('/reports/all')
def generate_all_reports():
    """Generar reportes para todos los invernaderos"""
    reports = irrigation_service.generate_all_html_reports()
    
    if reports:
        flash(f'Se generaron {len(reports)} reportes exitosamente', 'success')
        return jsonify({'success': True, 'reports': reports})
    else:
        flash('Error generando reportes', 'error')
        return jsonify({'success': False}), 500


@app.route('/output_xml')
def generate_output_xml():
    """Generar archivo XML de salida"""
    output_path = os.path.join('outputs', 'salida.xml')
    
    if irrigation_service.generate_xml_output(output_path):
        return send_file(output_path, as_attachment=True, 
                        download_name='salida.xml', mimetype='application/xml')
    else:
        flash('Error generando archivo XML de salida', 'error')
        return redirect(url_for('home'))

@app.route('/export_data')
def export_simulation_data():
    """Exportar datos de simulación en formato JSON"""
    data = irrigation_service.export_simulation_data('json')
    
    if data:
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(data)
            temp_path = f.name
        
        return send_file(temp_path, as_attachment=True, 
                        download_name='simulacion_datos.json', 
                        mimetype='application/json')
    else:
        flash('No hay datos de simulación para exportar', 'warning')
        return redirect(url_for('home'))

@app.route('/simulation_details/<greenhouse_name>/<plan_name>')
def simulation_details(greenhouse_name, plan_name):
    """Obtener detalles completos de una simulación"""
    result = irrigation_service.get_simulation_result(greenhouse_name, plan_name)
    
    if not result:
        return jsonify({'error': 'Simulación no encontrada'}), 404
    
    # Construir timeline completo
    timeline = {}
    for second in range(1, result.timeline.get_max_seconds() + 1):
        actions = result.timeline.get_actions_at_second(second)
        second_actions = []
        for i in range(actions.get_size()):
            action = actions.get(i)
            second_actions.append({
                'drone': action.drone_name,
                'action': action.description,
                'type': action.action_type
            })
        timeline[second] = second_actions
    
    # Estadísticas de drones
    drone_stats = []
    for i in range(result.drone_statistics.get_size()):
        stat = result.drone_statistics.get(i)
        drone_stats.append({
            'name': stat.drone_name,
            'water': stat.water_used,
            'fertilizer': stat.fertilizer_used,
            'plants': stat.plants_irrigated
        })
    
    return jsonify({
        'greenhouse': greenhouse_name,
        'plan': plan_name,
        'total_time': result.total_time,
        'total_water': result.total_water,
        'total_fertilizer': result.total_fertilizer,
        'drone_statistics': drone_stats,
        'timeline': timeline,
        'max_seconds': result.timeline.get_max_seconds()
    })

@app.route('/tda_viewer/<greenhouse_name>/<plan_name>')
def tda_viewer(greenhouse_name, plan_name):
    """Visor interactivo de TDAs"""
    result = irrigation_service.get_simulation_result(greenhouse_name, plan_name)
    
    if not result:
        flash('Simulación no encontrada', 'error')
        return redirect(url_for('greenhouse_detail', greenhouse_name=greenhouse_name))
    
    return render_template('tda_viewer.html', 
                         greenhouse_name=greenhouse_name,
                         plan_name=plan_name,
                         max_seconds=result.timeline.get_max_seconds())

@app.route('/about')
def about():
    """Información del proyecto y estudiante"""
    return render_template('about.html')

@app.route('/help')
def help_page():
    """Página de ayuda"""
    return render_template('help.html')

# Manejador de errores
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', 
                         error_code=404, 
                         error_message="Página no encontrada"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500, 
                         error_message="Error interno del servidor"), 500

# Funciones auxiliares para templates
@app.template_filter('basename')
def basename_filter(path):
    return os.path.basename(path)

@app.route('/simulate/<greenhouse_name>/<plan_name>')
def simulate_plan(greenhouse_name, plan_name):
    """Ejecutar simulación de un plan específico incluyendo timeline"""
    try:
        result = irrigation_service.simulate_specific_plan(greenhouse_name, plan_name)
        
        if result:
            # Convertir estadísticas de drones a lista normal
            drone_stats = []
            if result.drone_statistics and not result.drone_statistics.is_empty():
                for i in range(result.drone_statistics.get_size()):
                    stat = result.drone_statistics.get(i)
                    drone_stats.append({
                        'name': stat.drone_name,
                        'water': stat.water_used,
                        'fertilizer': stat.fertilizer_used,
                        'plants': stat.plants_irrigated
                    })
            
            # Convertir timeline a formato serializable
            timeline_data = {}
            max_seconds = min(20, result.timeline.get_max_seconds())  # Mostrar máximo 20 segundos
            
            for second in range(1, max_seconds + 1):
                actions = result.timeline.get_actions_at_second(second)
                second_actions = []
                
                if not actions.is_empty():
                    for i in range(actions.get_size()):
                        action = actions.get(i)
                        second_actions.append({
                            'drone': action.drone_name,
                            'action': action.description,
                            'type': action.action_type
                        })
                
                if second_actions:  # Solo incluir segundos con acciones
                    timeline_data[second] = second_actions
            
            return jsonify({
                'success': True,
                'total_time': result.total_time,
                'total_water': result.total_water,
                'total_fertilizer': result.total_fertilizer,
                'drone_statistics': drone_stats,
                'timeline': timeline_data,
                'max_seconds': result.timeline.get_max_seconds()
            })
        else:
            return jsonify({'success': False, 'error': 'No se pudo ejecutar la simulación'}), 500
            
    except Exception as e:
        print(f"Error en simulación: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    
@app.route('/tda_graph/<greenhouse_name>/<plan_name>/<int:time_t>')
def generate_tda_graph(greenhouse_name, plan_name, time_t):
    """Generar gráfico Graphviz del estado de TDAs en tiempo t"""
    try:
        result = irrigation_service.get_simulation_result(greenhouse_name, plan_name)
        
        if not result:
            # Si no hay simulación, ejecutarla primero
            result = irrigation_service.simulate_specific_plan(greenhouse_name, plan_name)
            if not result:
                return jsonify({'error': 'No se pudo ejecutar la simulación'}), 404
        
        # Generar gráfico TDA
        graph_path = irrigation_service.generate_tda_graph(greenhouse_name, plan_name, time_t)
        
        if graph_path and os.path.exists(graph_path):
            return send_file(graph_path, as_attachment=False)
        else:
            # Fallback: mostrar información en JSON
            return jsonify({
                'message': f'Visualización TDA para {greenhouse_name} - {plan_name} en t={time_t}',
                'greenhouse': greenhouse_name,
                'plan': plan_name,
                'time': time_t,
                'total_time': result.total_time,
                'total_water': result.total_water,
                'total_fertilizer': result.total_fertilizer,
                'note': 'La generación de gráficos Graphviz está en desarrollo'
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def simplelist_to_list(simple_list):
    """Convertir SimpleList a lista normal de Python"""
    if not simple_list or simple_list.is_empty():
        return []
    
    result = []
    for i in range(simple_list.get_size()):
        result.append(simple_list.get(i))
    return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)