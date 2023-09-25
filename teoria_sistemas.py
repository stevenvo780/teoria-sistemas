import random
import matplotlib.pyplot as plt
import numpy as np

# Clase para representar un agente en el sistema.
# Incorpora conceptos como homeostasis, no-linearidad, cooperación y competencia.
class Agent:
    def __init__(self, money, is_employer, cooperation_index):
        self.money = money  # Dinero inicial del agente
        # Rol inicial del agente en el sistema (empleador o empleado)
        self.is_employer = is_employer
        self.previous_money = money  # Usado para rastrear cambios en la riqueza del agente
        self.cooperation_index = cooperation_index  # Índice de cooperación del agente

    def work(self, market):
        # Seleccionamos una tasa de recurso disponible dependiendo del rol del agente en el sistema.
        available_resource = market.money * \
            0.01 if self.is_employer else market.money * 0.005

        # Las ganancias se modelan usando una raíz cuadrada para representar rendimientos decrecientes del recurso.
        earnings = min((available_resource)**0.5, self.money * 0.1)

        # Aplicamos un coeficiente de cooperación para modelar interacciones sociales.
        self.money += earnings * self.cooperation_index
        market.money -= earnings

    def consume(self, market):
        # Utilizamos una función de utilidad logarítmica para representar el consumo.
        expense = np.log(self.money) * 0.1
        if self.money > expense:
            self.money -= expense
            market.add_money(expense)

    def adapt(self):
        # Los agentes cambian de rol si hay un cambio significativo en su riqueza, ilustrando adaptabilidad.
        if self.money < self.previous_money * 0.9:
            self.is_employer = False
        elif self.money > self.previous_money * 1.1:
            self.is_employer = True
        self.previous_money = self.money

    def cooperate(self, other):
        # La cooperación entre agentes es modelada como un aumento en la riqueza basado en el índice de cooperación.
        cooperation_gain = self.money * 0.01 * self.cooperation_index
        self.money += cooperation_gain
        other.money += cooperation_gain

    def compete(self, other):
        # La competencia es una suma cero donde el agente más rico gana a expensas del más pobre.
        if self.money > other.money:
            self.money += 10
            other.money -= 10

# Clase para el Mercado que modela la disponibilidad de recursos.
class Market:
    def __init__(self, initial_money):
        self.money = initial_money

    def add_money(self, amount):
        self.money += amount

    def adjust_conditions(self):
        # Mecanismo de ajuste para mantener el sistema dentro de ciertos límites.
        if self.money < 2000:
            self.add_money(500)
        elif self.money > 8000:
            self.money -= 500

# Clase para el Gobierno que introduce una jerarquía en el sistema (impuestos regionales y federales).
class Government:
    def tax_and_redistribute(self, agents):
        total_tax = 0
        regional_tax = 0
        for agent in agents:
            # Impuestos federales y regionales son recaudados como porcentaje del dinero del agente.
            tax = agent.money * 0.07
            regional = agent.money * 0.03
            agent.money -= (tax + regional)
            total_tax += tax
            regional_tax += regional

        # Los impuestos recaudados se redistribuyen uniformemente entre los agentes.
        for agent in agents:
            agent.money += (total_tax + regional_tax) / len(agents)


# Parámetros de la simulación y clases iniciales.
N = 100  # Número de agentes
T = 500  # Número de turnos en la simulación
initial_market_money = 5000  # Dinero inicial en el mercado

agents = [Agent(money=random.randint(20, 100), is_employer=random.choice(
    [True, False]), cooperation_index=random.uniform(0.8, 1.2)) for _ in range(N)]
market = Market(initial_money=initial_market_money)
government = Government()

# Listas para rastrear métricas durante la simulación.
total_employer_wealth = []
total_employee_wealth = []
total_satisfaction = []

# La simulación principal que representa la evolución del sistema.
for t in range(T):
    market.adjust_conditions()  # Ajustar las condiciones del mercado

    # Competencia y cooperación entre agentes.
    for i in range(0, len(agents), 2):
        agents[i].compete(agents[i + 1])
        agents[i].cooperate(agents[i + 1])

    # Trabajo, consumo y adaptación de los agentes.
    for agent in agents:
        agent.work(market)
        agent.consume(market)
        agent.adapt()

    government.tax_and_redistribute(agents)  # Impuestos y redistribución

    # Rastrear métricas para análisis posterior.
    total_employer_wealth.append(
        sum(agent.money for agent in agents if agent.is_employer))
    total_employee_wealth.append(
        sum(agent.money for agent in agents if not agent.is_employer))
    total_satisfaction.append(
        sum(agent.money * agent.cooperation_index for agent in agents))

# Visualización en 3D para entender la dinámica del sistema.
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(range(T), total_employer_wealth, zs=0,
        zdir='z', label='Riqueza Total de Empleadores')
ax.plot(range(T), total_employee_wealth, zs=1,
        zdir='z', label='Riqueza Total de Empleados')
ax.plot(range(T), total_satisfaction, zs=2,
        zdir='z', label='Satisfacción Total')
ax.set_xlabel('Turno')
ax.set_ylabel('Eje Z')
ax.set_zlabel('Riqueza/Satisfacción Total')
plt.title('Dinámicas del Sistema con Competencia y Cooperación')
plt.legend()
plt.show()
