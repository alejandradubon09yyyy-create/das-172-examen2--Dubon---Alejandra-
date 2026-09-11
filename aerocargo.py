"""
Módulo de Funciones del Sistema AeroCargo-Matrix
Contiene la lógica de validación, cálculo de ocupación, evaluación de balance 
y extracción de submatrices sin modificar las matrices de entrada.
"""

def validar_matriz_coherencia(cargas, capacidades):
    """
    Valida las dimensiones, regularidad y coherencia numérica de las matrices.
    Retorna True si son válidas, de lo contrario False.
    """
    if not cargas or not capacidades:
        return False

    n_cargas, n_cap = len(cargas), len(capacidades)
    if n_cargas < 2 or n_cap < 2 or n_cargas != n_cap:
        return False

    m_cargas = len(cargas[0])
    m_cap = len(capacidades[0])
    if m_cargas < 2 or m_cap < 2 or m_cargas != m_cap:
        return False

    # Validar regularidad y valores permitidos (peso >= 0, capacidad > 0)
    for i in range(n_cargas):
        if len(cargas[i]) != m_cargas or len(capacidades[i]) != m_cap:
            return False
        for j in range(m_cargas):
            val_carga = cargas[i][j]
            val_cap = capacidades[i][j]
            if val_carga < 0 or val_cap <= 0:
                return False

    return True


def calcular_ocupacion_sobrecargas(cargas, capacidades):
    """
    Calcula la matriz de porcentajes de ocupación y lista las celdas en sobrecarga (>100.0%).
    Retorna una tupla: (matriz_porcentajes, lista_coordenadas_sobrecarga).
    """
    n = len(cargas)
    m = len(cargas[0])
    matriz_ocupacion = []
    sobrecargas = []

    for i in range(n):
        fila_porcentajes = []
        for j in range(m):
            porcentaje = (cargas[i][j] / capacidades[i][j]) * 100.0
            fila_porcentajes.append(round(porcentaje, 2))
            if porcentaje > 100.0:
                sobrecargas.append((i, j))
        matriz_ocupacion.append(fila_porcentajes)

    return matriz_ocupacion, sobrecargas


def evaluar_balance_lateral(cargas, tolerancia_kg):
    """
    Calcula los pesos longitudinales (vector por fila) y el desbalance lateral (babor vs estribor).
    Retorna una tupla: (vector_pesos_filas, desbalance_kg, esta_balanceado).
    """
    n = len(cargas)
    m = len(cargas[0])
    vector_pesos_filas = []

    suma_izquierda = 0.0
    suma_derecha = 0.0

    mitad = m // 2
    es_impar = (m % 2 != 0)

    for i in range(n):
        peso_fila = sum(cargas[i])
        vector_pesos_filas.append(peso_fila)

        for j in range(m):
            val = cargas[i][j]
            # Si m es impar, omitimos la columna central (j == mitad)
            if es_impar and j == mitad:
                continue
            if j < mitad:
                suma_izquierda += val
            else:
                suma_derecha += val

    desbalance_kg = abs(suma_izquierda - suma_derecha)
    esta_balanceado = desbalance_kg <= tolerancia_kg

    return vector_pesos_filas, round(desbalance_kg, 2), esta_balanceado


def extraer_submatriz_critica(matriz_ocupacion, k, p):
    """
    Extrae la submatriz k x p con el mayor promedio de ocupación usando ventana deslizante.
    """
    n = len(matriz_ocupacion)
    m = len(matriz_ocupacion[0])

    if k > n or p > m or k <= 0 or p <= 0:
        return []

    max_promedio = -1.0
    mejor_submatriz = []

    for i in range(n - k + 1):
        for j in range(m - p + 1):
            suma_ventana = 0.0
            submatriz_actual = []

            for r in range(k):
                fila_sub = []
                for c in range(p):
                    val = matriz_ocupacion[i + r][j + c]
                    suma_ventana += val
                    fila_sub.append(val)
                submatriz_actual.append(fila_sub)

            promedio_actual = suma_ventana / (k * p)

            if promedio_actual > max_promedio:
                max_promedio = promedio_actual
                mejor_submatriz = submatriz_actual

    return mejor_submatriz  