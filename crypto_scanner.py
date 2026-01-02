import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# 1. data representation
data = {
    'code_snippet': [
        "print('hello world')", 
        "import rsa; key = rsa.newkeys(1024)", 
        "for i in range(10): print(i)",
        "from Crypto.Cipher import AES; cipher = AES.new(key, AES.MODE_ECB)",
        "x = a + b",
        "hashlib.sha1(data).hexdigest()"
    ],
    'is_vulnerable': [0, 1, 0, 1, 0, 1] # 0: safe, 1: quantum vulnerable
}

df = pd.DataFrame(data)

# 2. convert text data into vector (TF-IDF)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['code_snippet'])
y = df['is_vulnerable']

# 3. learn model (Random Forest)
model = RandomForestClassifier()
model.fit(X, y)

# 4. test new code (test)
# new_code = ["import rsa; public_key, private_key = rsa.newkeys(2048)"]

# 4. new test code
test_codes = [
    "print('Hello Raspberry Pi!')",                               # safe
    "import rsa; key = rsa.newkeys(512)",                         # vulnerable
    "from Crypto.Hash import SHA1; h = SHA1.new(data)",           # vulnerable
    "from pqcrypto.kem.kyber512 import generate_keypair"          # safe(quantum safe)
]

for code in test_codes:
    new_X = vectorizer.transform([code])
    prediction = model.predict(new_X)
    result = "⚠️ [danger] quantum vulnerable password detected" if prediction[0] == 1 else "✅ [safe] normal or PQC code"
    print(f"Code: {code[:30]}... -> Result: {result}")

new_X = vectorizer.transform(test_codes)
prediction = model.predict(new_X)

if prediction[0] == 1:
    print("⚠️ warning: password pattern vulnerable to quantum attacks detected!")
else:
    print("✅ safe: standard code.")