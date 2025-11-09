from kafka import KafkaConsumer
import psycopg2, json

conn = psycopg2.connect(
    dbname="fraud",
    user="user",
    password="password",
    host="postgres",
    port="5432"
)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id SERIAL PRIMARY KEY,
    transaction_id BIGINT,
    score FLOAT,
    fraud_flag BOOLEAN
);
""")
conn.commit()

consumer = KafkaConsumer(
    'scores',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest'
)

for msg in consumer:
    val = msg.value
    cur.execute(
        "INSERT INTO scores (transaction_id, score, fraud_flag) VALUES (%s, %s, %s)",
        (val["transaction_id"], val["score"], val["fraud_flag"])
    )
    conn.commit()
    print(val)
