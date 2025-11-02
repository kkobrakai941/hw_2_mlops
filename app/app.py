import os
from src.preprocessing import preprocess
from src.scorer import score

INPUT_PATH = "./input/test.csv"
REFERENCE_PATH = "./train_data/train.csv"
MODEL_PATH = "./models/my_catboost.cbm"
OUTPUT_DIR = "./output"

if __name__ == "__main__":
    X_test = preprocess(INPUT_PATH, REFERENCE_PATH)
    score(X_test, MODEL_PATH, OUTPUT_DIR)

