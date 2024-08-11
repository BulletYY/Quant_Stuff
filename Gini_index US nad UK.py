from pygini import gini
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def generate_data(start, koniec, krok):
    return [(i, j) for i, j in zip(range(start, koniec + 1, krok), range(1, ((koniec - start) // krok) + 2))]

def lorenz_curve(data):
    data = sorted(data, key=lambda x: x[0])
    xi, yi = zip(*data)

    weighted_xi = np.array(xi) * np.array(yi)
    cum_weighted_xi = np.cumsum(weighted_xi)
    cum_yi = np.cumsum(yi)

    cum_weighted_xi_norm = cum_weighted_xi / cum_weighted_xi[-1]
    cum_yi_norm = cum_yi / cum_yi[-1]

    cum_weighted_xi_norm = np.insert(cum_weighted_xi_norm, 0, 0)
    cum_yi_norm = np.insert(cum_yi_norm, 0, 0)

    return cum_yi_norm, cum_weighted_xi_norm

def gini_coefficient(lorenz_x, lorenz_y):
    lorenz_area = np.trapz(lorenz_y, lorenz_x)
    return 1 - 2 * lorenz_area

start = 10
end = 600
step = 10

# Generowanie danych
data = generate_data(start, end, step)

# Obliczanie krzywej Lorenza
lorenz_x, lorenz_y = lorenz_curve(data)

# Rysowanie krzywej Lorenza
plt.figure(figsize=(8, 8))
plt.plot(lorenz_x, lorenz_y, marker='o', linestyle='-',
         color='blue', label='Lorenz Curve')
plt.plot([0, 1], [0, 1], linestyle='--', color='black', label='Ideal Scenario')
plt.xlabel('Cumulative % of Population')
plt.ylabel('Cumulative % of Income')
plt.title('Lorenz Curve Compared to Theoretical Ideal Scenario')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Obliczanie współczynnika Giniego
gini_computed = gini_coefficient(lorenz_x, lorenz_y)
print(f"Gini coefficient {gini_computed:.4f}")
# generuje mi moje dane i zlicza od start  co podany step
data = generate_data(start, end, step)

# print(data)

# WAZNE ! do dalszych rozważań będe używał już giniego liczonego za pomocą paczki pygini

# obliczanie cumm income. dtype bo gini oczekuje danych typu float64
incomes = np.array([x * y for x, y in data], dtype=np.float64)

# print(incomes)

gini_coefficient = gini(incomes)
print(f"Gini Coefficient: {gini_coefficient:.4f}")

# Wczytanie danych
data = pd.read_csv(
    r"C:\Users\Bullet\OneDrive\Pulpit\databases\Real_Disposable_income.csv")

# print(data.head())


def lorenz_curve(data):
    population_share = np.arange(1, len(data) + 1) / len(data)

    data_sorted = data.sort_values(by='DSPIC96')

    income_share = np.cumsum(
        data_sorted['DSPIC96']) / np.sum(data_sorted['DSPIC96'])

    return population_share, income_share


lorenz_x, lorenz_y = lorenz_curve(data)

plt.figure(figsize=(8, 8))
plt.plot(lorenz_x, lorenz_y, marker='o', linestyle='-',
         color='b', label='Lorenz Curve')
plt.plot([0, 1], [0, 1], linestyle='--', color='black', label='Ideal Scenario')
plt.xlabel('Cumulative % of Population')
plt.ylabel('Cumulative % of Disposable Income')
plt.title('Lorenz Curve for Disposable Income')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

def lorenz_curve(data):
    sorted_data = np.sort(data)
    n = len(data)
    cumulative_sum = np.cumsum(sorted_data)
    cumulative_percent = np.arange(1, n + 1) / n * 100  # Procentowy udział populacji

    return cumulative_percent, cumulative_sum / cumulative_sum[-1]  # Cumulative sum normalizowany do sumy całkowitej

# Dane wejściowe
data = np.array([4_398, 10_826, 16_653, 23_638, 30_290, 38_043, 46_812, 57_983, 73_031, 141_200, 44_287]) # zrodlo dane wziete https://www.ons.gov.uk/ to jest wektor danych tez dla disposable income given in deciles

# https://docs.google.com/spreadsheets/d/1ujEUZ8T1Kgs93nGGJLqjmsCJRNWdHmxTydZfFnIs4bU/edit?gid=10661742#gid=10661742

# Obliczenie krzywej Lorenza
lorenz_x, lorenz_y = lorenz_curve(data)

# Obliczenie współczynnika Giniego
def gini_coefficient_2(data):
    sorted_data = np.sort(data)
    n = len(data)
    sum_xi = np.sum(sorted_data)
    
    gini = 1 - (2 * np.sum((n + 1 - np.arange(1, n + 1)) * sorted_data)) / (n * sum_xi)
    
    return gini

gini_coeff = gini_coefficient_2(data)
print(f"Gini Coefficient: {gini_coeff:.4f}")