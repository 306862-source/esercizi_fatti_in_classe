import pandas as pd

# Leggi il file Parquet
df = pd.read_parquet('C:\\Users\\paolo\\OneDrive\\Documenti\\università\\magistrale\\secondo anno\\secondo semestre\\Pervasive computing e servizi cloud\\esercizi\\fatti in classe\\progetto\\2023_NOAA_AIS_ships_12.parquet')

# Salva i dati come CSV, che può essere aperto facilmente in Excel
df.to_csv('progetto\ships_data.csv', index=False)

print("Dati letti dal file Parquet e salvati in 'ships_data.csv' per l'apertura in Excel.")