import pandas as pd
from catboost import CatBoostClassifier
import matplotlib.pyplot as plt
import json
import os

def score(input_df: pd.DataFrame, model_path: str, output_dir: str):
    model = CatBoostClassifier()
    model.load_model(model_path)

    preds = model.predict_proba(input_df)[:, 1]

    os.makedirs(output_dir, exist_ok=True)
    pd.DataFrame({
        "id": range(len(preds)),
        "target": preds
    }).to_csv(os.path.join(output_dir, "sample_submission.csv"), index=False)

    feature_importances = model.get_feature_importance()
    feature_names = model.feature_names_
    top5 = sorted(zip(feature_names, feature_importances), key=lambda x: x[1], reverse=True)[:5]
    with open(os.path.join(output_dir, "feature_importances.json"), "w") as f:
        json.dump(dict(top5), f, indent=4)

    plt.figure(figsize=(8, 4))
    plt.hist(preds, bins=50, color="skyblue", edgecolor="black")
    plt.title("Score Distribution")
    plt.xlabel("Predicted Probability")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "score_distribution.png"))
    plt.close()

