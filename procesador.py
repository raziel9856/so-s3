class Procesador:

    # Algoritmo de planificación First-Come, First-Served (FCFS)
    def fcfs(procesos):
        tiempo_actual = 0
        for proceso in sorted(procesos, key=lambda p: (p.arrival_time, -p.prioridad)):
            if tiempo_actual < proceso.arrival_time:
                tiempo_actual = proceso.arrival_time
            if proceso.tiempo_respuesta == -1:
                proceso.tiempo_respuesta = tiempo_actual - proceso.arrival_time
            proceso.tiempo_espera = tiempo_actual - proceso.arrival_time
            proceso.tiempo_finalizacion = tiempo_actual + proceso.burst_time
            proceso.tiempo_retorno = proceso.tiempo_finalizacion - proceso.arrival_time
            tiempo_actual += proceso.burst_time
        return procesos

    # Algoritmo de planificación Shortest Job First (SJF)
    def sjf(procesos):
        tiempo_actual = 0
        procesos_terminados = 0
        n = len(procesos)
        while procesos_terminados < n:
            procesos_disponibles = [p for p in procesos if p.arrival_time <= tiempo_actual and p.tiempo_finalizacion == 0]
            if not procesos_disponibles:
                tiempo_actual += 1
                continue
            proceso_actual = min(procesos_disponibles, key=lambda p: (p.burst_time, -p.prioridad))
            if proceso_actual.tiempo_respuesta == -1:
                proceso_actual.tiempo_respuesta = tiempo_actual - proceso_actual.arrival_time
            tiempo_actual += proceso_actual.burst_time
            proceso_actual.tiempo_finalizacion = tiempo_actual
            proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.arrival_time
            proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.burst_time
            procesos_terminados += 1
        return procesos

    # Algoritmo de planificación Round Robin (RR)
    def round_robin(procesos, quantum):
        tiempo_actual = 0
        cola = []
        procesos_terminados = 0
        n = len(procesos)
        while procesos_terminados < n:
            for proceso in procesos:
                if proceso.arrival_time == tiempo_actual:
                    cola.append(proceso)
            if cola:
                cola.sort(key=lambda p: -p.prioridad)
                proceso_actual = cola.pop(0)
                if proceso_actual.tiempo_respuesta == -1:
                    proceso_actual.tiempo_respuesta = tiempo_actual - proceso_actual.arrival_time
                if proceso_actual.tiempo_restante > quantum:
                    tiempo_actual += quantum
                    proceso_actual.tiempo_restante -= quantum
                    cola.append(proceso_actual)
                else:
                    tiempo_actual += proceso_actual.tiempo_restante
                    proceso_actual.tiempo_restante = 0
                    proceso_actual.tiempo_finalizacion = tiempo_actual
                    proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.arrival_time
                    proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.burst_time
                    procesos_terminados += 1
            else:
                tiempo_actual += 1
        return procesos

    # Algoritmo de planificación Preemptive Shortest Job First (PSJF)
    def psjf(procesos):
        tiempo_actual = 0
        procesos_terminados = 0
        n = len(procesos)
        while procesos_terminados < n:
            procesos_disponibles = [p for p in procesos if p.arrival_time <= tiempo_actual and p.tiempo_restante > 0]
            if not procesos_disponibles:
                tiempo_actual += 1
                continue
            proceso_actual = min(procesos_disponibles, key=lambda p: (p.tiempo_restante, -p.prioridad))
            if proceso_actual.tiempo_respuesta == -1:
                proceso_actual.tiempo_respuesta = tiempo_actual - proceso_actual.arrival_time
            proceso_actual.tiempo_restante -= 1
            tiempo_actual += 1
            if proceso_actual.tiempo_restante == 0:
                proceso_actual.tiempo_finalizacion = tiempo_actual
                proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.arrival_time
                proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.burst_time
                procesos_terminados += 1
        return procesos

    # Algoritmo de planificación Multi-Level Queue (MLQ)
    def mlq(procesos, colas):
        tiempo_actual = 0
        procesos_terminados = 0
        n = len(procesos)
        while procesos_terminados < n:
            for cola in colas:
                procesos_disponibles = [p for p in procesos if p.arrival_time <= tiempo_actual and p.tiempo_restante > 0]
                if procesos_disponibles:
                    if cola['algoritmo'] == Procesador.round_robin:
                        procesos_actualizados = cola['algoritmo'](procesos_disponibles, cola['quantum'])
                    else:
                        procesos_actualizados = cola['algoritmo'](procesos_disponibles)

                    for proceso_actual in procesos_actualizados:
                        if proceso_actual.tiempo_restante == 0:
                            tiempo_actual += proceso_actual.burst_time
                            proceso_actual.tiempo_finalizacion = tiempo_actual
                            proceso_actual.tiempo_retorno = proceso_actual.tiempo_finalizacion - proceso_actual.arrival_time
                            proceso_actual.tiempo_espera = proceso_actual.tiempo_retorno - proceso_actual.burst_time
                            procesos_terminados += 1
                    break
                else:
                    tiempo_actual += 1
        return procesos

    # Función para calcular los promedios de los tiempos de espera, finalización, respuesta y retorno
    def calcular_promedios(procesos):
        n = len(procesos)
        total_wt = sum(p.tiempo_espera for p in procesos)
        total_ct = sum(p.tiempo_finalizacion for p in procesos)
        total_rt = sum(p.tiempo_respuesta for p in procesos)
        total_tat = sum(p.tiempo_retorno for p in procesos)

        return {
            'WT_promedio': total_wt / n,
            'CT_promedio': total_ct / n,
            'RT_promedio': total_rt / n,
            'TAT_promedio': total_tat / n
        }