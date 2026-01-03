import pandas as pd

def extract_excel(file_path: str):
    df = pd.read_excel(file_path)
    return [(1, df.to_string(index=False))]
