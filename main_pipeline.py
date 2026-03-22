import os
from src.processing import process_data
from src.detection import run_detection
from src.explainability import ThreatExplainer
import pandas as pd

# 1. Process with Sampling (To prevent the hang you experienced)
print("--- Step 1: Processing Logs (Sampling 50,000 rows for speed) ---")
# Use a smaller sample to ensure it works first
# Note: You might need to edit src/processing.py to accept 'nrows' in pd.read_csv
df = process_data('data/email.csv', 'data/psychometric.csv') 
df = df.sample(min(50000, len(df))) 

# 2. Detect
print("--- Step 2: Running Detection Engine ---")
df, fitted_iso_model = run_detection(df) # Getting the model back

# 3. Explain
print("--- Step 3: Generating Explanations via SHAP ---")
features = ['hour', 'is_night', 'attachment_count', 'recip_count', 'suspicion_content', 'O', 'C', 'E', 'A', 'N']
explainer = ThreatExplainer(fitted_iso_model, features)
df['threat_reason'], _ = explainer.explain_anomaly(df[features].values)

# 4. Save for Dashboard
if not os.path.exists('data'): os.makedirs('data')
df.to_csv('data/final_results.csv', index=False)
print(f"--- SUCCESS: {len(df)} records processed. Data ready for Dashboard ---")