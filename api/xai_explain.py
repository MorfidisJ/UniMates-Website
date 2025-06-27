import joblib
import shap
import numpy as np
from ml_model_loader import compute_features

MODEL_PATH = 'match_model.pkl'
model = joblib.load(MODEL_PATH)
explainer = shap.Explainer(model)

def get_shap_explanation(user1, user2):
    feats = compute_features(user1, user2)
    shap_values = explainer(feats)
    # Return SHAP values as a dict for each feature
    return shap_values.values[0].tolist(), shap_values.data[0].tolist() 