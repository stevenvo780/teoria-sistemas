# Mejorando el modelo y la visualización para abordar la Teoría de Sistemas de manera más completa

import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Adaptación del código usando clases para una mejor claridad y dinámicas más realistas

# Clase para Agentes con Homeostasis, No Linearidad, y Cooperación


class Agent:
    def __init__(self, money, is_employer, cooperation_index):
        self.money = money
        self.is_employer = is_employer
        self.previous_money = money
        self.cooperation_index = cooperation_index  # Nuevo: índice de cooperación

    def work(self, market):
        earnings = (
            market.money * 0.01)**0.5 if self.is_employer else (market.money * 0.005)**0.5
        self.money += earnings * self.cooperation_index  # Nuevo: efecto de la cooperación
        market.money -= earnings

    def consume(self, market):
        expense = np.log(self.money) * 0.1
        if self.money > expense:
            self.money -= expense
            market.add_money(expense)

    def adapt(self):
        if self.money < self.previous_money * 0.9:
            self.is_employer = False
        elif self.money > self.previous_money * 1.1:
            self.is_employer = True
        self.previous_money = self.money

    def cooperate(self, other):  # Nuevo: función de cooperación
        cooperation_gain = self.money * 0.01 * self.cooperation_index
        self.money += cooperation_gain
        other.money += cooperation_gain

# Clase para el Mercado con mecanismo de ajuste


class Market:
    def __init__(self, initial_money):
        self.money = initial_money

    def add_money(self, amount):
        self.money += amount

    def adjust_conditions(self):  # Nuevo: ajuste del mercado
        if self.money < 2000:
            self.add_money(500)
        elif self.money > 8000:
            self.money -= 500

# Clase para el Gobierno con jerarquía (Impuestos regionales y federales)


class Government:
    def tax_and_redistribute(self, agents):
        total_tax = 0
        regional_tax = 0

        for agent in agents:
            tax = agent.money * 0.07  # Impuesto federal
            regional = agent.money * 0.03  # Impuesto regional
            agent.money -= (tax + regional)
            total_tax += tax
            regional_tax += regional

        for agent in agents:
            agent.money += (total_tax + regional_tax) / len(agents)


# Parámetros e inicialización
N = 100
T = 500
initial_market_money = 5000

# Inicializar agentes y mercado con las clases corregidas
agents = [Agent(money=random.randint(20, 100), is_employer=random.choice(
    [True, False]), cooperation_index=random.uniform(0.8, 1.2)) for _ in range(N)]
market = Market(initial_money=initial_market_money)
government = Government()

# Listas para rastrear la riqueza y satisfacción total
total_employer_wealth = []
total_employee_wealth = []
total_satisfaction = []  # Nuevo: Satisfacción total en el sistema

# Simulación con lógicas adaptadas
for t in range(T):
    market.adjust_conditions()

    # Cooperación entre agentes (Nuevo)
    for i in range(0, len(agents), 2):
        agents[i].cooperate(agents[i+1])

    for agent in agents:
        agent.work(market)
        agent.consume(market)
        agent.adapt()
    government.tax_and_redistribute(agents)

    total_employer_wealth.append(
        sum(agent.money for agent in agents if agent.is_employer))
    total_employee_wealth.append(
        sum(agent.money for agent in agents if not agent.is_employer))
    total_satisfaction.append(
        sum(agent.money * agent.cooperation_index for agent in agents))  # Nuevo

# Gráfico 3D para visualizar la dinámica en el sistema
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(range(T), total_employer_wealth, total_satisfaction,
        label='Employer Wealth vs Satisfaction')
ax.plot(range(T), total_employee_wealth, total_satisfaction,
        label='Employee Wealth vs Satisfaction')
ax.set_xlabel('Turn')
ax.set_ylabel('Total Wealth')
ax.set_zlabel('Total Satisfaction')
ax.legend()
plt.title('Advanced System Dynamics')
plt.show()
