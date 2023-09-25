# Implementando mejoras en el modelo y visualización para abordar la Teoría de Sistemas de manera más completa

import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns  # Para heatmaps

# Adaptación del código usando clases para una mejor claridad y dinámicas más realistas

class Agent:
    def __init__(self, money, is_employer, cooperation_index):
        self.money = money
        self.is_employer = is_employer
        self.previous_money = money
        self.cooperation_index = cooperation_index

    def work(self, market):
        # Introduciendo competencia: los agentes compiten por un recurso limitado en el mercado
        available_resource = market.money * 0.01 if self.is_employer else market.money * 0.005
        earnings = min((available_resource)**0.5, self.money * 0.1)
        self.money += earnings * self.cooperation_index
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

    def cooperate(self, other):
        cooperation_gain = self.money * 0.01 * self.cooperation_index
        self.money += cooperation_gain
        other.money += cooperation_gain

class Market:
    def __init__(self, initial_money):
        self.money = initial_money

    def add_money(self, amount):
        self.money += amount

    def adjust_conditions(self):
        if self.money < 2000:
            self.add_money(500)
        elif self.money > 8000:
            self.money -= 500

class Government:
    def tax_and_redistribute(self, agents):
        total_tax = 0
        regional_tax = 0

        for agent in agents:
            tax = agent.money * 0.07
            regional = agent.money * 0.03
            agent.money -= (tax + regional)
            total_tax += tax
            regional_tax += regional

        for agent in agents:
            agent.money += (total_tax + regional_tax) / len(agents)

# Parámetros e inicialización
N = 100
T = 500
initial_market_money = 5000

agents = [Agent(money=random.randint(20, 100), is_employer=random.choice([True, False]), cooperation_index=random.uniform(0.8, 1.2)) for _ in range(N)]
market = Market(initial_money=initial_market_money)
government = Government()

# Listas para rastrear la riqueza y satisfacción total
total_employer_wealth = []
total_employee_wealth = []
total_satisfaction = []

# Simulación con lógicas adaptadas
for t in range(T):
    market.adjust_conditions()

    for i in range(0, len(agents), 2):
        agents[i].cooperate(agents[i + 1])

    for agent in agents:
        agent.work(market)
        agent.consume(market)
        agent.adapt()
    government.tax_and_redistribute(agents)

    total_employer_wealth.append(sum(agent.money for agent in agents if agent.is_employer))
    total_employee_wealth.append(sum(agent.money for agent in agents if not agent.is_employer))
    total_satisfaction.append(sum(agent.money * agent.cooperation_index for agent in agents))

# Mejoras en la visualización
fig = plt.figure(figsize=(18, 6))

# Gráfico 3D para riqueza de empleadores y empleados
ax1 = fig.add_subplot(131, projection='3d')
ax1.scatter(range(T), total_employer_wealth, total_employee_wealth, c=total_satisfaction, cmap='viridis')
ax1.set_xlabel('Time')
ax1.set_ylabel('Total Employer Wealth')
ax1.set_zlabel('Total Employee Wealth')
ax1.set_title('Wealth Dynamics')

# Heatmap para riqueza de empleadores y empleados
ax2 = fig.add_subplot(132)
sns.heatmap([total_employer_wealth, total_employee_wealth], annot=False, ax=ax2, cmap='coolwarm')
ax2.set_title('Wealth Heatmap')
ax2.set_xlabel('Time')
ax2.set_ylabel('Wealth Type')
ax2.set_yticklabels(['Employer', 'Employee'])

# Gráfico 3D para satisfacción total
ax3 = fig.add_subplot(133, projection='3d')
ax3.scatter(range(T), total_satisfaction, total_satisfaction, c=total_satisfaction, cmap='viridis')
ax3.set_xlabel('Time')
ax3.set_ylabel('Total Satisfaction')
ax3.set_zlabel('Total Satisfaction')
ax3.set_title('Satisfaction Dynamics')

plt.show()
