import pandas as pd
import os

def load_all_health_data():
    try:
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        data_files = {
            'doctors': 'Lekarze_pielegniarki_2017-2023.csv',
            'hospitals': 'Szpitale_lozka_szpitalne_2017-2023.csv',
            'expenditure': 'Wydatki_na_zdrowie_2017-2023.csv',
            'deaths': 'Zgony_i_przyczyny_2017-2023.csv'
        }
        
        dfs = {}
        for key, file_name in data_files.items():
            file_path = os.path.join(data_dir, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Plik danych nie został znaleziony: {file_path}")
            
            df = pd.read_csv(file_path, sep=';', encoding='utf-8', quotechar='"', dtype={'Kod': str})
            
            for col in df.columns:
                if col != 'Kod' and col != 'Nazwa':
                    df[col] = df[col].astype(str).str.replace(',', '.')
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            dfs[key] = df
            
        return dfs
    except Exception as e:
        raise 