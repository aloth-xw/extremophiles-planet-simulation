import pandas as pd
import numpy as np


df = pd.read_csv(r"C:\Users\Laura\OneDrive\Escritorio\extremophiles\extremofilos.csv")

# Planetas/exoplanetas
planet_conditions = {
    "Earth": {"Temperature": 25, "pH": 7, "Pressure": 1, "Salinity": 0.03},
    "Mars": {"Temperature": -60, "pH": 5, "Pressure": 0.006, "Salinity": 0.02},
    "Europa": {"Temperature": -160, "pH": 7, "Pressure": 100, "Salinity": 0.04},
    "Enceladus": {"Temperature": -200, "pH": 7, "Pressure": 0.1, "Salinity": 0.03},
    "Venus": {"Temperature": 465, "pH": 0, "Pressure": 92, "Salinity": 0.01},
    "TRAPPIST-1e": {"Temperature": -10, "pH": 7, "Pressure": 1, "Salinity": 0.03},
    "TRAPPIST-1f": {"Temperature": -60, "pH": 6, "Pressure": 1, "Salinity": 0.03},
    "Kepler-452b": {"Temperature": 22, "pH": 7, "Pressure": 1, "Salinity": 0.03},
    "Proxima_Centauri_b": {"Temperature": -40, "pH": 6, "Pressure": 1, "Salinity": 0.02},
    "Titan_like": {"Temperature": -179, "pH": 6, "Pressure": 1.5, "Salinity": 0.01},
}

#supervivencia
def survival_probability(row, conditions):
    temp = row['Optimal Temperature']
    if isinstance(temp, str) and '-' in temp:
        temp = np.mean([float(x) for x in temp.split('-')])
    try:
        temp = float(temp)
    except:
        temp = 25 

    pressure = row['Optimal Pressure']
    if isinstance(pressure, str) and '-' in pressure:
        pressure = np.mean([float(x) for x in pressure.split('-')])
    try:
        pressure = float(pressure)
    except:
        pressure = 1  

    pH = float(row['Optimal pH'])
    salinity = float(row['Optimal Salinity'])


    temp_score = np.exp(-0.001*(temp - conditions['Temperature'])**2)
    pH_score = np.exp(-0.1*(pH - conditions['pH'])**2)
    pressure_score = np.exp(-0.001*(pressure - conditions['Pressure'])**2)
    salinity_score = np.exp(-10*(salinity - conditions['Salinity'])**2)
    prob = temp_score * pH_score * pressure_score * salinity_score
    return np.clip(prob, 0, 1)

#prob
results = []
for planet, cond in planet_conditions.items():
    for i, row in df.iterrows():
        prob = survival_probability(row, cond)
        results.append({
            "Organism": row['Organism'],
            "Planet": planet,
            "Survival Probability": round(prob, 3)
        })



results_df = pd.DataFrame(results)
results_df.to_csv("survival_results.csv", index=False)

print(results_df.head())


import matplotlib.pyplot as plt

avg_probs = results_df.groupby('Planet')['Survival Probability'].mean()
avg_probs.plot(kind='bar', color='pink')
plt.ylabel('Average Survival Probability')
plt.title('Average Extremophile Survival Probability by Planet')
plt.tight_layout()
plt.savefig('average_survival_by_planet.png')
plt.show()

