from sklearn.metrics import precision_score, recall_score, f1_score

def get_performance_metrics(df):
    """
    Simulates performance by treating the top 2% as Ground Truth 
    attacks for demonstration, or uses hidden labels if available.
    """
    # For the hackathon, we simulate a 'Validation Set'
    y_true = df['is_flagged'].values 
    y_pred = df['risk_score'] > 85 # Our threshold
    
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)
    
    return {
        "Precision": round(precision, 2),
        "Recall": round(recall, 2),
        "F1 Score": round(f1, 2),
        "Accuracy": round((y_true == y_pred).mean(), 2)
    }