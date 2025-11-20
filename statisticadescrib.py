import pandas as pd
import numpy as np
from scipy import stats

# Configurare afișare pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', 100)

# Încărcare date
print("=" * 80)
print("📊 ANALIZA STATISTICILOR DESCRIPTIVE - ENERGIE ROMÂNIA")
print("=" * 80)
print()

df = pd.read_csv("energie_transformata.csv")
df["date"] = pd.to_datetime(df["date"])

print(f"✅ Date încărcate cu succes!")
print(f"   📅 Perioada: {df['date'].min()} → {df['date'].max()}")
print(f"   📊 Total înregistrări: {len(df):,}")
print(f"   📈 Coloane: {len(df.columns)}")
print()

# ============================================================================
# 1. INFORMAȚII GENERALE DESPRE DATASET
# ============================================================================
print("=" * 80)
print("1️⃣  INFORMAȚII GENERALE DESPRE DATASET")
print("=" * 80)
print()

print("📋 Structura datelor:")
print(df.info())
print()

print("🔍 Primele 5 rânduri:")
print(df.head())
print()

print("📏 Dimensiuni dataset:")
print(f"   Rânduri: {df.shape[0]:,}")
print(f"   Coloane: {df.shape[1]}")
print()

# ============================================================================
# 2. VERIFICARE CALITATE DATE
# ============================================================================
print("=" * 80)
print("2️⃣  VERIFICARE CALITATE DATE")
print("=" * 80)
print()

print("❓ Valori lipsă per coloană:")
missing = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100
missing_df = pd.DataFrame({
    'Valori lipsă': missing,
    'Procent (%)': missing_percent
})
print(missing_df[missing_df['Valori lipsă'] > 0])
if missing.sum() == 0:
    print("   ✅ Nu există valori lipsă!")
print()

print("🔄 Duplicate:")
duplicates = df.duplicated().sum()
print(f"   Total duplicate: {duplicates}")
if duplicates == 0:
    print("   ✅ Nu există duplicate!")
print()

# ============================================================================
# 3. STATISTICI DESCRIPTIVE - SURSE DE ENERGIE
# ============================================================================
print("=" * 80)
print("3️⃣  STATISTICI DESCRIPTIVE - SURSE DE ENERGIE")
print("=" * 80)
print()

surse_energie = ["carbune", "hidro", "hidrocarburi", "nuclear",
                 "eolian", "fotovolt", "biomasa"]

print("📊 Statistici complete pentru sursele de energie:")
print()
statistici = df[surse_energie].describe()
print(statistici.round(2))
print()

# Statistici suplimentare
print("📈 Statistici suplimentare:")
print()
statistici_extra = pd.DataFrame({
    'Medie': df[surse_energie].mean(),
    'Mediană': df[surse_energie].median(),
    'Std Dev': df[surse_energie].std(),
    'Varianta': df[surse_energie].var(),
    'Min': df[surse_energie].min(),
    'Max': df[surse_energie].max(),
    'Range': df[surse_energie].max() - df[surse_energie].min(),
    'CV (%)': (df[surse_energie].std() / df[surse_energie].mean() * 100),
    'Skewness': df[surse_energie].skew(),
    'Kurtosis': df[surse_energie].kurtosis()
})
print(statistici_extra.round(2))
print()

# Explicații
print("📖 Explicații:")
print("   • CV (Coeficient de Variație): măsoară variabilitatea relativă")
print("     - CV < 15%: variabilitate redusă (stabilă)")
print("     - CV 15-30%: variabilitate moderată")
print("     - CV > 30%: variabilitate ridicată (instabilă)")
print()
print("   • Skewness (Asimetrie):")
print("     - Pozitivă: distribuție asimetrică spre dreapta")
print("     - Negativă: distribuție asimetrică spre stânga")
print("     - ~0: distribuție simetrică")
print()
print("   • Kurtosis (Aplatizare):")
print("     - Pozitivă: distribuție cu vârfuri ascuțite")
print("     - Negativă: distribuție aplatizată")
print()

# ============================================================================
# 4. STATISTICI DESCRIPTIVE - PRODUCȚIE ȘI CONSUM
# ============================================================================
print("=" * 80)
print("4️⃣  STATISTICI DESCRIPTIVE - PRODUCȚIE, CONSUM, SOLD")
print("=" * 80)
print()

variabile_cheie = ["productie", "consum", "sold", "stocare"]

print("📊 Statistici complete:")
print()
statistici_prod_consum = df[variabile_cheie].describe()
print(statistici_prod_consum.round(2))
print()

print("📈 Statistici suplimentare:")
print()
statistici_extra_pc = pd.DataFrame({
    'Medie': df[variabile_cheie].mean(),
    'Mediană': df[variabile_cheie].median(),
    'Std Dev': df[variabile_cheie].std(),
    'Min': df[variabile_cheie].min(),
    'Max': df[variabile_cheie].max(),
    'Range': df[variabile_cheie].max() - df[variabile_cheie].min(),
    'CV (%)': (df[variabile_cheie].std() / df[variabile_cheie].mean() * 100).abs()
})
print(statistici_extra_pc.round(2))
print()

# Analiza soldului
print("⚖️  Analiza detaliată a soldului energetic:")
print()
sold_pozitiv = (df['sold'] > 0).sum()
sold_negativ = (df['sold'] < 0).sum()
sold_zero = (df['sold'] == 0).sum()
total = len(df)

print(f"   🟢 Sold pozitiv (surplus): {sold_pozitiv:,} înregistrări ({sold_pozitiv / total * 100:.2f}%)")
print(f"   🔴 Sold negativ (deficit): {sold_negativ:,} înregistrări ({sold_negativ / total * 100:.2f}%)")
print(f"   ⚪ Sold zero (echilibru): {sold_zero:,} înregistrări ({sold_zero / total * 100:.2f}%)")
print()
print(f"   📊 Sold mediu: {df['sold'].mean():.2f} MWh")
print(f"   📈 Sold mediu pozitiv: {df[df['sold'] > 0]['sold'].mean():.2f} MWh")
print(f"   📉 Sold mediu negativ: {df[df['sold'] < 0]['sold'].mean():.2f} MWh")
print()

# ============================================================================
# 5. PERCENTILE ȘI CUARTILE
# ============================================================================
print("=" * 80)
print("5️⃣  PERCENTILE ȘI CUARTILE")
print("=" * 80)
print()

print("📊 Percentile pentru sursele de energie:")
print()
percentile = [0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
percentile_df = df[surse_energie].quantile(percentile)
percentile_df.index = [f'P{int(p * 100)}' for p in percentile]
print(percentile_df.round(2))
print()

print("📊 Percentile pentru producție și consum:")
print()
percentile_pc = df[["productie", "consum", "sold"]].quantile(percentile)
percentile_pc.index = [f'P{int(p * 100)}' for p in percentile]
print(percentile_pc.round(2))
print()

# ============================================================================
# 6. ANALIZA PE ANI
# ============================================================================
print("=" * 80)
print("6️⃣  ANALIZA COMPARATIVĂ PE ANI (2024 vs 2025)")
print("=" * 80)
print()

print("📊 Statistici 2024:")
print()
df_2024 = df[df["an"] == 2024]
stats_2024 = df_2024[surse_energie + ["productie", "consum", "sold"]].describe()
print(stats_2024.round(2))
print()

print("📊 Statistici 2025:")
print()
df_2025 = df[df["an"] == 2025]
stats_2025 = df_2025[surse_energie + ["productie", "consum", "sold"]].describe()
print(stats_2025.round(2))
print()

print("📈 Comparație medie 2024 vs 2025:")
print()
comparatie = pd.DataFrame({
    'Medie 2024': df_2024[surse_energie + ["productie", "consum", "sold"]].mean(),
    'Medie 2025': df_2025[surse_energie + ["productie", "consum", "sold"]].mean(),
    'Diferență': df_2025[surse_energie + ["productie", "consum", "sold"]].mean() -
                 df_2024[surse_energie + ["productie", "consum", "sold"]].mean(),
    'Variație (%)': ((df_2025[surse_energie + ["productie", "consum", "sold"]].mean() -
                      df_2024[surse_energie + ["productie", "consum", "sold"]].mean()) /
                     df_2024[surse_energie + ["productie", "consum", "sold"]].mean() * 100)
})
print(comparatie.round(2))
print()

# ============================================================================
# 7. ANALIZA PE LUNI
# ============================================================================
print("=" * 80)
print("7️⃣  ANALIZA PE LUNI")
print("=" * 80)
print()

print("📊 Producție medie pe luni:")
print()
prod_luna = df.groupby("luna")["productie"].agg(['mean', 'std', 'min', 'max', 'median'])
prod_luna.index = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun',
                   'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec'][:len(prod_luna)]
print(prod_luna.round(2))
print()

print("📊 Consum mediu pe luni:")
print()
consum_luna = df.groupby("luna")["consum"].agg(['mean', 'std', 'min', 'max', 'median'])
consum_luna.index = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun',
                     'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec'][:len(consum_luna)]
print(consum_luna.round(2))
print()

print("📊 Sold mediu pe luni:")
print()
sold_luna = df.groupby("luna")["sold"].agg(['mean', 'std', 'min', 'max', 'median'])
sold_luna.index = ['Ian', 'Feb', 'Mar', 'Apr', 'Mai', 'Iun',
                   'Iul', 'Aug', 'Sep', 'Oct', 'Noi', 'Dec'][:len(sold_luna)]
print(sold_luna.round(2))
print()

# ============================================================================
# 8. ANALIZA PE ORE
# ============================================================================
print("=" * 80)
print("8️⃣  ANALIZA PE ORE")
print("=" * 80)
print()

print("📊 Producție pe ore - Statistici complete:")
print()
prod_ora = df.groupby("ora")["productie"].agg(['mean', 'std', 'min', 'max', 'median'])
print(prod_ora.round(2))
print()

print("🔝 Top 5 ore cu producție maximă:")
print(prod_ora.nlargest(5, 'mean').round(2))
print()

print("⬇️ Top 5 ore cu producție minimă:")
print(prod_ora.nsmallest(5, 'mean').round(2))
print()

print("📊 Consum pe ore - Statistici complete:")
print()
consum_ora = df.groupby("ora")["consum"].agg(['mean', 'std', 'min', 'max', 'median'])
print(consum_ora.round(2))
print()

print("🔝 Top 5 ore cu consum maxim:")
print(consum_ora.nlargest(5, 'mean').round(2))
print()

print("⬇️ Top 5 ore cu consum minim:")
print(consum_ora.nsmallest(5, 'mean').round(2))
print()

# ============================================================================
# 9. ANALIZA PE ZILE SĂPTĂMÂNII
# ============================================================================
print("=" * 80)
print("9️⃣  ANALIZA PE ZILE SĂPTĂMÂNII")
print("=" * 80)
print()

zile_ordonate = ['monday', 'tuesday', 'wednesday', 'thursday',
                 'friday', 'saturday', 'sunday']
zile_ro = ['Luni', 'Marți', 'Miercuri', 'Joi', 'Vineri', 'Sâmbătă', 'Duminică']

print("📊 Statistici pe zile săptămânii:")
print()
stats_zile = df.groupby("zi_saptamana")[["productie", "consum", "sold"]].agg(['mean', 'std', 'min', 'max'])
stats_zile = stats_zile.reindex(zile_ordonate)
stats_zile.index = zile_ro
print(stats_zile.round(2))
print()

# ============================================================================
# 10. ANALIZA RAPORT PREȚ/CALITATE
# ============================================================================
print("=" * 80)
print("🔟 ANALIZA RAPORT PREȚ/CALITATE")
print("=" * 80)
print()

if 'raport_pret_calitate' in df.columns:
    print("📊 Statistici raport preț/calitate:")
    print()
    stats_raport = df['raport_pret_calitate'].describe()
    print(stats_raport.round(4))
    print()

    print("📊 Statistici suplimentare raport preț/calitate:")
    print()
    raport_stats = pd.DataFrame({
        'Medie': [df['raport_pret_calitate'].mean()],
        'Mediană': [df['raport_pret_calitate'].median()],
        'Std Dev': [df['raport_pret_calitate'].std()],
        'Min': [df['raport_pret_calitate'].min()],
        'Max': [df['raport_pret_calitate'].max()],
        'CV (%)': [df['raport_pret_calitate'].std() / df['raport_pret_calitate'].mean() * 100]
    })
    print(raport_stats.round(4))
    print()

    print("📈 Categorii raport preț/calitate:")
    print()
    excelent = (df['raport_pret_calitate'] >= 0.8).sum()
    bun = ((df['raport_pret_calitate'] >= 0.6) & (df['raport_pret_calitate'] < 0.8)).sum()
    mediu = ((df['raport_pret_calitate'] >= 0.4) & (df['raport_pret_calitate'] < 0.6)).sum()
    slab = (df['raport_pret_calitate'] < 0.4).sum()

    print(f"   🟢 Excelent (≥80% energie curată): {excelent:,} ({excelent / len(df) * 100:.2f}%)")
    print(f"   🟡 Bun (60-79% energie curată): {bun:,} ({bun / len(df) * 100:.2f}%)")
    print(f"   🟠 Mediu (40-59% energie curată): {mediu:,} ({mediu / len(df) * 100:.2f}%)")
    print(f"   🔴 Slab (<40% energie curată): {slab:,} ({slab / len(df) * 100:.2f}%)")
    print()

# ============================================================================
# 11. TESTE DE NORMALITATE
# ============================================================================
print("=" * 80)
print("1️⃣1️⃣  TESTE DE NORMALITATE (Shapiro-Wilk)")
print("=" * 80)
print()

print("📊 Testarea normalității distribuțiilor:")
print("   (p-value > 0.05 → distribuție normală)")
print()

# Test pe un subset (Shapiro-Wilk nu funcționează bine pe seturi mari)
sample_size = min(5000, len(df))
df_sample = df.sample(n=sample_size, random_state=42)

normalitate = []
for col in surse_energie + ["productie", "consum", "sold"]:
    stat, p_value = stats.shapiro(df_sample[col])
    normalitate.append({
        'Variabilă': col,
        'Statistic': stat,
        'P-value': p_value,
        'Normal?': 'Da' if p_value > 0.05 else 'Nu'
    })

normalitate_df = pd.DataFrame(normalitate)
print(normalitate_df.to_string(index=False))
print()
print(f"   ℹ️  Test efectuat pe un eșantion de {sample_size:,} înregistrări")
print()

# ============================================================================
# 12. MATRICE DE CORELAȚIE
# ============================================================================
print("=" * 80)
print("1️⃣2️⃣  MATRICE DE CORELAȚIE")
print("=" * 80)
print()

print("📊 Matricea de corelație între sursele de energie:")
print()
corr_matrix = df[surse_energie].corr()
print(corr_matrix.round(3))
print()

print("📊 Corelații cu producția totală:")
print()
corr_productie = df[surse_energie + ["productie"]].corr()["productie"].sort_values(ascending=False)
print(corr_productie.round(3))
print()

print("📊 Corelații cu consumul:")
print()
corr_consum = df[surse_energie + ["consum"]].corr()["consum"].sort_values(ascending=False)
print(corr_consum.round(3))
print()

# ============================================================================
# 13. REZUMAT FINAL
# ============================================================================
print("=" * 80)
print("1️⃣3️⃣  REZUMAT FINAL")
print("=" * 80)
print()

print("📊 REZUMAT STATISTICI DESCRIPTIVE:")
print()
print(f"✅ Total înregistrări analizate: {len(df):,}")
print(f"✅ Perioada: {df['date'].min().strftime('%Y-%m-%d')} → {df['date'].max().strftime('%Y-%m-%d')}")
print(f"✅ Surse de energie analizate: {len(surse_energie)}")
print()

print("🔝 TOP 3 SURSE CU PRODUCȚIE MEDIE CEA MAI MARE:")
top_3 = df[surse_energie].mean().nlargest(3)
for i, (sursa, val) in enumerate(top_3.items(), 1):
    print(f"   {i}. {sursa.capitalize()}: {val:.2f} MWh")
print()

print("📉 TOP 3 SURSE CU CEA MAI MARE VARIABILITATE (CV):")
cv = (df[surse_energie].std() / df[surse_energie].mean() * 100).nlargest(3)
for i, (sursa, val) in enumerate(cv.items(), 1):
    print(f"   {i}. {sursa.capitalize()}: CV = {val:.2f}%")
print()

print("🔵 SURSĂ CEA MAI STABILĂ (CV minim):")
cv_min = (df[surse_energie].std() / df[surse_energie].mean() * 100).nsmallest(1)
for sursa, val in cv_min.items():
    print(f"   • {sursa.capitalize()}: CV = {val:.2f}%")
print()

print("⚖️  BILANȚ ENERGETIC:")
print(f"   Producție medie totală: {df['productie'].mean():.2f} MWh")
print(f"   Consum mediu total: {df['consum'].mean():.2f} MWh")
print(f"   Sold mediu: {df['sold'].mean():.2f} MWh")
if df['sold'].mean() > 0:
    print(f"   ✅ Sistemul este în SURPLUS mediu de {df['sold'].mean():.2f} MWh")
else:
    print(f"   ⚠️  Sistemul este în DEFICIT mediu de {abs(df['sold'].mean()):.2f} MWh")
print()

print("📅 PERIODICITATE:")
print(f"   Ora cu consum maxim: {consum_ora['mean'].idxmax()}:00 ({consum_ora['mean'].max():.2f} MWh)")
print(f"   Ora cu consum minim: {consum_ora['mean'].idxmin()}:00 ({consum_ora['mean'].min():.2f} MWh)")
print(
    f"   Diferență vârf-minimă: {(consum_ora['mean'].max() - consum_ora['mean'].min()):.2f} MWh ({(consum_ora['mean'].max() - consum_ora['mean'].min()) / consum_ora['mean'].min() * 100:.1f}%)")
print()

print("=" * 80)
print("✅ ANALIZA STATISTICĂ COMPLETĂ!")
print("=" * 80)