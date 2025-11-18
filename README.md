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

## 📊 Setul de Date

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

  
