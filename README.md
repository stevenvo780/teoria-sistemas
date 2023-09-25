# Sistema Económico Simulado: Un Enfoque desde la Teoría de Sistemas

## Introducción

Este repositorio contiene un modelo de simulación de un sistema económico. El modelo está diseñado para ilustrar varios conceptos de la Teoría de Sistemas, incorporando principios como dinámicas no lineales, homeostasis, adaptabilidad, cooperación, y jerarquía. A continuación, se detallan los aspectos fundamentales de este enfoque.

## Conceptos de Teoría de Sistemas Incorporados

### 1. Dinámicas No Lineales

Los agentes en el sistema tienen ingresos y gastos que no son lineales, reflejando las realidades complejas de las economías modernas.

### 2. Homeostasis

Los agentes se adaptan a su entorno cambiando su estado de "empleador" a "empleado" y viceversa, buscando un equilibrio que les permita sobrevivir y prosperar.

### 3. Adaptabilidad y Aprendizaje

Los agentes utilizan información sobre su riqueza anterior para adaptarse y cambiar su estado, ilustrando el concepto de aprendizaje y adaptabilidad en sistemas complejos.

### 4. Cooperación y Competencia

Los agentes interactúan entre sí de manera cooperativa y competitiva, lo que añade otra capa de complejidad al sistema.

### 5. Jerarquía

El sistema incluye un modelo simplificado de un gobierno que impone impuestos a diferentes niveles (federal y regional), añadiendo una estructura jerárquica al sistema.

### 6. Interconexiones y Redes

Los agentes en el sistema no sólo interactúan con el mercado sino también entre sí y con una entidad de gobierno, formando una red interconectada de relaciones.

### 7. Flujo de Información

El estado y las decisiones de los agentes se basan en el flujo de información a través del sistema, que en este caso es su riqueza anterior y la riqueza del sistema en general.

### 8. Emergencia

El sistema como un todo exhibe patrones y comportamientos que no son evidentes a nivel de los agentes individuales, un fenómeno conocido como emergencia en la Teoría de Sistemas.

## Estructura del Código

El código está organizado en clases para representar diferentes entidades en el sistema:

- `Agent`: Representa a los agentes individuales en el sistema.
- `Market`: Modela el mercado donde los agentes interactúan.
- `Government`: Simula un gobierno que impone impuestos y redistribuye la riqueza.

Cada clase tiene métodos que modelan las actividades y decisiones de las entidades, como `work`, `consume`, `adapt`, `cooperate`, y `tax_and_redistribute`.

## Visualización

Se utiliza una visualización en 3D para representar múltiples aspectos del sistema simultáneamente, incluida la riqueza total de los empleadores y empleados, así como la "satisfacción" en el sistema, que es un producto de la riqueza y el índice de cooperación.

## Cómo Ejecutar el Código

Puede ejecutar el código usando Python 3.x. Asegúrese de tener instaladas las bibliotecas necesarias (`matplotlib`, `numpy` y `seaborn`).

```bash
python teoria_sistemas.py
```

Esto generará gráficos que ilustran la evolución del sistema a lo largo del tiempo.

## Contribuciones

Siéntase libre de contribuir al proyecto y mejorar la simulación o la visualización de los datos.
