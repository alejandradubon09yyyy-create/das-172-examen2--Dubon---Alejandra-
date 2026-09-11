AeroCargo-Matrix

Auditoría y Balance Matricial de Distribución de Carga en Bahía de Aeronave.

I. Explicación del Problema
¿Por qué importa el balance de masa y la capacidad de piso?

Cuando un avión de carga se llena, no basta con que la carga total "quepa" o no supere el peso máximo del avión. Importan dos cosas más, y ambas pueden causar un accidente si se ignoran:

1. Capacidad del piso (por celda, no en general)

El piso de la bodega no es una superficie uniforme: está dividido en secciones, y cada sección soporta un peso máximo distinto. Es como un elevador de edificio: que el peso total de las personas esté dentro del límite no sirve de nada si todas se paran sobre el mismo punto del piso. Si una sola celda recibe más peso del que su estructura tolera, esa zona del fuselaje se puede deformar o fallar, aunque el resto del avión esté perfectamente cargado.

Por eso el sistema no solo suma pesos: calcula, celda por celda, qué porcentaje de su capacidad está usando cada compartimiento:

%Ocupación(i,j) = ( PesoReal(i,j) / CapacidadMáxima(i,j) ) × 100

Si ese porcentaje pasa de 100%, esa celda está sobrecargada, sin importar cómo esté el resto del avión.

2. Balance y simetría (izquierda-derecha, adelante-atrás)

Un avión no vuela como un bloque rígido: se comporta como una balanza. Si un lado (babor) pesa mucho más que el otro (estribor), el avión tiende a inclinarse hacia ese lado, y el piloto tiene que compensarlo constantemente con los controles. En vuelos cortos es incómodo; en condiciones críticas (despegue, turbulencia, un motor fallando) puede ser peligroso y reduce la maniobrabilidad.

Por eso se calcula el desbalance lateral:

DesbalanceLateral = | SumaPesoMitadIzquierda − SumaPesoMitadDerecha |

y se compara contra una tolerancia máxima aceptable. Si el número de columnas es impar, la columna central se descarta del cálculo porque está exactamente sobre el eje de simetría del avión — no le "pertenece" a ningún lado.

En resumen: el sistema no solo pregunta "¿cabe el peso?", sino "¿está bien repartido, punto por punto y lado por lado?" — porque una carga mal distribuida puede ser tan peligrosa como una carga excesiva.

II. Diagrama de Arquitectura Modular

La solución sigue un patrón simple: un script principal orquesta llamadas a módulos puros, y cada módulo solo recibe datos, los procesa, y devuelve un resultado — nunca modifica lo que recibe ni depende de variables externas.


II. Diagrama de Arquitectura Modular

La solución sigue un patrón modular basado en funciones puras e inmutabilidad: el script principal (`main.py`) orquesta las llamadas a cada módulo, pasando matrices como argumentos y recibiendo nuevas estructuras sin alterar los datos originales.

```text
               +----------------------------------+
               |        main.py / Script          |
               +----------------------------------+
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
+------------------+  +-------------------+  +--------------------+
|  validar_matriz  |  | calcular_ocupacion|  | evaluar_balance    |
|   _coherencia    |  |   _sobrecargas    |  |     _lateral       |
+------------------+  +-------------------+  +--------------------+
        |                       |                       |
   [Bool/Valid]        [MatrizOcupacion %]     [VectorPesosFilas]
                       [ListaSobrecargas]      [DesbalanceKg, Bool]
                                                        |
                                                        v
                                             +--------------------+
                                             | extraer_submatriz  |
                                             |     _critica       |
                                             +--------------------+
                                                        |
                                               [Submatriz k x p]



III. Análisis de Complejidad Computacional
¿Por qué O(N × M) en tiempo?

Piensa en la matriz como una hoja de cálculo con N filas y M columnas, es decir, N × M celdas en total. Casi todas las operaciones del sistema (calcular el porcentaje de ocupación, sumar pesos por fila, buscar submatrices) necesitan visitar cada celda al menos una vez para poder usarla en un cálculo.

No hay forma de saber si la celda (3,5) está sobrecargada sin leer esa celda.
No hay forma de sumar el peso de una fila sin leer cada una de sus columnas.

Como cada celda se visita una cantidad de veces que no depende del tamaño de la matriz (se lee, se calcula un porcentaje, se compara — trabajo constante por celda), el tiempo total de ejecución crece de forma directamente proporcional al número de celdas: si duplicas N o M, duplicas aproximadamente el trabajo. Eso es exactamente lo que significa O(N × M): "el trabajo crece al mismo ritmo que el total de celdas."

(La búsqueda de la submatriz crítica del Módulo 4 técnicamente revisa varias posiciones de ventana, pero conceptualmente sigue el mismo principio: el costo está atado al tamaño de la cuadrícula que se recorre, no a un factor externo.)

¿Por qué O(N × M) en memoria?

Cada vez que el sistema necesita generar una matriz nueva — por ejemplo, la matriz de porcentajes de ocupación del Módulo 2 — tiene que guardar un valor por cada una de las N × M celdas originales, porque el resultado tiene exactamente la misma forma que la entrada. No se puede comprimir esa información sin perderla: cada celda de la matriz de entrada tiene un porcentaje correspondiente que hay que conservar.

Por eso el espacio adicional que se usa (memoria auxiliar) también crece en proporción directa al tamaño de la matriz: O(N × M). Es el mismo argumento que en tiempo, pero aplicado a "cuánto espacio ocupa lo que guardamos" en lugar de "cuánto tiempo tarda el recorrido".

En una frase para resumir ambos: tanto el tiempo como la memoria son proporcionales al número total de celdas de la matriz, porque el algoritmo necesita tocar y/o duplicar cada celda exactamente una vez para completar su trabajo.

