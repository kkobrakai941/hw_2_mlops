from kafka import KafkaConsumer, KafkaProducer
from catboost import CatBoostClassifier
from src.preprocessing import preprocess
import pandas as pd
import json

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest'
)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

model = CatBoostClassifier()
model.load_model("models/my_catboost.cbm")

for msg in consumer:
    df = pd.DataFrame([msg.value])
    X = preprocess(df, "train_data/train.csv")
    score = float(model.predict_proba(X)[:, 1][0])
    fraud_flag = int(score > 0.5)

    result = {
        "transaction_id": msg.value.get("transaction_id"),
        "score": score,
        "fraud_flag": fraud_flag
    }
    producer.send('scores', value=result)
    print(kafaresult)
