"""
Script Principal de Ejecución (AeroCargo-Matrix)
Demuestra el flujo completo del sistema con datos de prueba realistas.
"""

from aerocargo import (
    validar_matriz_coherencia,
    calcular_ocupacion_sobrecargas,
    evaluar_balance_lateral,
    extraer_submatriz_critica
)

def imprimir_matriz(titulo, matriz, es_porcentaje=False):
    print(f"\n--- {titulo} ---")
    for fila in matriz:
        if es_porcentaje:
            print("  [" + ", ".join(f"{val:6.1f}%" for val in fila) + "]")
        else:
            print("  [" + ", ".join(f"{val:6.1f}" for val in fila) + "]")

def ejecutar_simulacion():
    print("=========================================================")
    print("      AEROCARGO-MATRIX: AUDITORÍA DE CARGA Y BALANCE     ")
    print("=========================================================")

    # Datos de prueba: Matriz de 3 filas (longitudinal) por 4 columnas (transversal)
    cargas_reales = [
        [500.0, 450.0, 480.0, 520.0],
        [600.0, 850.0, 300.0, 400.0],  # Celda (1,1) está sobrecargada
        [400.0, 420.0, 410.0, 430.0]
    ]

    capacidades_maximas = [
        [600.0, 600.0, 600.0, 600.0],
        [600.0, 700.0, 600.0, 600.0],
        [500.0, 500.0, 500.0, 500.0]
    ]

    tolerancia_desbalance_kg = 150.0

    # 1. Validación de matrices
    es_valida = validar_matriz_coherencia(cargas_reales, capacidades_maximas)
    print(f"\n[1] Validación de Coherencia Dimensional: {'APROBADA' if es_valida else 'RECHAZADA'}")

    if not es_valida:
        print("Error: Las matrices ingresadas no son válidas. Abortando auditoría.")
        return

    imprimir_matriz("Matriz de Cargas Reales (kg)", cargas_reales)
    imprimir_matriz("Matriz de Capacidades Máximas (kg)", capacidades_maximas)

    # 2. Porcentajes de Ocupación y Sobrecargas
    matriz_ocup, sobrecargas = calcular_ocupacion_sobrecargas(cargas_reales, capacidades_maximas)
    imprimir_matriz("Matriz de Porcentajes de Ocupación", matriz_ocup, es_porcentaje=True)

    print(f"\n[2] Detección de Sobrecargas (> 100.0%):")
    if sobrecargas:
        for f, c in sobrecargas:
            print(f"    CRÍTICO: Celda en fila {f}, columna {c} con {matriz_ocup[f][c]}% de ocupación.")
    else:
        print("    OK: No se detectaron celdas en sobrecarga.")

    # 3. Evaluación de Balance Lateral
    pesos_filas, desbalance_kg, esta_balanceado = evaluar_balance_lateral(cargas_reales, tolerancia_desbalance_kg)
    print(f"\n[3] Auditoría de Balance y Simetría Lateral:")
    print(f"    Vector de Peso Longitudinal (por fila): {pesos_filas} kg")
    print(f"    Desbalance Lateral Calculado: {desbalance_kg} kg (Tolerancia: {tolerancia_desbalance_kg} kg)")
    print(f"    Estado del Balance: {'DENTRO DE NORMA' if esta_balanceado else 'DESBALANCE CRÍTICO'}")

    # 4. Extracción de Submatriz Crítica (Ventana 2x2)
    k, p = 2, 2
    submatriz = extraer_submatriz_critica(matriz_ocup, k, p)
    print(f"\n[4] Extracción de Submatriz Crítica de Zona ({k}x{p}):")
    imprimir_matriz(f"Submatriz de Mayor Concentración ({k}x{p})", submatriz, es_porcentaje=True)

    print("\n=========================================================")
    print("                FIN DEL REPORTE DE AUDITORÍA            ")
    print("=========================================================")

if __name__ == "__main__":
    ejecutar_simulacion() 