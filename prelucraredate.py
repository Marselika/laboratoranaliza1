# cleaning_part1.py
import pandas as pd
import numpy as np
from typing import List, Optional, Tuple

def load_data(path: str, encoding: str = "utf-8") -> pd.DataFrame:
    """Încarcă CSV-ul într-un DataFrame."""
    df = pd.read_csv(path, encoding=encoding)
    print(f"Date citite: {len(df)} rânduri, {len(df.columns)} coloane.")
    return df

def report_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Raportează numărul și procentul de valori lipsă pe coloană.
    Returnează un DataFrame sumar (col: missing_count, missing_pct).
    """
    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df)) * 100
    summary = pd.DataFrame({
        "missing_count": missing_count,
        "missing_pct": missing_pct
    }).sort_values("missing_pct", ascending=False)
    print("\n--- Valori lipsă pe coloane ---")
    print(summary[summary["missing_count"] > 0])
    return summary

def detect_bad_rows(df: pd.DataFrame, threshold_row_pct: float = 50.0) -> pd.DataFrame:
    """
    Găsește rândurile cu mai mult de `threshold_row_pct`% valori lipsă.
    Returnează DataFrame cu index-urile acelor rânduri.
    """
    row_missing_pct = (df.isna().sum(axis=1) / df.shape[1]) * 100
    bad_idx = df.index[row_missing_pct > threshold_row_pct].tolist()
    print(f"\nRânduri cu > {threshold_row_pct}% valori lipsă: {len(bad_idx)}")
    return df.loc[bad_idx]

def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None, keep: str = "first") -> Tuple[pd.DataFrame, int]:
    """
    Detectează și elimină duplicate.
    - subset: lista de coloane pe baza cărora se verifică duplicatele (None -> toate coloanele)
    - keep: 'first', 'last' sau False (False -> elimină toate duplicatele păstrând niciunul)
    Returnează (df_no_duplicates, n_removed)
    """
    before = len(df)
    # număr duplicate
    dup_mask = df.duplicated(subset=subset, keep=False)
    n_total_duplicates = dup_mask.sum()
    # opțional: afișează câteva rânduri duplicate pentru inspectare
    if n_total_duplicates:
        print(f"\nAu fost găsite {n_total_duplicates} rânduri care apar ca duplicat (nu neapărat eliminate încă).")
        print("Exemple (duplicați):")
        print(df[dup_mask].head(10))
    # eliminare efectivă
    df_clean = df.drop_duplicates(subset=subset, keep=keep)
    after = len(df_clean)
    removed = before - after
    print(f"Duplicate eliminate: {removed} (rămase: {after}).")
    return df_clean, removed

def impute_missing(
    df: pd.DataFrame,
    strategy: str = "median",
    numeric_cols: Optional[List[str]] = None,
    categorical_cols: Optional[List[str]] = None,
    date_col: Optional[str] = None
) -> Tuple[pd.DataFrame, dict]:
    """
    Tratează valorile lipsă.
    Strategii posibile:
      - 'drop' : șterge rândurile cu ANY NaN (atenție)
      - 'median': pentru coloane numerice -> mediană; categorice -> modul
      - 'mode': pentru numerice -> mod (rareori folosit), categorice -> mod
      - 'ffill': forward-fill (util pentru serii temporale; recomandat cu date sortate)
    Parametri:
      - numeric_cols / categorical_cols: liste explicite (dacă None se detectează automat)
      - date_col: dacă se dorește imputare pe serie temporală, trece coloana date pentru sortare înainte de ffill
    Returnează (df_imputed, info_dict) cu statistici despre imputare.
    """
    info = {"before_missing": df.isna().sum().to_dict()}
    df_work = df.copy()

    # Detectăm coloanele dacă nu sunt specificate
    if numeric_cols is None:
        # convertim la numeric temporar pentru detectare
        detected_numeric = df_work.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = detected_numeric
    if categorical_cols is None:
        categorical_cols = [c for c in df_work.columns if c not in numeric_cols]

    if strategy == "drop":
        before = len(df_work)
        df_work = df_work.dropna()
        info["dropped_rows"] = before - len(df_work)
        print(f"Drop strategy: am eliminat {info['dropped_rows']} rânduri care conțineau NaN.")
        info["after_missing"] = df_work.isna().sum().to_dict()
        return df_work, info

    if strategy == "ffill":
        if date_col and date_col in df_work.columns:
            df_work = df_work.sort_values(date_col)
        df_work = df_work.ffill().bfill()
        print("Imputare ffill/bfill aplicată (ordinea: sort după date dacă a fost indicată).")
        info["after_missing"] = df_work.isna().sum().to_dict()
        return df_work, info

    # Pentru strategiile median / mode / median+mode
    if strategy in ("median", "mode"):
        # Asigură conversia numericelor - dacă sunt stocate ca stringuri
        for col in numeric_cols:
            if col in df_work.columns:
                df_work[col] = pd.to_numeric(df_work[col], errors="coerce")

        # Numeric: fill
        for col in numeric_cols:
            if col in df_work.columns:
                if strategy == "median":
                    fill_val = df_work[col].median(skipna=True)
                else:
                    mode = df_work[col].mode(dropna=True)
                    fill_val = mode[0] if not mode.empty else np.nan
                if pd.notna(fill_val):
                    n_before = df_work[col].isna().sum()
                    df_work[col] = df_work[col].fillna(fill_val)
                    n_after = df_work[col].isna().sum()
                    print(f"Col numeric '{col}': {n_before} -> {n_after} NaN (umplut cu {fill_val}).")

        # Categorical: fill with mode
        for col in categorical_cols:
            if col in df_work.columns:
                mode_vals = df_work[col].mode(dropna=True)
                if not mode_vals.empty:
                    fill_val = mode_vals[0]
                    n_before = df_work[col].isna().sum()
                    df_work[col] = df_work[col].fillna(fill_val)
                    n_after = df_work[col].isna().sum()
                    print(f"Col categoric '{col}': {n_before} -> {n_after} NaN (umplut cu '{fill_val}').")
                else:
                    # dacă nu există mod (ex. toate NaN) nu facem nimic
                    print(f"Col categoric '{col}': nu s-a găsit mod (toate NaN?).")

        info["after_missing"] = df_work.isna().sum().to_dict()
        return df_work, info

    raise ValueError(f"Strategie necunoscută: {strategy}")

# -------------------------
# Exemplar de rulare
# -------------------------
if __name__ == "__main__":
    # Înlocuiește cu calea ta
    input_csv = "datalab1.csv"

    df = load_data(input_csv)

    # 1) Raport missing
    missing_summary = report_missing(df)

    # (opțional) inspectează rândurile foarte sărace în informație
    bad_rows = detect_bad_rows(df, threshold_row_pct=50.0)

    # 2) Tratare valori lipsă (alege strategia: 'median', 'ffill', 'drop', 'mode')
    df_imputed, impute_info = impute_missing(df, strategy="median")
    print("\nSumar imputare (excerpts):")
    for k, v in list(impute_info["before_missing"].items())[:10]:
        pass  # doar exemple; poți printa aici dacă vrei

    # 3) Verificare + eliminare duplicate (poți da subset dacă ai chei)
    df_no_dup, removed = remove_duplicates(df_imputed, subset=None, keep="first")

    # Salvare
    df_no_dup.to_csv("energy_data.csv", index=False)
    print("\nFișier salvat: energy_data.csv")
