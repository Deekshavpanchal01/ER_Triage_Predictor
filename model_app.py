from flask import Flask, render_template, request
import flask

app = Flask(__name__)

# Dummy prediction function for demonstration
def make_prediction(feature_dict):
    # Example: always return Not Critical and Critical with probabilities
    # Replace this with your real model logic
    prob_critical = 0.8 if feature_dict["HR"] > 120 or feature_dict["Saturation"] < 90 else 0.1
    prob_not_critical = 1 - prob_critical
    predictions = [
        {"name": "Not Critical", "prob": prob_not_critical},
        {"name": "Critical", "prob": prob_critical}
    ]
    pred = "Critical" if prob_critical > prob_not_critical else "Not Critical"
    return predictions, pred

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/predictor", methods=["POST", "GET"])
def predictor():
    if request.method == "POST":
        feature_dict = {}
        patient_name = request.form["patient_name"]
        feature_dict["Age"] = float(request.form["age"])
        feature_dict["HR"] = float(request.form["heart_rate"])
        feature_dict["BT"] = float(request.form["body_temp"])
        feature_dict["Saturation"] = float(request.form["oxygen_saturation"])
        # Get all checked symptoms as a list
        symptoms_selected = request.form.getlist("symptoms")
        feature_dict["Chief_complain"] = ', '.join(symptoms_selected)
        # Get pain level and AVPU from form
        pain_level = request.form.get("pain_level", 0)
        avpu = request.form.get("avpu", "Alert")
        feature_dict["Pain_Level"] = int(pain_level)
        feature_dict["AVPU"] = avpu

        predictions, pred = make_prediction(feature_dict)

        # Determine recommended action based on prediction
        if predictions[1]['prob'] > 0.5:
            recommended_action = "Immediate medical attention required."
        else:
            recommended_action = "No immediate action required. Routine check-up is sufficient."

        # Calculate estimated wait time based on prediction
        max_pred = max(predictions, key=lambda x: x['prob'])
        pred_clean = max_pred['name'].strip().lower()
        if pred_clean == "critical":
            estimated_wait = "< 30 minutes"
        elif pred_clean == "not critical":
            estimated_wait = "> 30 minutes or No wait Time required,You are normal."
        else:
            estimated_wait = "You are normal. No wait time required."

        return flask.render_template(
            'home.html',
            prediction=predictions,
            pred=pred,
            patient_name=patient_name,
            recommended_action=recommended_action,
            symptoms_selected=symptoms_selected,
            pain_level=pain_level,
            avpu=avpu,
            estimated_wait=estimated_wait
        )
    else:
        return flask.render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)