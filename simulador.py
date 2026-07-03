class SimuladorMLQ:
    def __init__(self, procesos):
        self.procesos = sorted(procesos, key=lambda x: x.at) # Ordenar por tiempo de llegada
        self.tiempo_actual = 0.0
        self.terminados = []
        
        # Colas del esquema: RR(3), RR(5), Priority 
        self.cola_1 = [] # Q=1: Round Robin (Quantum 3)
        self.cola_2 = [] # Q=2: Round Robin (Quantum 5)
        self.cola_3 = [] # Q=3: Priority (5>1)

    def _encolar_procesos_llegados(self):
        llegados = [p for p in self.procesos if p.at <= self.tiempo_actual and p.remaining_bt > 0]
        for p in llegados:
            if p not in self.cola_1 and p not in self.cola_2 and p not in self.cola_3:
                if p.q == 1:
                    self.cola_1.append(p)
                elif p.q == 2:
                    self.cola_2.append(p)
                elif p.q == 3:
                    self.cola_3.append(p)

    def _obtener_siguiente_proceso(self):
        # El algoritmo despacha respetando la prioridad de la cola [cite: 13]
        if self.cola_1:
            return self.cola_1.pop(0), 3.0, 1 # (Proceso, Quantum, ID Cola)
        if self.cola_2:
            return self.cola_2.pop(0), 5.0, 2
        if self.cola_3:
            # Ordenar por prioridad (mayor a menor) y luego por tiempo de llegada
            self.cola_3.sort(key=lambda x: (-x.pr, x.at))
            return self.cola_3.pop(0), float('inf'), 3 # Priority no usa quantum per se
        return None, 0, 0

    def simular(self):
        while len(self.terminados) < len(self.procesos):
            self._encolar_procesos_llegados()
            
            proceso_actual, quantum, id_cola = self._obtener_siguiente_proceso()
            
            if proceso_actual is None:
                # Si no hay procesos listos, adelantar el tiempo a la siguiente llegada
                pendientes = [p for p in self.procesos if p.remaining_bt > 0]
                if pendientes:
                    self.tiempo_actual = min(p.at for p in pendientes)
                continue

            # Registrar el tiempo de respuesta (solo la primera vez que obtiene CPU)
            if proceso_actual.start_time == -1.0:
                proceso_actual.start_time = self.tiempo_actual

            # Determinar cuánto tiempo se ejecutará
            # Es el mínimo entre su tiempo restante y su quantum
            tiempo_ejecucion = min(proceso_actual.remaining_bt, quantum)
            
            # Para hacer el sistema expropiativo entre colas, verificamos si llega alguien a una cola superior
            siguiente_llegada = float('inf')
            pendientes = [p for p in self.procesos if p.at > self.tiempo_actual and p.remaining_bt > 0 and p.q < id_cola]
            if pendientes:
                siguiente_llegada = min(p.at for p in pendientes)
            
            # Ajustar el tiempo de ejecución si llega un proceso más prioritario antes de terminar
            tiempo_real_ejecucion = min(tiempo_ejecucion, siguiente_llegada - self.tiempo_actual)
            
            # Avanzar el reloj y reducir la ráfaga
            self.tiempo_actual += tiempo_real_ejecucion
            proceso_actual.remaining_bt -= tiempo_real_ejecucion

            self._encolar_procesos_llegados()

            # Evaluar estado del proceso post-ejecución
            if proceso_actual.remaining_bt <= 0:
                proceso_actual.ct = self.tiempo_actual
                proceso_actual.calcular_metricas()
                self.terminados.append(proceso_actual)
            else:
                # Si no terminó, vuelve a su respectiva cola
                if id_cola == 1:
                    self.cola_1.append(proceso_actual)
                elif id_cola == 2:
                    self.cola_2.append(proceso_actual)
                elif id_cola == 3:
                    self.cola_3.append(proceso_actual)