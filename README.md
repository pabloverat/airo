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
    🟡 Generación de Código de Expresiones Aritméticas y estatutos secuenciales

#### Avance 4
    🔴 Generación de Código de Estatutos Condicionales (Decisiones)
    🔴 Generación de Código de Estatutos Condicionales (Ciclos)

#### Avance 5
    ⚪ Generación de Código de Funciones

#### Avance 6
    ⚪ Mapa de Memoria de Ejecución para la Máquina Virtual
    ⚪ Máquina Virtual: Ejecución de Expresiones aritméticas

#### Avance 7
    ⚪ Generación de Código de Arreglos / Tipos estructurados
    ⚪ Máquina Virtual: ejecución de estatutos secuenciales y condicionales

#### Avance 8
    ⚪ 1era versión de Documentación
    ⚪ Máquina virtual: ejecución de módulos y arreglos
    ⚪ Generación de código y Máquina virtual para una parte de la aplicación

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