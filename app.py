from flask import Flask, request, render_template_string
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
with open("RF.pkl", "rb") as file:
    model = pickle.load(file)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Bank Customer Churn Prediction</title>
    <style>
        body{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg,#1e3c72,#2a5298);
            margin:0;
            padding:0;
        }

        .container{
            width: 700px;
            margin: 40px auto;
            background:white;
            padding:30px;
            border-radius:15px;
            box-shadow:0 8px 20px rgba(0,0,0,0.2);
        }

        h1{
            text-align:center;
            color:#2a5298;
        }

        .grid{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:15px;
        }

        label{
            font-weight:bold;
        }

        input,select{
            width:100%;
            padding:10px;
            border:1px solid #ccc;
            border-radius:8px;
        }

        button{
            width:100%;
            padding:12px;
            background:#2a5298;
            color:white;
            border:none;
            border-radius:8px;
            font-size:16px;
            cursor:pointer;
            margin-top:20px;
        }

        button:hover{
            background:#1e3c72;
        }

        .result{
            text-align:center;
            margin-top:20px;
            font-size:22px;
            font-weight:bold;
        }

        .churn{
            color:red;
        }

        .stay{
            color:green;
        }
    </style>
</head>
<body>

<div class="container">

<h1>🏦 Bank Customer Churn Prediction</h1>

<form method="POST">

<div class="grid">

<div>
<label>Credit Score</label>
<input type="number" name="credit_score" required>
</div>

<div>
<label>Country</label>
<select name="country">
    <option>France</option>
    <option>Germany</option>
    <option>Spain</option>
</select>
</div>

<div>
<label>Gender</label>
<select name="gender">
    <option>Male</option>
    <option>Female</option>
</select>
</div>

<div>
<label>Age</label>
<input type="number" name="age" required>
</div>

<div>
<label>Tenure</label>
<input type="number" name="tenure" required>
</div>

<div>
<label>Balance</label>
<input type="number" step="0.01" name="balance" required>
</div>

<div>
<label>Products Number</label>
<input type="number" name="products_number" required>
</div>

<div>
<label>Credit Card</label>
<select name="credit_card">
    <option value="1">Yes</option>
    <option value="0">No</option>
</select>
</div>

<div>
<label>Active Member</label>
<select name="active_member">
    <option value="1">Yes</option>
    <option value="0">No</option>
</select>
</div>

<div>
<label>Estimated Salary</label>
<input type="number" step="0.01" name="estimated_salary" required>
</div>

</div>

<button type="submit">Predict</button>

</form>

{% if prediction %}
<div class="result {{ css }}">
    {{ prediction }}
</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    css = ""

    if request.method == "POST":

        country_map = {
            "France": 0,
            "Germany": 1,
            "Spain": 2
        }

        gender_map = {
            "Male": 1,
            "Female": 0
        }

        data = pd.DataFrame([{
            "credit_score": float(request.form["credit_score"]),
            "country": country_map[request.form["country"]],
            "gender": gender_map[request.form["gender"]],
            "age": float(request.form["age"]),
            "tenure": float(request.form["tenure"]),
            "balance": float(request.form["balance"]),
            "products_number": float(request.form["products_number"]),
            "credit_card": float(request.form["credit_card"]),
            "active_member": float(request.form["active_member"]),
            "estimated_salary": float(request.form["estimated_salary"])
        }])

        result = model.predict(data)[0]

        if result == 1:
            prediction = "⚠ Customer Likely to Churn"
            css = "churn"
        else:
            prediction = "✅ Customer Likely to Stay"
            css = "stay"

    return render_template_string(html,
                                  prediction=prediction,
                                  css=css)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
