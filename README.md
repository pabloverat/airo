# airo

## Descripción del proyecto
Lenguaje de programación  imperativo que se desarrolla como parte del curso Diseño de Compiladores en el programa de Ingeniería de Tecnologías Computacionales.

---

## Bitácora de desarrollo

**ENTREGA FINAL** : Lunes 5 de junio, 1:00pm

### Semáforo de actividades por avance

    🟢 Done
    🟡 Doing
    🔴 To Do - Late
    ⚪ To Do - On Time

#### Avance 0
    🟢 Tokens
    🟢 Diagramas de Sintaxis
    🟢 Gramática

#### Avance 1
    🟢 Análisis de Léxico y Sintaxis

#### Avance 2
    🟢 Semántica Básica de Variables
    🟢 Semántica Básica de Expresiones

#### Avance 3
    🟢 Generación de Código de Expresiones Aritméticas y estatutos secuenciales

#### Avance 4
    🟢 Generación de Código de Estatutos Condicionales (Decisiones)
    🟢 Generación de Código de Estatutos Condicionales (Ciclos)

#### Avance 5
    🟢 Generación de Código de Funciones

#### Avance 6
    🟢 Mapa de Memoria de Ejecución para la Máquina Virtual
    🟢 Máquina Virtual: Ejecución de Expresiones aritméticas

#### Avance 7
    🔴 Generación de Código de Arreglos / Tipos estructurados
    🟢 Máquina Virtual: ejecución de estatutos secuenciales y condicionales

#### Avance 8
    🔴 1era versión de Documentación
    🟡 Máquina virtual: ejecución de módulos y arreglos
    🔴 Generación de código y Máquina virtual para una parte de la aplicación

### Actividades realizadas
% de complitud

- 30-Abril
    - 100% Selección de proyecto, creación de repositorio, etc.
    - 25% Avance 0: Propuesta y consideraciones semánticas.  

- 01-Mayo
    - 75% Avance 0: Diagrama de sintaxis.  
    - 100% Avance 0: Gramatica

- 02-Mayo
    - 99% Avance 1: Lexer done, parser done  (More testing pending!)

- 03-Mayo
    - 100% Avance 1: Más pruebas a Análisis sintáctico, bug fixes

- 04-Mayo
    - 25% Avance 2: primera iteración de tabla de variables, ya las guarda por separado en un dict de globales y otro de locales y les asigna una "dirección virtual" según ciertos rangos definidos en el init

- 09-Mayo
    - 50% Avance 2:
    - Refactorización de tabla de variables para que haya un objeto de tabla por función (globales se incluye en directorio de funciones).
    - Implementación de directorio de funciones: ya guarda tipo de función, lista de recursos con los tipos y lista de params con los tipos
    - Falta implementar cuádruplos para indicar dirección de inicio de las funciones.

- 10-Mayo
    - 75% Avance 2:
    - Definición cubo semántico
    - Falta implementar validación semántica en cuádruplos

- 11-Mayo
    - bug fix: antes no se podía hacer operaciones entre llamadas a función y ya se puede, se eliminaron las variables booleanas y las operaciones entre ellas (AND, OR, NOT)
    - 100% Avance 2: dirFunc, varTable y Cubo Semántico listo

- 12-Mayo
    - 20% Avance 3: primera iteración cuádruplos para expresiones, ya se generan operador y operandos falta dónde se van a guardar y temporales.

- 13-Mayo
    - 60% Avance 3:
        - ya se guardan temporales
        - listos cuádruplos para +, -, * y /
        - ya se hace el primer goto a main
        - falta código para el resto de las operaciones lineales(asignar, lectura, etc).

- 14-Mayo
    - 90% Avance 3:
        - listos cuádruplos para <, >, =<, =>, ==, !=
        - listo cuádruplo para asignar, escribir
        - falta código para leer

- 15-Mayo
    - 100% Avance 3:
        - listo cuádruplos para lectura read()
        - limpieza de código
        - falta agregar comentarios al código en gral

- 16-Mayo
    - 50% Avance 4:
        - cuádruplos para if e if-else listos
        - agregué type checking que faltaba al asignar

- 17-Mayo
    - 100% Avance 4:
        - avance completado
        - cuádruplos para while listos (saltos de gotof y goto de vuelta)

- 19-Mayo
    - 25% Avance 5:
        - agregué dirInicio a funciones
        - puntos neurálgicos y cuadruplos para declaración funciones

- 21-Mayo
    - 100% Avance 5:
        - avance completado
        - puntos neurálgicos y cuadruplos para llamada a funciones

- 22-Mayo
    - 10% Avance 6:
        - agregué tabla de constantes: diccionario que indexa una tupla con una dirección dentro de un rango predeterminado y el tipo de la constante

- 28-Mayo
    - 20% Avance 6:
        - ahora se generan los cuádruplos con direcciones, también se siguen generando con nombres para debugging
    
- 29-Mayo
    - 30% Avance 6:
        - se genera el archivo ovejota y se recrean cuadruplos, dirFuncs y constsTable desde maq virtual

- 02-Junio
    - 100% Avance 6:
        - mapa de memoria creado con una clase que tiene dos diccionarios: uno con listas para guardar los valores que estarán en la memoria, y uno con las direcciones base
        - ya hace operaciones binarias

- 03-Junio
    - 50% Avance 7:
        - la máquina virtual ya ejecuta cuádruplos para estatutos secuenciales, condicionales y ciclos.
    - 25% Avance 8:
        - implementación de pila de memorias para recursión
        - la máquina virtual ya ejecuta cuádruplos para módulos tipo void 
        - prueba de recursión con void 'tests/test_void2.ld' completada

- 04-Junio
    - 33% Avance 8:
        - la máquina virtual ya ejecuta cuádruplos para módulos con return
        - pruebas de recursión fibonacci y factorial completadas