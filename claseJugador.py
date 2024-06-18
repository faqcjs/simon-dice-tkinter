import json

class Jugador:
    def __init__(self, jug, fecha, hora, puntaje):
        self.__jugador= jug
        self.__fecha = fecha
        self.__hora = hora
        self.__puntaje = puntaje
    
    def __str__(self):
        return f'Jugador:{self.__jugador}\nPuntaje:{self.__puntaje}\nFecha:{self.__fecha}\nHora:{self.__hora}'
    
    def toJson(self):
        d = dict(
            jugador = self.__jugador,
            fecha = str(self.__fecha),
            hora = str(self.__hora),
            puntaje = self.__puntaje
        )
        return d
    
    def getJugador(self):
        return self.__jugador
    
    def getFecha(self):
        return self.__fecha
    
    def getHora(self):
        return self.__hora
    
    def getPuntaje(self):
        return self.__puntaje
    
    def __gt__(self,otro):
        return self.__puntaje < otro.__puntaje
    