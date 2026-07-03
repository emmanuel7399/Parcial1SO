from proceso import Proceso
from simulador import SimuladorMLQ
import os

def procesar_archivo(ruta_entrada):
    procesos = []
    
    # Lectura del archivo de entrada
    with open(ruta_entrada, 'r') as file:
        lineas = file.readlines()
        for linea in lineas:
            linea = linea.strip()
            # Ignorar comentarios y líneas vacías
            if not linea or linea.startswith("#"):
                continue
            
            # Parseo según estructura: etiqueta; BT; AT; Q; Prioridad [cite: 21]
            datos = linea.split(";")
            if len(datos) == 5:
                p = Proceso(datos[0].strip(), datos[1], datos[2], datos[3], datos[4])
                procesos.append(p)

    # Simulación
    simulador = SimuladorMLQ(procesos)
    simulador.simular()

    # Generación de archivo de salida
    ruta_salida = f"salida_{os.path.basename(ruta_entrada)}"
    with open(ruta_salida, 'w') as file:
        file.write(f"# archivo: {os.path.basename(ruta_entrada)}\n")
        file.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n") # [cite: 28]
        
        sum_wt = sum_ct = sum_rt = sum_tat = 0.0
        
        # Ordenar los terminados por Etiqueta (o por orden de completado)
        for p in sorted(simulador.terminados, key=lambda x: x.etiqueta):
            linea = f"{p.etiqueta};{p.bt}; {p.at}; {p.q}; {p.pr};  {p.wt:.1f}; {p.ct:.1f}; {p.rt:.1f}; {p.tat:.1f}\n"
            file.write(linea)
            
            sum_wt += p.wt
            sum_ct += p.ct
            sum_rt += p.rt
            sum_tat += p.tat
            
        n = len(simulador.terminados)
        if n > 0:
            # Los valores promedio de estas métricas [cite: 30]
            promedios = f"# WT={sum_wt/n:.2f}; CT={sum_ct/n:.2f}; RT={sum_rt/n:.2f}; TAT={sum_tat/n:.2f};\n"
            file.write(promedios)
            
    print(f"Resultados generados en {ruta_salida}")

if __name__ == "__main__":
    # Prueba con el archivo proporcionado
    procesar_archivo("mlq002.txt")