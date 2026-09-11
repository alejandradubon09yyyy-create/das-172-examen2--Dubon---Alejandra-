"""
Módulo de Pruebas Unitarias para AeroCargo-Matrix
Cubre casos típicos y casos de borde/límite según los requerimientos académicos.
"""

import unittest
from aerocargo import (
    validar_matriz_coherencia,
    calcular_ocupacion_sobrecargas,
    evaluar_balance_lateral,
    extraer_submatriz_critica
)

class TestAeroCargo(unittest.TestCase):

    # --- 1. PRUEBAS DE VALIDACIÓN Y COHERENCIA DIMENSIONAL ---

    def test_01_validacion_correcta_matriz_valida(self):
        """Caso Típico: Matrices de 2x2 válidas con valores positivos."""
        cargas = [[100.0, 200.0], [300.0, 400.0]]
        capacidades = [[500.0, 500.0], [500.0, 500.0]]
        self.assertTrue(validar_matriz_coherencia(cargas, capacidades))

    def test_02_validacion_error_dimensiones_menores_a_minimo(self):
        """Caso Borde: Matriz menor a 2x2 (ej. 1x2) debe ser rechazada."""
        cargas = [[100.0, 200.0]]
        capacidades = [[500.0, 500.0]]
        self.assertFalse(validar_matriz_coherencia(cargas, capacidades))

    def test_03_validacion_error_matriz_irregular_o_dimensiones_distintas(self):
        """Caso Borde: Matriz de carga y capacidad con dimensiones no coincidentes."""
        cargas = [[100.0, 200.0], [300.0, 400.0]]
        capacidades = [[500.0, 500.0]]  # Le falta una fila
        self.assertFalse(validar_matriz_coherencia(cargas, capacidades))


    # --- 2. PRUEBAS DE OCUPACIÓN Y DETECCIÓN DE SOBRECARGA ---

    def test_04_calculo_ocupacion_y_deteccion_sobrecarga(self):
        """Caso Típico: Cálculo correcto de % y detección de celda > 100.0%."""
        cargas = [[600.0, 200.0], [100.0, 400.0]]
        capacidades = [[500.0, 500.0], [500.0, 500.0]]
        matriz_p, sobrecargas = calcular_ocupacion_sobrecargas(cargas, capacidades)
        
        # Celda (0,0): 600/500 * 100 = 120.0% -> Sobrecargada
        self.assertEqual(matriz_p[0][0], 120.0)
        self.assertEqual(sobrecargas, [(0, 0)])


    # --- 3. PRUEBAS DE BALANCE Y SIMETRÍA LATERAL ---

    def test_05_balance_lateral_columnas_pares(self):
        """Caso Típico: Matriz con N=2, M=2 (columnas pares)."""
        cargas = [[100.0, 100.0], [200.0, 200.0]]
        # Izquierda: 100+200=300, Derecha: 100+200=300 -> Desbalance = 0.0
        pesos, desbalance, balanceado = evaluar_balance_lateral(cargas, tolerancia_kg=50.0)
        self.assertEqual(desbalance, 0.0)
        self.assertTrue(balanceado)

    def test_06_balance_lateral_columnas_impares_omite_columna_central(self):
        """Caso Borde: M=3 (impar). La columna central (índice 1) debe ignorarse."""
        cargas = [
            [100.0, 999.0, 100.0],
            [200.0, 888.0, 200.0]
        ]
        # Babor: 100+200=300, Estribor: 100+200=300. La central (999, 888) se omite.
        pesos, desbalance, balanceado = evaluar_balance_lateral(cargas, tolerancia_kg=10.0)
        self.assertEqual(desbalance, 0.0)
        self.assertTrue(balanceado)


    # --- 4. PRUEBAS DE EXTRACCIÓN DE SUBMATRIZ CRÍTICA ---

    def test_07_extraccion_submatriz_critica_exitosa(self):
        """Caso Típico: Extrae la submatriz k x p con el mayor promedio de ocupación."""
        matriz_ocupacion = [
            [10.0, 20.0, 30.0],
            [40.0, 150.0, 160.0],
            [50.0, 140.0, 170.0]
        ]
        submatriz = extraer_submatriz_critica(matriz_ocupacion, k=2, p=2)
        esperada = [
            [150.0, 160.0],
            [140.0, 170.0]
        ]
        self.assertEqual(submatriz, esperada)

    def test_08_submatriz_dimensiones_invalidas(self):
        """Caso Borde: Solicitar una submatriz más grande que la matriz original."""
        matriz_ocupacion = [[50.0, 50.0], [50.0, 50.0]]
        submatriz = extraer_submatriz_critica(matriz_ocupacion, k=3, p=3)
        self.assertEqual(submatriz, [])

if __name__ == "__main__":
    unittest.main() 