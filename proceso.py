class Proceso:
    def __init__(self, etiqueta, bt, at, q, pr):
        # Tipos de datos según las especificaciones
        self.etiqueta = str(etiqueta) # Identificación del proceso [cite: 22]
        self.bt = float(bt)           # Tiempo total necesario [cite: 23]
        self.at = float(at)           # Momento de llegada [cite: 24]
        self.q = int(q)               # Cola a la que pertenece [cite: 25]
        self.pr = int(pr)             # Prioridad (5 es la más alta) [cite: 26]
        
        # Variables de estado para la simulación
        self.remaining_bt = self.bt
        self.start_time = -1.0
        self.ct = 0.0
        self.wt = 0.0
        self.tat = 0.0
        self.rt = 0.0

    def calcular_metricas(self):
        # TurnAround Time (TAT) = Tiempo de completado - Tiempo de llegada [cite: 29]
        self.tat = self.ct - self.at
        # Tiempo de espera (WT) = TAT - Burst Time [cite: 29]
        self.wt = self.tat - self.bt
        # Tiempo de respuesta (RT) = Primer tiempo en CPU - Tiempo de llegada [cite: 29]
        self.rt = self.start_time - self.at