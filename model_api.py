import pickle
import numpy as np

with open("model.pkl", "rb") as read_file:
    lr_model = pickle.load(read_file)

feature_names = lr_model.feature_names

def get_features():
    # Return a dict with all features set to 0 or empty string
    return {name: 0 for name in feature_names}
def make_prediction(feature_dict):
    x_input = [
        float(feature_dict[name]) if name in feature_dict else 0
        for name in lr_model.feature_names
    ]
    pred_probs = lr_model.predict_proba([x_input]).flat
    pred_class = lr_model.predict([x_input])[0]
    predictions = [
        {'name': lr_model.target_names[0], 'prob': pred_probs[0]},
        {'name': lr_model.target_names[1], 'prob': pred_probs[1]}
    ]
    if pred_class == 1:
        critical_message = "Patient is CRITICAL (High Priority)"
    else:
        critical_message = "Patient is NOT critical (Low Priority)"
    return predictions, critical_message

# Optional: test code
if __name__ == "__main__":
    # Example: all features set to 0
    test_features = get_features()
    print(make_prediction(test_features))