from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    crime = data.get("crime")
    age = data.get("age")
    weapon = data.get("weapon")

    # make sure age is number
    try:
        age = int(age)
    except:
        age = 0

    # RULES (your current logic)
    if crime == "Homicide" or weapon == "Firearm":
        result = "High Risk 🔴"

    elif age < 18:
        result = "Sensitive Case 🟡"

    else:
        result = "Low Risk ✅"

    # ALWAYS RETURN OUTSIDE IF-ELSE (VERY IMPORTANT)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)