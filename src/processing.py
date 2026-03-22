import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from hashlib import sha256

def process_data(email_path, psycho_path):
    # Load data
    emails = pd.read_csv(email_path)
    psycho = pd.read_csv(psycho_path)
    
    # 1. Privacy: Hash User IDs immediately 
    emails['user_hash'] = emails['user'].apply(lambda x: sha256(str(x).encode()).hexdigest()[:12])
    psycho['user_hash'] = psycho['user_id'].apply(lambda x: sha256(str(x).encode()).hexdigest()[:12])
    
    # 2. Tier 1: Metadata Features
    emails['date'] = pd.to_datetime(emails['date'])
    emails['hour'] = emails['date'].dt.hour
    emails['is_night'] = emails['hour'].apply(lambda x: 1 if x < 6 or x > 20 else 0)
    emails['attachment_count'] = emails['attachments'].apply(lambda x: len(str(x).split(';')) if pd.notnull(x) else 0)
    emails['recip_count'] = emails.apply(lambda x: len(str(x['to']).split(';')) + len(str(x['cc']).split(';')), axis=1)

    # 3. Tier 2: Sentiment/NLP Features (Simplified for speed)
    # Looking for 'disgruntled' keywords or exfiltration signals [cite: 63]
    suspicious_words = ['quit', 'resume', 'salary', 'password', 'access', 'download', 'bypass']
    emails['suspicion_content'] = emails['content'].str.lower().apply(
        lambda x: sum(1 for word in suspicious_words if word in str(x))
    )

    # 4. Merging with Psychometrics [cite: 50]
    # I use a LEFT JOIN to keep all email logs even if psychometric data is missing
    df = pd.merge(emails, psycho[['user_hash', 'O', 'C', 'E', 'A', 'N']], on='user_hash', how='left')
    
    # Handle Missing Psychometrics: Impute with population mean (Safe for accuracy)
    for col in ['O', 'C', 'E', 'A', 'N']:
        df[col] = df[col].fillna(df[col].mean())
        
    return df