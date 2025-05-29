import requests
from configparser import ConfigParser

def extract_nbp(url):
    print("[1/4] Extracting NBP rates…")
    r = requests.get(url); r.raise_for_status()
    return r.json()[0]['rates']

def extract_crypto(url):
    print("[2/4] Extracting Crypto prices…")
    r = requests.get(url); r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    cfg = ConfigParser()
    cfg.read('config.yaml')
    nbp = extract_nbp(cfg['sources']['nbp_api'])
    crypto = extract_crypto(cfg['sources']['crypto_api'])
    print("Done extracting.")
