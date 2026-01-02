from kyber.py.kyber512 import Kyber512

print("---[PQC practice] Kyber-512 algorithm activated---")

try:
    pk, sk = Kyber512.keygen()
    c, key_enc = Kyber512.enc(pk)
    key_dec = Kyber512.dec(c, sk)

    if key_enc == key_dec:
        print("success: quantum safe communication succeeded")
        print(f"shared private key: {key_enc.hex()[:32]}...")
except Exception as e:
    print(f"error occurred: {e}")