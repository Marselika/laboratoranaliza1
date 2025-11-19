# Raport de Analiză a Datelor despre Producerea Energiei Electrice
##### Student: Iatco Marcel
##### Perioada analizată: 1 ianuarie 2024 - 31 august 2025
### 1. Obiectivul Lucrării
Această lucrare își propune să realizeze o analiză complexă a datelor privind producerea și consumul energiei electrice pe o perioadă de aproximativ 20 de luni (ianuarie 2024 - august 2025). Prin intermediul tehnicilor moderne de analiză și vizualizare a datelor, am investigat pattern-urile de producție și consum energetic, corelațiile dintre diferite surse de energie și factorii temporali, precum și evoluția sistemului energetic național.

**Obiectivele specifice includ:**

- Preprocesarea și curățarea unui set masiv de date temporale
- Identificarea corelațiilor între variabilele energetice
- Crearea de vizualizări informative pentru comunicarea rezultatelor
- Dezvoltarea unei aplicații interactive pentru explorarea datelor

## Setul de Date

### Structura Datelor

| Coloană | Tip | Descriere |
|---------|-----|-----------|
| `date` | datetime | Timestamp-ul înregistrării |
| `carbune` | numeric | Producție din cărbune (MWh) |
| `consum` | numeric | Consum total de energie (MWh) |
| `hidro` | numeric | Producție hidroelectrică (MWh) |
| `hidrocarburi` | numeric | Producție din hidrocarburi (MWh) |
| `nuclear` | numeric | Producție nucleară (MWh) |
| `eolian` | numeric | Producție eoliană (MWh) |
| `productie` | numeric | Producție totală (MWh) |
| `fotovolt` | numeric | Producție fotovoltaică (MWh) |
| `biomasa` | numeric | Producție din biomasă (MWh) |
| `stocare` | numeric | Energie în stocare (MWh) |
| `sold` | numeric | Diferența producție-consum (MWh) |

### Dimensiunea Datelor

- **Perioada:** Ianuarie 2024 - August 2025
- **Total înregistrări:** 1395
- **Format:** CSV

  ##  Preprocesarea Datelor

### 1. Curățarea Datelor
```python
import pandas as pd
import numpy as np

# Încărcarea datelor
df = pd.read_csv("energie.csv")

# Verificarea valorilor lipsă
print("Valori lipsă per coloană:")
print(df.isnull().sum())

# Verificarea duplicatelor
duplicates = df.duplicated().sum()
print(f"Număr de duplicate: {duplicates}")
```

**Rezultate:**
- ✅ Nu s-au identificat valori lipsă
- ✅ Nu s-au găsit înregistrări duplicate
- ✅ Toate valorile numerice validate

**Descompunerea datelor temporale:**
```python
# Convertirea la datetime
df["date"] = pd.to_datetime(df["date"])

# Extragerea componentelor temporale
df["an"] = df["date"].dt.year
df["luna"] = df["date"].dt.month
df["zi"] = df["date"].dt.day
df["ora"] = df["date"].dt.hour
df["minut"] = df["date"].dt.minute
df["zi_saptamana"] = df["date"].dt.day_name().str.lower()
```
**Crearea variabilei raport preț/calitate:**
```python
df_trans["raport_pret_calitate"] = df_trans["productie"] / df_trans["consum"]
```
### 3. Statistici Descriptive

<img width="707" height="118" alt="image" src="https://github.com/user-attachments/assets/67e7bc82-3bd0-43f5-9c89-253da6a2a11b" />
<img width="662" height="718" alt="image" src="https://github.com/user-attachments/assets/c74f2a29-4d4e-4d15-b809-63d17fee7523" />
<img width="1486" height="617" alt="image" src="https://github.com/user-attachments/assets/1322743a-c533-4beb-a2fa-e66adeb72931" />
<img width="662" height="370" alt="image" src="https://github.com/user-attachments/assets/e0576db5-031a-4f81-8d6d-e9585811d792" />

## Analiza Corelațiilor

### 1. Corelația Ora - Energie Fotovoltaică
<img width="917" height="545" alt="image" src="https://github.com/user-attachments/assets/1dece863-ba86-4fca-a6d9-06ef32128ec0" />

**Observatie:**
Producția fotovoltaică urmează perfect ciclul solar diurn, cu maximum între 12:00-14:00 și zero sau minus în timpul nopții.

### 3. Heatmap - Producție pe Luni
<img width="992" height="547" alt="image" src="https://github.com/user-attachments/assets/e0836e24-ce5b-43b1-9a5c-4b9de790b19a" />

| Sezon | Caracteristici |
|-------|----------------|
| ❄️ **Iarnă** | Solar minim, eolian maxim, consum ridicat |
| 🌸 **Primăvară** | Hidro maxim (topirea zăpezii), echilibru bun |
| ☀️ **Vară** | Solar maxim, eolian minim, consum pentru răcire |
| 🍂 **Toamnă** | Tranziție, hidro scăzut |

## Vizualizări

### 1. Producția Lunară pe Tipuri

<img width="1188" height="590" alt="image" src="https://github.com/user-attachments/assets/7c96f2d6-7bc1-46f2-9fcf-3bdcf67ae03b" />

### 2. Soldul Zilnic 2024 vs 2025

<img width="1189" height="790" alt="image" src="https://github.com/user-attachments/assets/fe4b77e4-dce0-45b7-8d10-8745b8a5c9fd" />

### 3. Seria Temporală pe Sold

<img width="1389" height="626" alt="image" src="https://github.com/user-attachments/assets/c57089a1-b5bd-424b-81c4-bd1d2f6be426" />

### 4. Peek-ul Producției pe Ore

<img width="1390" height="590" alt="image" src="https://github.com/user-attachments/assets/43198042-b694-4a57-9230-799abd9a86e7" />

### 5. Consumul Mediu pe Zilele Săptămânii

<img width="859" height="538" alt="image" src="https://github.com/user-attachments/assets/7c81adf1-151a-4380-8c1c-b0b5802b3db6" />

### 6. Producția Medie Lunară 2024 vs 2025

<img width="859" height="470" alt="image" src="https://github.com/user-attachments/assets/174e543a-f0ce-4fb7-970c-a83a4618f7c9" />

### 7. Comparare Consum și Producție

<img width="1389" height="1000" alt="image" src="https://github.com/user-attachments/assets/a5a5bd36-9cd4-4bbd-b91a-31eb5848c5e4" />

<img width="1389" height="1000" alt="image" src="https://github.com/user-attachments/assets/eccc9fbb-265c-468f-8a67-c30760fb01eb" />


## Aplicația Streamlit
- ✅ Selectare multiplă a surselor
- ✅ Filtrare pe an (2024, 2025)
- ✅ Granularitate: Orar, Zilnic, Lunar
- ✅ Grafice interactive cu culori distinctive
- ✅ Vizualizare producție totală
- ✅ Comparație între ani
- ✅ Statistici în timp real
- ✅ Identificarea trend-urilor


<img width="1777" height="967" alt="image" src="https://github.com/user-attachments/assets/acd80605-f49b-4682-84e7-5175bd0a4049" />

<img width="356" height="586" alt="image" src="https://github.com/user-attachments/assets/96beeb07-bb6f-4321-81ee-31edd228d923" />

<img width="344" height="338" alt="image" src="https://github.com/user-attachments/assets/78716ad6-edc4-4c89-8256-ced11362cd78" />










