from data_structures.queue import Queue

class IrrigationPlan:
    def __init__(self, name, plan_string):
        self.name = name
        self.plan_string = plan_string
        self.irrigation_queue = Queue()
        self._parse_plan_string(plan_string)
    
    def _parse_plan_string(self, plan_string):
        """Parsear 'H1-P2, H2-P1, H2-P2, H3-P3, H1-P4' a cola"""
        # Limpiar y dividir
        tasks = plan_string.replace(" ", "").split(",")
        
        for task in tasks:
            if task.strip():  # Ignorar elementos vacíos
                self.irrigation_queue.enqueue(task.strip())
    
    def get_next_task(self):
        """Obtener siguiente tarea sin eliminarla"""
        return self.irrigation_queue.peek()
    
    def complete_current_task(self):
        """Marcar tarea actual como completada"""
        if not self.irrigation_queue.is_empty():
            return self.irrigation_queue.dequeue()
        return None
    
    def is_completed(self):
        return self.irrigation_queue.is_empty()