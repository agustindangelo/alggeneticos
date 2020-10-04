import numpy as np
import pandas as pd

def calcular_tamaño_interno_iteraciones(tamaño, maxima_potencia=13):
    '''Calcula el tamaño interno que satisfaga la condición y el número de iteraciones necesario
    para llenar completamente la matriz.'''

    if maxima_potencia < 3:
        maxima_potencia = 3

    borde_mas_largo = max(tamaño)

    for potencia in range(1, maxima_potencia + 1):
        d = (2**potencia) + 1
        if borde_mas_largo <= d:
            return (d, d), potencia

    d = 2**maxima_potencia + 1
    return (d, d), maxima_potencia

def definir_desplazamiento_diamante(superficie, i, j, medio_paso, variabilidad):
    '''Define el desplazamiento del punto medio, para el paso del diamante.'''

    arriba_izq = superficie[i - medio_paso, j - medio_paso]
    arriba_der = superficie[i - medio_paso, j + medio_paso]
    abajo_izq = superficie[i + medio_paso, j - medio_paso]
    abajo_der = superficie[i + medio_paso, j + medio_paso]

    promedio = (arriba_izq + arriba_der + abajo_izq + abajo_der) / 4.0

    valor_aleatorio = np.random.uniform()

    return variabilidad * valor_aleatorio + (1.0 - variabilidad) * promedio

def definir_desplazamiento_cuadrado(superficie, i, j, medio_paso, variabilidad):
    '''Define el desplazamiento del punto medio, para el paso del cuadrado.'''
    
    acumulador = 0
    dividir_por = 4

    # checkear celda superior
    if i - medio_paso >= 0:
        acumulador += superficie[i - medio_paso, j]
    else:
        dividir_por -= 1

    # checkear celda inferior
    if i + medio_paso < superficie.shape[0]:
        acumulador += superficie[i + medio_paso, j]
    else:
        dividir_por -= 1

    # checkear celda a la izquierda
    if j - medio_paso >= 0:
        acumulador += superficie[i, j - medio_paso]
    else:
        dividir_por -= 1

    # checkear celda a la derecha
    if j + medio_paso < superficie.shape[0]:
        acumulador += superficie[i, j + medio_paso]
    else:
        dividir_por -= 1

    promedio = acumulador / dividir_por
    valor_aleatorio = np.random.uniform()
    return variabilidad * valor_aleatorio + (1.0 - variabilidad) * promedio


def ejecutar_paso_diamante(superficie, paso, variabilidad):
    '''Realiza el paso del diamante.'''

    # calcular las esquinas del diamante
    medio_paso = int(np.floor(paso / 2))
    pasos_x = range(medio_paso, superficie.shape[0], paso)
    pasos_y = pasos_x[:]

    for i in pasos_x:
        for j in pasos_y:
            if superficie[i,j] == -1.0:
                superficie[i,j] = definir_desplazamiento_diamante(superficie, i, j, medio_paso, variabilidad)

def ejecutar_paso_cuadrado(superficie, paso, variabilidad):
    '''Realiza el paso del cuadrado.'''

    medio_paso = int(np.floor(paso / 2))

    pasos_verticales_x = range(medio_paso, superficie.shape[0], paso)
    pasos_verticales_y = range(0, superficie.shape[1], paso)

    pasos_horizontales_x = range(0, superficie.shape[0], paso)
    pasos_horizontales_y = range(medio_paso, superficie.shape[1], paso)

    for i in pasos_horizontales_x:
        for j in pasos_horizontales_y:
            superficie[i,j] = definir_desplazamiento_cuadrado(superficie, i, j, medio_paso, variabilidad)

    for i in pasos_verticales_x:
        for j in pasos_verticales_y:
            superficie[i,j] = definir_desplazamiento_cuadrado(superficie, i, j, medio_paso, variabilidad)


def generar_terreno(tamaño=(1, 1), altura_min=0.5, altura_max=1, variabilidad=0.5, semilla=0):
    '''Ejecuta el algoritmo. Retorna una matriz cuyo tamaño es el especificado por parámetro y
    la cual se corresponde con la superficie resultante. Cada elemento x_ij de esta matriz representa
    la altura del punto ij.

    Para generar la superficie, se requiere una matriz n x n donde n = 2**x + 1, donde x es un entero
    mayor o igual a 2. Sin embargo, el tamaño solicitado por parámetro puede no cumplir esta condición, por
    lo tanto  utilizamos internamente el mayor n más proximo que satisfaga dicha condición. 
    
    Por simpleza se trabaja internamente con alturas entre 0 y 1, antes de retornar la superficie
    se reescala a la altura solicitada por parámetro y en caso de ser necesario se recorta al tamaño solicitado.
    '''

    tamaño_interno, iteraciones = calcular_tamaño_interno_iteraciones(tamaño)
    
    # inicializar el arreglo de floats, los llenamos de "-1"
    superficie = np.full(tamaño_interno, -1, dtype='float')

    # seteamos la semilla para que al ejecutarlo varias veces nos dé el mismo resultado
    np.random.seed(semilla)

    # paso 1: inicializar las esquinas
    superficie[0, 0] = np.random.uniform()
    superficie[tamaño_interno[0] - 1, 0] = np.random.uniform()
    superficie[0, tamaño_interno[1] - 1] = np.random.uniform()
    superficie[tamaño_interno[0] - 1, tamaño_interno[1] - 1] = np.random.uniform()

    # paso 2: construir iterativamente la superficie
    for i in range(iteraciones):
        r = np.power(variabilidad, i) 

        paso = int(np.floor((tamaño_interno[0] - 1) / 2**i))

        ejecutar_paso_diamante(superficie, paso, r)
        ejecutar_paso_cuadrado(superficie, paso, r)

    # reescalar los valores para satisfacer los limites de altura que se pasaron por parámetro
    superficie = altura_min + (superficie * (altura_max - altura_min))

    # recortar el arreglo para satisfacer el tamaño que se pasó por parámetro
    return superficie[:tamaño[0], :tamaño[1]]