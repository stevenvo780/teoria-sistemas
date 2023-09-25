# Integrando todo en un solo script para abordar la Teoría de Sistemas de manera completa

# Importando la biblioteca necesaria
import random
import matplotlib.pyplot as plt
import numpy as np

# Adaptación del código usando clases para una mejor claridad y dinámicas más realistas

# Clase para Agentes con Homeostasis y No Linearidad
class Agent:
    def __init__(self, money, is_employer):
        self.money = money
        self.is_employer = is_employer
        self.previous_money = money

    def work(self, market):
        earnings = (market.money * 0.01)**0.5 if self.is_employer else (market.money * 0.005)**0.5
        self.money += earnings
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

# Clase para el Mercado
class Market:
    def __init__(self, initial_money):
        self.money = initial_money

    def add_money(self, amount):
        self.money += amount

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

        # Redistribución federal y regional
        for agent in agents:
            agent.money += (total_tax + regional_tax) / len(agents)

# Parámetros e inicialización
N = 100
T = 500
initial_market_money = 5000

# Inicializar agentes y mercado con las clases corregidas
agents = [Agent(money=random.randint(20, 100), is_employer=random.choice([True, False])) for _ in range(N)]
market = Market(initial_money=initial_market_money)
government = Government()

# Listas para rastrear la riqueza total
total_employer_wealth = []
total_employee_wealth = []

# Simulación con lógicas adaptadas
for t in range(T):
    if t % 50 == 0:
        market.add_money(500)
    
    for agent in agents:
        agent.work(market)
        agent.consume(market)
        agent.adapt()
    government.tax_and_redistribute(agents)
    
    # Rastreo de la riqueza total
    total_employer_wealth.append(sum(agent.money for agent in agents if agent.is_employer))
    total_employee_wealth.append(sum(agent.money for agent in agents if not agent.is_employer))

# Gráfico para visualizar la dinámica de la riqueza en el sistema
plt.figure(figsize=(10, 5))
plt.plot(range(T), total_employer_wealth, label='Total Employer Wealth')
plt.plot(range(T), total_employee_wealth, label='Total Employee Wealth')
plt.xlabel('Turn')
plt.ylabel('Total Wealth')
plt.legend()
plt.title('Adapted System Dynamics')
plt.show()
