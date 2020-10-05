import pandas as pd 
import numpy as np 
from timeit import time
import itertools 

def importar_tablas():  
    # ------------------------ formateo de tabla de distancias
    tabla_distancias = pd.read_csv('apps/assets/distancias_capitales.csv')
    tabla_distancias = tabla_distancias.rename(columns={'Distancias en kilómetros': 'Capital'})
    columnas = ['capital']
    for i in range(24):
        columnas.append(i)
    tabla_distancias.columns = columnas
    # ------------------------
    tabla_capitales = pd.read_csv('apps/assets/capitales.csv')

    return tabla_distancias, tabla_capitales

def formatear(tabla_capitales, recorrido):
    # devuelve una tabla con latitudes y longitudes, ordenada por orden de recorrido lista para ser impresa en el mapa
    tabla_final = pd.DataFrame(columns=['capital', 'latitud', 'longitud'])
    
    for i in range(len(recorrido)):
        tabla_final = tabla_final.append(tabla_capitales.iloc[recorrido[i]])
    return tabla_final


def main_heuristicoA(tabla_distancias, nro_ciudad):
    t0 = time.perf_counter()

    recorrido = []
    recorrido.append(nro_ciudad)
    distancia_recorrida = 0
    
    id_capital_sig = nro_ciudad #
    tabla_auxiliar = tabla_distancias[id_capital_sig].copy() #inicializar tabla auxiliar

    while len(recorrido) < len(tabla_distancias):  # len(tabla_distancias) -> 24
    
        distancia_mas_cercana = tabla_auxiliar.min()
        id_capital_sig = tabla_auxiliar.idxmin()
        
        if id_capital_sig in recorrido:  # si verdadero, esa capital ya se visitó y por lo tanto se elimina de tabla auxiliar
            tabla_auxiliar = tabla_auxiliar.drop(id_capital_sig) 
        else:
            distancia_recorrida += distancia_mas_cercana  
            recorrido.append(id_capital_sig)
            tabla_auxiliar = tabla_distancias[id_capital_sig].copy() # reinicio la tabla auxiliar para que tenga todas las filas
    
    recorrido.append(nro_ciudad) #vuelvo a la ciudad de inicio
    tf = time.perf_counter()
    tiempo_ejecucion = tf - t0
    return recorrido, distancia_recorrida, tiempo_ejecucion

def generar_recorridos_posibles(cantidad_ciudades):
    '''
    componente para el método exhaustivo. Genera todos los recorridos posibles de longitud cantidad_ciudades
    siempre partiendo desde Bs. As. (para simplificar)
    '''
    aux = list(itertools.permutations([i for i in range(cantidad_ciudades)])) # generar permutaciones de las capitales
    
    recorridos_posibles = []
    for recorrido in aux:
        recorrido_aux = list(recorrido)   # itertools devuelve tuplas pero lo paso a listas
        recorrido_aux.append(recorrido[0]) # para que vuelva a la ciudad de partida
        recorridos_posibles.append(recorrido_aux)
    return recorridos_posibles

def calcular_distancia(tabla_distancias, recorrido):
    '''
    dado un recorrido [ciudad 1, ciudad 2,  .., ciudad n, ciudad 1], calcula la longitud del trayecto
    '''
    distancia_recorrida = 0
    for i in range(len(recorrido) - 1):
        distancia_actual = tabla_distancias[recorrido[i]][recorrido[i+1]]
        distancia_recorrida = distancia_recorrida + distancia_actual
    return distancia_recorrida

def main_exhaustivo(tabla_distancias, cantidad_ciudades):

    distancia_minima = 9999999999
    t0 = time.perf_counter()
    recorridos_posibles = generar_recorridos_posibles(cantidad_ciudades)

    for recorrido in recorridos_posibles:
        distancia_recorrida = calcular_distancia(tabla_distancias, recorrido)
        if distancia_recorrida < distancia_minima:
            distancia_minima = distancia_recorrida
            recorrido_minimo = recorrido

    t1 = time.perf_counter()
    tiempo_ejecucion = t1 - t0

    return recorrido_minimo, distancia_minima, tiempo_ejecucion