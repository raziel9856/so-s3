import os
import random
from proceso import Proceso
from procesador import Procesador

archivo_seleccionado_global = ""
def main():
    opc = 0
    while opc != 2:
        print("""
        Seleccione la opción deseada:
            1. Leer un archivo
            2. Salir del Programa
        """)
        opc = int(input())
        if (opc == 1):
            procesos = leer_archivo()
            colas = [
                {'prioridad': 1, 'algoritmo': Procesador.round_robin, 'quantum': 1},
                {'prioridad': 2, 'algoritmo': Procesador.round_robin, 'quantum': 3},
                {'prioridad': 4, 'algoritmo': Procesador.sjf}
            ]
            procesos = Procesador.mlq(procesos, colas)
            promedio = Procesador.calcular_promedios(procesos)
            imprimir_procesos(procesos, promedio)
            print(f"Promedios: {promedio}")
        elif (opc != 2):
            print("Has escogido una opción inválida")

def leer_archivo():
    global archivo_seleccionado_global
    carpeta = 'entrada'
    archivos = os.listdir(carpeta)
    if not archivos:
        print("No hay archivos en la carpeta 'entrada'.")
        return

    archivo_seleccionado = random.choice(archivos)
    archivo_seleccionado_global = archivo_seleccionado
    ruta_archivo = os.path.join(carpeta, archivo_seleccionado)
    print(f"Archivo seleccionado: {archivo_seleccionado}")

    procesos = []
    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea.startswith('#') or not linea:
                continue
            valores = linea.split(';')
            if len(valores) == 5:
                etiqueta, burst_time, arrival_time, queue, prioridad = valores
                proceso = Proceso(etiqueta, int(burst_time), int(arrival_time), int(queue), int(prioridad))
                procesos.append(proceso)
    return procesos


def imprimir_procesos(procesos, promedio):
    global archivo_seleccionado_global
    nombre_salida = os.path.splitext(archivo_seleccionado_global)[0] + ".txt"
    ruta_salida = os.path.join('salida', nombre_salida)
    os.makedirs('salida', exist_ok=True)

    with open(ruta_salida, 'w') as archivo_salida:
        archivo_salida.write(f"# archivo: {archivo_seleccionado_global}\n")
        archivo_salida.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")
        for proceso in procesos:
            linea = (f"{proceso.etiqueta}; {proceso.burst_time}; {proceso.arrival_time}; {proceso.queue}; {proceso.prioridad}; "
                     f"{proceso.tiempo_espera}; {proceso.tiempo_finalizacion}; {proceso.tiempo_respuesta}; {proceso.tiempo_retorno}\n")
            archivo_salida.write(linea)
            print(linea.strip())
        archivo_salida.write(f"\nWT: {promedio['WT_promedio']}; CT: {promedio['CT_promedio']}; RT: {promedio['RT_promedio']}; TAT: {promedio['TAT_promedio']}")

main()