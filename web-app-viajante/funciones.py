import pandas as pd 
import numpy as np 
from timeit import time
import itertools 
from operator import itemgetter


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
    distancia_recorrida += tabla_distancias[recorrido[-1]][recorrido[-2]] # sumo la distancia de vuelta a casa
    tf = time.perf_counter()
    tiempo_ejecucion = tf - t0
    return recorrido, distancia_recorrida, tiempo_ejecucion

def main_heuristicoB(tabla_distancias):
    t0 = time.perf_counter()
    menor_distancia = 99999999999

    for i in range(len(tabla_distancias)):
        recorrido_actual = []
        recorrido_actual.append(i)
        distancia_recorrida = 0
        tabla_auxiliar = tabla_distancias[i].copy() #inicializar tabla auxiliar

        while len(recorrido_actual) < len(tabla_distancias):  # len(tabla_distancias) -> 24
            distancia_mas_cercana = tabla_auxiliar.min()
            id_capital_sig = tabla_auxiliar.idxmin()
            
            if id_capital_sig in recorrido_actual:  # si verdadero, esa capital ya se visitó y por lo tanto se elimina de tabla auxiliar
                tabla_auxiliar = tabla_auxiliar.drop(id_capital_sig) 
            else:
                distancia_recorrida += distancia_mas_cercana  
                recorrido_actual.append(id_capital_sig)
                tabla_auxiliar = tabla_distancias[id_capital_sig].copy() # reinicio la tabla auxiliar para que tenga todas las filas
        
        recorrido_actual.append(i) #vuelvo a la ciudad de inicio
        distancia_recorrida += tabla_distancias[recorrido_actual[-1]][recorrido_actual[-2]] # sumo la distancia de vuelta a casa

        if distancia_recorrida < menor_distancia:
            menor_distancia = distancia_recorrida
            menor_recorrido = recorrido_actual

    tf = time.perf_counter()
    tiempo_ejecucion = tf - t0
    return menor_recorrido, menor_distancia, tiempo_ejecucion

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

def crossover_ciclico(padre1, padre2):
    
    hijo1 = []
    hijo2 = []
    for i in range(len(padre1)):
        hijo1.append(-1)
        hijo2.append(-1)
        
    # HIJO 1
    valor_inicial = padre1[0]
    hijo1[0] = valor_inicial
    gen = padre2[0]
 
    i = 1
    while True:
        if padre1[0] == padre2[0]:
            break
        if padre1[i] == gen:
            hijo1[i] = gen
            gen = padre2[i]
            if valor_inicial == padre2[i]:
                break
        if i >= len(padre1)-1:
            i = 1
        else:
            i += 1
    #intercambiar los que quedaron vacíos
    for i, prov in enumerate(hijo1):
        if prov == -1:
            hijo1[i] = padre2[i]
            
    # HIJO 2
    valor_inicial = padre2[0]
    hijo2[0] = valor_inicial
    gen = padre1[0]
 
    i = 1
    while True:
        if padre1[0] == padre2[0]:
            break
        if padre2[i] == gen:
            hijo2[i] = gen
            gen = padre1[i]
            if valor_inicial == padre1[i]:
                break
        if i >= len(padre1)-1:
            i = 1
        else:
            i += 1
    
    #intercambiar los que quedaron vacíos
    for i, prov in enumerate(hijo2):
        if prov == -1:
            hijo2[i] = padre1[i]
    
    return hijo1, hijo2

def inicializar(tamaño_poblacion, longitud_cromosoma):
    poblacion_inicial = []
    for i in range(tamaño_poblacion):
        num = []
        num.append(np.random.randint(1,24))
        for i in range(1, longitud_cromosoma-1):
            band=True
            while(band==True):
                prov=np.random.randint(1,24)              
                repetido=0
                for j in (num):
                    if prov==j:
                        repetido=repetido+1
                if repetido<1:
                    num.append(prov)
                    band=False
        num.append(num[0])
        poblacion_inicial.append(num)
    
    return poblacion_inicial

def mutacion(cromosoma):
    aux = cromosoma[:-1]  # aux es el cromosoma pero sin la vuelta a casa
    
    provA = np.random.randint(1, len(aux)-1)
    provB = np.random.randint(1, len(aux)-1)
    #no se si haria falta validar que no toque la misma provincia a permutar
    band=False
    while (band==False):
        if provA==provB:
            provB = np.random.randint(1, len(aux)-1)
        else:
            band=True
    A=aux[provA]
    B=aux[provB]
    aux[provA]=B
    aux[provB]=A
    
    aux.append(cromosoma[0]) # vuelvo a agregar la vuelta a casa
    return aux

def func_objetivo_v2(poblacion, distancias):
    f_objetivo=0
    #sumatoria de todas las distancias de todas las poblaciones
    for cromosoma in poblacion:
        f_objetivo = f_objetivo + calcular_distancia(distancias, cromosoma)
    return f_objetivo

def fitness_v2(poblacion, cromosoma, f_obj, tabla_distancias):
    recorrido = calcular_distancia(tabla_distancias, cromosoma)
    suma_complemento = 0
    
    for r in poblacion:
        suma_complemento = suma_complemento + (f_obj - calcular_distancia(tabla_distancias, r))
        
    fitness = (f_obj - recorrido) / suma_complemento
    return fitness

def seleccionar(poblacion, distancias, elitismo=False):
    lista_poblacion = []
    id_seleccionado = 0
    padres = []
    fobj = func_objetivo_v2(poblacion, distancias)
    for id, individuo in enumerate(poblacion):
        lista_poblacion.append([id, individuo, fitness_v2(poblacion, individuo, fobj, distancias)])
    lista_poblacion = sorted(lista_poblacion, key=itemgetter(2), reverse=True)

    if elitismo:
        padres.append(lista_poblacion[0][1]) #los dos individuos elitistas
        padres.append(lista_poblacion[1][1])
    else:
        # RULETA 
        
        while len(padres) < 2:  # porque necesitamos dos padres
            num_aleatorio = np.random.rand()    
            fitness_acumulada = lista_poblacion[0][2]
            i = 0
            
            while(fitness_acumulada < 1):
                if num_aleatorio <= fitness_acumulada:
                    id_seleccionado = lista_poblacion[i][0]
                    break
                else: 
                    i += 1
                    fitness_acumulada += lista_poblacion[i][2]
                    
            if fitness_acumulada == 1:
                id_seleccionado = lista_poblacion[-1][0]

            for sublista in lista_poblacion:
                if sublista[0] == id_seleccionado:
                    cromosoma_elegido = sublista[1]
                    break
                    
            if cromosoma_elegido not in padres:
                padres.append(cromosoma_elegido)
                
    return padres[0], padres[1]

def generar_estadisticos(poblaciones, tabla_distancias):
    '''Genera la tabla, cada fila es una población'''
    resultados = [[],[],[],[],[]] # valor_fobjetivo, recorrido minimo, recorrido maximo, mediana recorridos, mejor cromosoma
    
    for poblacion in poblaciones:
        recorridos = []
        menor_recorrido = 999999999
        for cromosoma in poblacion:
            recorrido = calcular_distancia(tabla_distancias, cromosoma)
            recorridos.append((cromosoma, recorrido))   
            
            if recorrido < menor_recorrido:
                mejor_cromosoma = cromosoma
                menor_recorrido = recorrido
        recorridos = np.array(recorridos)

        resultados[0].append(np.sum(recorridos[:, 1]))
        resultados[1].append(np.min(recorridos[:, 1]))
        resultados[2].append(np.max(recorridos[:, 1]))
        resultados[3].append(np.median(recorridos[:, 1]))
        resultados[4].append(mejor_cromosoma)
        
    df = pd.DataFrame(resultados).transpose()
    df.columns = ['Función Objetivo Poblacion', 'Distancia mínima', 'Distancia máxima', 'Mediana de distancias', 'Mejor cromosoma']
    return df

def main_genetico(distancias, p_crossover=0.9, p_mutacion=0.2, ciclos=3, tamaño_poblacion=50, longitud_cromosoma=24, elitismo=True):
    t0 = time.perf_counter()
    
    poblacion_actual = inicializar(tamaño_poblacion, longitud_cromosoma)
    poblaciones = []
    poblaciones.append(poblacion_actual)
    cantidad_selecciones = tamaño_poblacion // 2

    for i in range(ciclos):
        print(f'ciclo {i}')
        poblacion_nueva = []
        if elitismo:
            padre_1, padre_2 = seleccionar(poblacion_actual, distancias, elitismo)
            poblacion_nueva.append(padre_1)
            poblacion_nueva.append(padre_2)
        for j in range(cantidad_selecciones+1):
         
            if len(poblacion_nueva) == tamaño_poblacion:
                continue
                
            # SELECCIONAR
            padre_1, padre_2 = seleccionar(poblacion_actual, distancias, False)
            
            # CRUZAR
            if np.random.rand() <= p_crossover:
                hijo_1, hijo_2 = crossover_ciclico(padre_1[:-1], padre_2[:-1])
                hijo_1.append(hijo_1[0])   # para que el hijo vuelva a casa
                hijo_2.append(hijo_2[0])   # para que el hijo vuelva a casa

            else: 
                hijo_1 = padre_1
                hijo_2 = padre_2

            # MUTAR
            if np.random.rand() <= p_mutacion:
                hijo_1 = mutacion(hijo_1)
            if np.random.rand() <= p_mutacion:
                hijo_2 = mutacion(hijo_2)

            # PASAR A PROXIMA GENERACION
            poblacion_nueva.append(hijo_1)
            if len(poblacion_nueva) != tamaño_poblacion:
                poblacion_nueva.append(hijo_2)

        poblacion_actual = poblacion_nueva
        
        poblaciones.append(poblacion_nueva)
    tf = time.perf_counter()
    
    poblaciones_df = pd.DataFrame(poblaciones)
    resultados = generar_estadisticos(poblaciones, distancias)
#    generar_graficos(resultados)
    tiempo_ejecucion = tf - t0
    
    return resultados.iloc[-1,:], tiempo_ejecucion