class Proceso:
    def __init__(self, etiqueta, burst_time, arrival_time, queue, prioridad):
        self.etiqueta = etiqueta
        self.burst_time = burst_time
        self.arrival_time = arrival_time
        self.queue = queue
        self.prioridad = prioridad
        self.tiempo_restante = burst_time
        self.tiempo_finalizacion = 0
        self.tiempo_espera = 0
        self.tiempo_retorno = 0
        self.tiempo_respuesta = -1