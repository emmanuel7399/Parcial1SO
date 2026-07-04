class Proceso:
    def __init__(self, etiqueta, bt, at, q, pr):
        # Tipos de datos según las especificaciones
        self.etiqueta = str(etiqueta) # Identificación del proceso
        self.bt = float(bt)           # Tiempo total necesario 
        self.at = float(at)           # Momento de llegada 
        self.q = int(q)               # Cola a la que pertenece 
        self.pr = int(pr)             # Prioridad (5 es la más alta) 
        
        # Variables de estado para la simulación
        self.remaining_bt = self.bt
        self.start_time = -1.0
        self.ct = 0.0
        self.wt = 0.0
        self.tat = 0.0
        self.rt = 0.0

    def calcular_metricas(self):
        # TurnAround Time (TAT) = Tiempo de completado - Tiempo de llegada 
        self.tat = self.ct - self.at
        # Tiempo de espera (WT) = TAT - Burst Time 
        self.wt = self.tat - self.bt
        # Tiempo de respuesta (RT) = Primer tiempo en CPU - Tiempo de llegada 
        self.rt = self.start_time - self.at