# Manteniendo la estructura del código previo y continuando con las mejoras en visualización y análisis

import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Agent:
    def __init__(self, money, is_employer, cooperation_index):
        self.money = money
        self.is_employer = is_employer
        self.previous_money = money
        self.cooperation_index = cooperation_index

    def work(self, market):
        earnings = (
            market.money * 0.01)**0.5 if self.is_employer else (market.money * 0.005)**0.5
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


N = 100
T = 500
initial_market_money = 5000

agents = [Agent(money=random.randint(20, 100), is_employer=random.choice([True, False]),
                cooperation_index=random.uniform(0.8, 1.2)) for _ in range(N)]
market = Market(initial_money=initial_market_money)
government = Government()

total_employer_wealth = []
total_employee_wealth = []
total_cooperation = []

for t in range(T):
    market.adjust_conditions()

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
    total_cooperation.append(
        sum(agent.cooperation_index for agent in agents)/N)

# 3D plot for enhanced visualization
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

x = np.linspace(1, T, T)
ax.plot(x, total_employer_wealth, zs=0,
        zdir='z', label='Total Employer Wealth')
ax.plot(x, total_employee_wealth, zs=1,
        zdir='z', label='Total Employee Wealth')
ax.plot(x, total_cooperation, zs=2, zdir='z', label='Avg Cooperation Index')

ax.set_xlabel('Time')
ax.set_ylabel('Z-Direction')
ax.set_zlabel('Wealth/Cooperation')
ax.legend()
plt.title('Adapted System Dynamics with 3D Visualization')
plt.show()
