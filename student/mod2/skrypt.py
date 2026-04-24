import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# Wczytanie i przygotowanie danych
# =========================================================
df = pd.read_csv('energydata_complete.csv')

# Konwersja kolumny 'date' do formatu daty i czasu
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour
df['month'] = df['date'].dt.month

# Wyliczenie średniej temperatury wewnątrz domu
temp_cols = ['T1', 'T2', 'T3', 'T4', 'T5', 'T7', 'T8', 'T9']
df['T_indoor_mean'] = df[temp_cols].mean(axis=1)

# DYNAMICZNE POBRANIE ZAKRESU DAT DO TYTUŁÓW
start_date = df['date'].min().strftime('%d.%m.%Y')
end_date = df['date'].max().strftime('%d.%m.%Y')
date_info = f"(Okres pomiarowy: {start_date} - {end_date} | Zima - Wiosna)"

# =========================================================
# 1. Średni dobowy profil zużycia energii (Appliances)
# =========================================================
hourly_energy = df.groupby('hour')['Appliances'].mean().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(data=hourly_energy, x='hour', y='Appliances', color='skyblue')
plt.title(f'Średni dobowy profil zużycia energii\n{date_info}', fontsize=13)
plt.xlabel('Godzina')
plt.ylabel('Średnie zużycie energii (Wh)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('daily_energy.png')
plt.show()

# =========================================================
# 2. Średni dobowy profil temperatury (Wewnątrz vs Zewnątrz)
# =========================================================
hourly_temp = df.groupby('hour')[['T_indoor_mean', 'T_out']].mean().reset_index()

plt.figure(figsize=(10, 5))
plt.plot(hourly_temp['hour'], hourly_temp['T_indoor_mean'], marker='o', label='Średnia temp. wewnątrz')
plt.plot(hourly_temp['hour'], hourly_temp['T_out'], marker='s', label='Temp. na zewnątrz (T_out)')
plt.title(f'Średni dobowy profil temperatury domu\n{date_info}', fontsize=13)
plt.xlabel('Godzina')
plt.ylabel('Temperatura (°C)')
plt.xticks(range(0, 24))
plt.legend()
plt.grid(linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('daily_temp.png')
plt.show()

# =========================================================
# 3. NOWY WYKRES: Sezonowość zużycia energii (Miesiące)
# =========================================================
# Mapowanie numerów miesięcy na polskie nazwy
month_map = {1: 'Styczeń', 2: 'Luty', 3: 'Marzec', 4: 'Kwiecień', 5: 'Maj'}
df['month_name'] = df['month'].map(month_map)

plt.figure(figsize=(10, 5))
sns.boxplot(
    data=df, 
    x='month_name', 
    y='Appliances', 
    palette='viridis', 
    order=['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj']
)

plt.title(f'Rozkład zużycia energii w poszczególnych miesiącach\n{date_info}', fontsize=13)
plt.xlabel('Miesiąc (2016)')
plt.ylabel('Zużycie energii (Wh)')
plt.ylim(0, 600) # Ograniczenie osi Y by ekstremalne anomalie nie psuły czytelności wykresu
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('monthly_energy_trend.png')
plt.show()
