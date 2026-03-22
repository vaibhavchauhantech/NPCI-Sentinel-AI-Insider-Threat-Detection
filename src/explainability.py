import shap
import pandas as pd
import matplotlib.pyplot as plt

class ThreatExplainer:
    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names
        # Use TreeExplainer for Isolation Forest (very fast)
        self.explainer = shap.TreeExplainer(model)

    def explain_anomaly(self, X_sample):
        # Calculate SHAP values
        shap_values = self.explainer.shap_values(X_sample)
        
        # Identify top contributing feature for the alert
        # We take the absolute highest SHAP value
        explanations = []
        for i in range(len(X_sample)):
            top_idx = shap_values[i].argmax()
            reason = f"High {self.feature_names[top_idx]} contribution"
            explanations.append(reason)
            
        return explanations, shap_values