from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def _build_connect_args(pg_cfg: dict) -> dict:
    """
    Buduje connect_args tylko z istniejących pól.
    Dzięki temu sslmode / sslrootcert są opcjonalne.
    """
    args = {}
    if pg_cfg.get("sslmode"):
        args["sslmode"] = pg_cfg["sslmode"]
    if pg_cfg.get("sslrootcert"):
        args["sslrootcert"] = pg_cfg["sslrootcert"]
    return args


def load(df, cfg, table: str = "currency_rates") -> None:
    """Zapisuje df do tabeli w Postgresie."""
    pg = cfg["postgres"]

    conn_str = (
        f"postgresql+psycopg2://{pg['user']}:{pg['password']}"
        f"@{pg['host']}:{pg['port']}/{pg['db']}"
    )
    engine = create_engine(conn_str, connect_args=_build_connect_args(pg))

    print(f"    → Inserting {len(df)} rows into '{table}'…")
    try:
        with engine.begin() as conn:
            df.to_sql(table, conn, if_exists="append", index=False)
    except SQLAlchemyError as exc:
        raise RuntimeError(f"PostgreSQL insert failed: {exc}") from exc
    print("    ✓ Load complete")

if __name__ == "__main__":
    import yaml
    import pandas as pd

    # dummy dataframe
    df_test = pd.DataFrame(
        {"code": ["USD", "EUR"], "rate": [4.0, 4.5], "type": ["fiat", "fiat"]}
    )

    cfg = yaml.safe_load(open("config.yaml"))
    load(df_test, cfg)