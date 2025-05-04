import pandas as pd
import json
import os

BASE_DIR = os.path.dirname(__file__)
EXCEL_FILE = os.path.join(BASE_DIR, 'tarifs_ludagri.xls')
JSON_FILE = os.path.join(BASE_DIR, 'moyennes.json')

def load_excel():
    return pd.read_excel(EXCEL_FILE)

def load_moyennes():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_moyenne(reference, moyenne):
    moyennes = load_moyennes()
    moyennes[reference] = moyenne
    with open(JSON_FILE, 'w') as f:
        json.dump(moyennes, f)

def rechercher_prix(reference):
    df = load_excel()
    ref_filtrée = df[df['Reference'].str.contains(reference, case=False, na=False)]
    if not ref_filtrée.empty:
        description = ref_filtrée.iloc[0].get('Description', '')
        prix = ref_filtrée.iloc[0].get('Prix', '')
        return {'source': 'excel', 'description': description, 'prix': prix}

    # Si pas trouvé → calcul moyenne
    df_match = df[df['Reference'].str[:5] == reference[:5]]
    if not df_match.empty:
        moyenne = df_match['Prix'].mean()
        save_moyenne(reference, moyenne)
        return {'source': 'moyenne', 'description': 'Estimation sur références similaires', 'prix': round(moyenne, 2)}
    
    return None