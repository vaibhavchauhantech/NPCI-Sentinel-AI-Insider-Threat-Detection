from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
from sklearn.ensemble import IsolationForest
import numpy as np

class BehaviorAutoencoder(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8)
        )
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim)
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))

def run_detection(df):
    features = ['hour', 'is_night', 'attachment_count', 'recip_count', 'suspicion_content', 'O', 'C', 'E', 'A', 'N']
    X = df[features].values
    
    # 1. Isolation Forest
    iso = IsolationForest(contamination=0.02, random_state=42)
    iso.fit(X)
    iso_raw = iso.decision_function(X) * -1
    
    # 2. Autoencoder
    X_tensor = torch.FloatTensor(X)
    model = BehaviorAutoencoder(len(features))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    
    # Short training
    for _ in range(20): 
        output = model(X_tensor)
        loss = nn.MSELoss()(output, X_tensor)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        reconstructed = model(X_tensor)
        ae_raw = torch.mean((X_tensor - reconstructed)**2, dim=1).numpy()

    # 3. Normalization
    scaler = MinMaxScaler(feature_range=(0, 100))
    # Combine scores first, then scale
    combined_raw = (iso_raw + ae_raw).reshape(-1, 1)
    df['risk_score'] = scaler.fit_transform(combined_raw).flatten()
    
    # Flag based on top 2% of the NORMALIZED score
    df['is_flagged'] = df['risk_score'] > df['risk_score'].quantile(0.98) 
    
    return df, iso