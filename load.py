import psycopg2
from psycopg2.extras import execute_values

def load(df, cfg):
    print("[4/4] Loading into PostgreSQL…")
    conn = psycopg2.connect(
        host=cfg['postgres']['host'],
        port=cfg['postgres']['port'],
        dbname=cfg['postgres']['db'],
        user=cfg['postgres']['user'],
        password=cfg['postgres']['password'],
        sslmode=cfg['postgres']['sslmode'],
        sslrootcert=cfg['postgres']['sslrootcert']
    )
    with conn:
        with conn.cursor() as cur:
            # create table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS exchange_rates (
                  code TEXT,
                  rate NUMERIC,
                  type TEXT,
                  fetched_at TIMESTAMP
                );
            """)
            tuples = [tuple(x) for x in df[['code','rate','type','fetched_at']].values]
            sql = "INSERT INTO exchange_rates (code,rate,type,fetched_at) VALUES %s"
            execute_values(cur, sql, tuples)
    conn.close()
    print("✅ Load complete.")
