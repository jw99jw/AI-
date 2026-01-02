import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# 1. AI training datasets (reinforced)
training_data = {
    'code_snippet': [
        "print('system check')", "import os; os.listdir()",
        "import rsa; key = rsa.newkeys(1024)", "from Crypto.Cipher import AES",
        "def add(a, b): return a + b", "hashlib.sha1(data)",
        "from pqcrypto.kem.kyber512 import generate_keypair", # PQC : safe
        "import ml_kem; key = ml_kem.generate_keypair()"      # PQC : safe
    ],
    'is_vulnerable': [0, 0, 1, 1, 0, 1, 0, 0]
}

df = pd.DataFrame(training_data)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['code_snippet'])
model = RandomForestClassifier()
model.fit(X, df['is_vulnerable'])

# 2. file scanning function
def scan_directory(path):
    print(f"beginning to scan : {path}")
    print("-" * 50)
    
    for root, dirs, files in os.walk(path):
        for file in files:
            # analyze only python files (except virtual environment folder)
            if file.endswith(".py") and "quantum_ai_env" not in root:
                file_path = os.path.join(root, file)
                
                with open(file_path, 'r', errors='ignore') as f:
                    code = f.read()
                    
                # AI prediction
                new_X = vectorizer.transform([code])
                prediction = model.predict(new_X)
                
                if prediction[0] == 1:
                    print(f"⚠️ [dager] {file_path}")
                else:
                    print(f"✅ [safe] {file_path}")

# 3. open my project directory
scan_directory('/home/klesa/project')