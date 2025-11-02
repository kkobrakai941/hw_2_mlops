import pandas as pd

def preprocess(input_path: str, reference_path: str = "train_data/train.csv") -> pd.DataFrame:
    
    df_test = pd.read_csv(input_path)
    df_train = pd.read_csv(reference_path)

    if "target" in df_train.columns:
        df_train = df_train.drop(columns=["target"])

    common_cols = [c for c in df_train.columns if c in df_test.columns]
    df_test = df_test[common_cols]
    for c in df_test.columns:
        if df_test[c].dtype == "object":
            df_test[c] = df_test[c].astype(str)
    df_test = df_test.fillna(0)

    return df_test

