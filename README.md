# Sistema Económico Simulado: Un Enfoque desde la Teoría de Sistemas

## Introducción

Este repositorio contiene un modelo de simulación de un sistema económico. El modelo está diseñado para ilustrar varios conceptos de la Teoría de Sistemas, incorporando principios como dinámicas no lineales, homeostasis, adaptabilidad, cooperación, y jerarquía. A continuación, se detallan los aspectos fundamentales de este enfoque.

## Conceptos de Teoría de Sistemas Incorporados

### 1. Interconexión de Componentes

- Los agentes, el mercado y el gobierno están interconectados. Los agentes interactúan entre sí y también con el mercado y el gobierno.

### 2. Homeostasis

- El método `adjust_conditions` en la clase `Market` busca mantener el sistema dentro de ciertos límites, lo cual es un ejemplo de homeostasis.

### 3. Adaptabilidad

- Los agentes cambian su rol (`is_employer`) en función de su riqueza, mostrando adaptabilidad.

### 4. Emergencia

- El sistema como un todo exhibe comportamientos que no son evidentes a partir de sus componentes individuales, como la redistribución de la riqueza y la cooperación.

### 5. Propósito o Función

- El sistema tiene un objetivo implícito de simular una economía con agentes que trabajan, consumen, cooperan y compiten.

### 6. Entropía

- El sistema intenta reducir la entropía a través de la redistribución de impuestos y ajustes en las condiciones del mercado.

### 7. Retroalimentación

- Los agentes reciben retroalimentación del mercado y del gobierno, lo cual afecta su comportamiento en futuras iteraciones.

### 8. No-Linearidad

- Las funciones de utilidad y ganancia son no-lineales (raíz cuadrada y logaritmo).

### 9. Jerarquía

- Existe una jerarquía en la forma de un gobierno que impone impuestos y redistribuye la riqueza.

### 10. Cooperación y Competencia

- Los agentes en el sistema tanto cooperan como compiten entre ellos, lo cual es crucial para la teoría de sistemas.

### 11. Flujos de Información y Recursos

- Hay un flujo constante de recursos (dinero) e información (estado del agente y del mercado) en el sistema.

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

\`\`\`bash
python teoria_sistemas.py
\`\`\`

Esto generará gráficos que ilustran la evolución del sistema a lo largo del tiempo.

## Contribuciones

Siéntase libre de contribuir al proyecto y mejorar la simulación o la visualización de los datos.
