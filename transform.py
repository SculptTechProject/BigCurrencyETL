import pandas as pd

def transform(nbp_rates, crypto_rates):
    print("[3/4] Transforming data…")
    df_nbp = pd.DataFrame(nbp_rates)[['code','mid']]
    df_nbp.rename(columns={'mid':'rate'}, inplace=True)
    df_nbp['type'] = 'fiat'

    df_crypto = pd.DataFrame(crypto_rates).T.reset_index()
    df_crypto.columns = ['code','rate']
    df_crypto['type'] = 'crypto'

    df = pd.concat([df_nbp, df_crypto], ignore_index=True)
    df['fetched_at'] = pd.Timestamp.utcnow()
    print(f"  → Combined {len(df_nbp)} fiat + {len(df_crypto)} crypto rows")
    return df

if __name__ == "__main__":
    # for quick test
    from extract import extract_nbp, extract_crypto
    nbp = extract_nbp("http://api.nbp.pl/api/exchangerates/tables/A?format=json")
    crypto = extract_crypto("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd")
    df = transform(nbp, crypto)
    print(df.head())
