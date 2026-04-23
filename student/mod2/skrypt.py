import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytanie danych z poprawnego pliku
df = pd.read_csv('energydata_complete.csv')

# Konwersja kolumny 'date' do formatu daty i czasu oraz ekstrakcja godziny
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour

# Wyliczenie średniej temperatury wewnątrz domu (z pominięciem T6 - zewnątrz)
temp_cols = ['T1', 'T2', 'T3', 'T4', 'T5', 'T7', 'T8', 'T9']
df['T_indoor_mean'] = df[temp_cols].mean(axis=1)

# =========================================================
# 1. Średni dobowy profil zużycia energii (Appliances)
# =========================================================
hourly_energy = df.groupby('hour')['Appliances'].mean().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(data=hourly_energy, x='hour', y='Appliances', color='skyblue')
plt.title('Średni dobowy profil zużycia energii')
plt.xlabel('Godzina')
plt.ylabel('Średnie zużycie energii (Wh)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('daily_energy.png') # Zapis do pliku
plt.show()

# =========================================================
# 2. Średni dobowy profil temperatury (Wewnątrz vs Zewnątrz)
# =========================================================
hourly_temp = df.groupby('hour')[['T_indoor_mean', 'T_out']].mean().reset_index()

plt.figure(figsize=(10, 5))
plt.plot(hourly_temp['hour'], hourly_temp['T_indoor_mean'], marker='o', label='Średnia temp. wewnątrz')
plt.plot(hourly_temp['hour'], hourly_temp['T_out'], marker='s', label='Temp. na zewnątrz (T_out)')
plt.title('Średni dobowy profil temperatury domu')
plt.xlabel('Godzina')
plt.ylabel('Temperatura (°C)')
plt.xticks(range(0, 24))
plt.legend()
plt.grid(linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('daily_temp.png')
plt.show()

# =========================================================
# 3. Macierz korelacji kluczowych zmiennych
# =========================================================
cols_to_corr = ['Appliances', 'T_indoor_mean', 'T_out', 'RH_out', 'Windspeed', 'Visibility']
corr = df[cols_to_corr].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title('Macierz korelacji zmiennych domowych i pogodowych')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.show()