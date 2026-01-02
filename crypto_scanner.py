import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# 1. training data 
training_data = {
    'code_snippet': [
        "print('system check')", "import os; os.listdir()",
        "import rsa; key = rsa.newkeys(1024)", "from Crypto.Cipher import AES",
        "def add(a, b): return a + b", "hashlib.sha1(data)",
        "from pqcrypto.kem.kyber512 import generate_keypair",
        "import ml_kem; key = ml_kem.generate_keypair()"
    ],
    'is_vulnerable': [0, 0, 1, 1, 0, 1, 0, 0]
}

df = pd.DataFrame(training_data)
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['code_snippet'])
model = RandomForestClassifier()
model.fit(X, df['is_vulnerable'])

# 2. improved scanning function
def scan_directory(path):
    # convert input path into absolute path (for debugging)
    abs_path = os.path.abspath(path)
    print(f"scanning path confirmed: {abs_path}")
    
    file_count = 0
    
    for root, dirs, files in os.walk(path):
        # skip .git and env folder (for performance and accuracy)
        if '.git' in root or 'env' in root.lower():
            continue
            
        for file in files:
            if file.endswith(".py"):
                file_count += 1
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    
                    # skip if file is empty
                    if not code.strip():
                        continue
                        
                    new_X = vectorizer.transform([code])
                    prediction = model.predict(new_X)
                    
                    status = "⚠️ [danger]" if prediction[0] == 1 else "✅ [safe]"
                    print(f"{status} {file_path}")
                except Exception as e:
                    print(f"❌ error ({file}): {e}")
    
    if file_count == 0:
        print("❓ Could not find python files to scan. Check the path")
    else:
        print(f"\n Total {file_count} files analyzed.")

# 3. scan (current folder)
scan_directory('.')