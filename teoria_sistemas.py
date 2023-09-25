import random
import matplotlib.pyplot as plt

# Definición de clases y funciones


class Agent:
    def __init__(self, money, is_employer):
        self.money = money
        self.is_employer = is_employer

    def work(self, market):
        if self.is_employer:
            # Limitar la extracción al dinero del agente
            market_money = market.extract_money(min(self.money, 30))
            self.money += market_money * random.uniform(0.5, 1.5)
        else:
            self.money += 10 * random.uniform(0.5, 1.5)

    def consume(self, market):
        expense = random.randint(1, 15)
        if self.money > expense:
            self.money -= expense
            market.add_money(expense)

    def adapt(self):
        if self.money < 20:
            self.is_employer = False
        elif self.money > 100:
            self.is_employer = True


class Market:
    def __init__(self, initial_money):
        self.money = initial_money

    def extract_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return amount
        else:
            return 0

    def add_money(self, amount):
        self.money += amount


class Government:
    def tax_and_redistribute(self, agents):
        total_tax = 0
        for agent in agents:
            tax = agent.money * 0.1
            agent.money -= tax
            total_tax += tax
        for agent in agents:
            agent.money += total_tax / len(agents)


# Parámetros iniciales
N = 100
T = 500
initial_market_money = 5000

# Inicialización de agentes y mercado
agents = [Agent(money=random.randint(20, 100),
                is_employer=random.choice([True, False])) for _ in range(N)]
market = Market(initial_money=initial_market_money)
government = Government()

# Listas para rastrear la riqueza total
total_employer_wealth = []
total_employee_wealth = []

# Simulación
for t in range(T):
    for agent in agents:
        agent.work(market)
        agent.consume(market)
        agent.adapt()
    government.tax_and_redistribute(agents)

    # Rastreo de la riqueza total
    total_employer_wealth.append(
        sum(agent.money for agent in agents if agent.is_employer))
    total_employee_wealth.append(
        sum(agent.money for agent in agents if not agent.is_employer))

# Gráfico
plt.figure(figsize=(10, 5))
plt.plot(range(T), total_employer_wealth, label='Riqueza total de Empleadores')
plt.plot(range(T), total_employee_wealth, label='Riqueza total de Empleados')
plt.xlabel('Turno')
plt.ylabel('Riqueza Total')
plt.legend()
plt.title('Dinámica de Riqueza en el Sistema Corregido')
plt.show()
