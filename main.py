import yaml
from extract import extract_nbp, extract_crypto
from transform import transform
from load import load

def main():
    print("=== BigCurrencyETL START ===")
    cfg = yaml.safe_load(open('config.yaml'))
    nbp = extract_nbp(cfg['sources']['nbp_api'])
    crypto = extract_crypto(cfg['sources']['crypto_api'])
    df = transform(nbp, crypto)
    load(df, cfg)
    print("=== BigCurrencyETL FINISHED ===")

if __name__ == "__main__":
    main()
