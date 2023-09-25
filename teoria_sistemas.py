import random
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# Class for Agents with Homeostasis, Non-linearity, Cooperation and Competition
class Agent:
    def __init__(self, money, is_employer, cooperation_index):
        self.money = money
        self.is_employer = is_employer
        self.previous_money = money
        self.cooperation_index = cooperation_index

    def work(self, market):
        # Introducing competition: agents compete for a limited resource in the market
        available_resource = market.money * \
            0.01 if self.is_employer else market.money * 0.005
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

    def compete(self, other):  # New: competition function
        if self.money > other.money:
            self.money += 10
            other.money -= 10

# Class for the Market with adjustment mechanism
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

# Class for the Government with hierarchy (Regional and Federal Taxes)
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


# Parameters and Initialization
N = 100
T = 500
initial_market_money = 5000

# Initialize agents and market with the corrected classes
agents = [Agent(money=random.randint(20, 100), is_employer=random.choice(
    [True, False]), cooperation_index=random.uniform(0.8, 1.2)) for _ in range(N)]
market = Market(initial_money=initial_market_money)
government = Government()

# Lists to track total wealth and satisfaction
total_employer_wealth = []
total_employee_wealth = []
total_satisfaction = []

# Simulation with adapted logics
for t in range(T):
    market.adjust_conditions()

    # Competition between agents
    for i in range(0, len(agents), 2):
        agents[i].compete(agents[i + 1])

    # Cooperation between agents
    for i in range(0, len(agents), 2):
        agents[i].cooperate(agents[i + 1])

    for agent in agents:
        agent.work(market)
        agent.consume(market)
        agent.adapt()
    government.tax_and_redistribute(agents)

    # Tracking total wealth and satisfaction
    total_employer_wealth.append(
        sum(agent.money for agent in agents if agent.is_employer))
    total_employee_wealth.append(
        sum(agent.money for agent in agents if not agent.is_employer))
    total_satisfaction.append(
        sum(agent.money * agent.cooperation_index for agent in agents))

# 3D Visualization
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot(range(T), total_employer_wealth, zs=0,
        zdir='z', label='Total Employer Wealth')
ax.plot(range(T), total_employee_wealth, zs=1,
        zdir='z', label='Total Employee Wealth')
ax.plot(range(T), total_satisfaction, zs=2,
        zdir='z', label='Total Satisfaction')
ax.set_xlabel('Turn')
ax.set_ylabel('Z-axis')
ax.set_zlabel('Total Wealth/Satisfaction')
plt.title('System Dynamics with Competition and Cooperation')
plt.legend()
plt.show()
