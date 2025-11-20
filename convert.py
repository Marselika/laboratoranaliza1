import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformări:
      1. Descompunere coloana 'date' în an, luna, zi, ora, minut, zi_saptamana
      2. Convertire coloane numerice la tip numeric
      3. Standardizare categorice
      4. Creare variabilă nouă raport_pret_calitate
    """

    df_trans = df.copy()

    # ------------------------------
    # 1. Descompunere coloana 'date'
    # ------------------------------
    df_trans["date"] = pd.to_datetime(df_trans["date"], errors="coerce")

    df_trans["an"] = df_trans["date"].dt.year
    df_trans["luna"] = df_trans["date"].dt.month
    df_trans["zi"] = df_trans["date"].dt.day
    df_trans["ora"] = df_trans["date"].dt.hour
    df_trans["minut"] = df_trans["date"].dt.minute
    df_trans["zi_saptamana"] = df_trans["date"].dt.day_name().str.lower()

    # ------------------------------
    # 2. Convertire numeric
    # ------------------------------
    numeric_cols = [
        "carbune","consum","hidro","hidrocarburi","nuclear",
        "eolian","productie","fotovolt","biomasa","stocare","sold"
    ]

    for col in numeric_cols:
        df_trans[col] = pd.to_numeric(df_trans[col], errors="coerce")

    # ------------------------------
    # 3. Standardizare categorice
    # ------------------------------
    df_trans["zi_saptamana"] = df_trans["zi_saptamana"].str.strip().str.lower()

    # ------------------------------
    # 4. Variabilă nouă: raport_pret_calitate
    # ------------------------------
    df_trans["raport_pret_calitate"] = df_trans["productie"] / df_trans["consum"]

    return df_trans


# Exemplu de rulare
if __name__ == "__main__":
    # Citește fișierul inițial
    df = pd.read_csv("energy_data.csv")

    # Aplică transformările
    df_t = transform_data(df)

    # Salvează rezultatul într-un nou fișier CSV
    df_t.to_csv("energie_transformata.csv", index=False)

    print("✔ Datele transformate au fost salvate în 'energie_transformata.csv'")
