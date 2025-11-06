from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def generate_plan(bmi_category, age):
    plan = {}

    # === DIET ===
    if bmi_category == "Underweight":
        plan['Diet'] = (
            "- Eat nutrient-dense foods: nuts, seeds, avocados, whole grains, lean proteins (chicken, fish, eggs, legumes).\n"
            "- Eat 5–6 small meals per day instead of 2–3 large ones.\n"
            "- Add healthy fats: olive oil, peanut butter, full-fat dairy (if tolerated).\n"
            "- Include protein with every meal to support muscle gain.\n"
            "- Avoid empty calories (soda, candy); focus on quality calories."
        )
    elif bmi_category == "Normal weight":
        plan['Diet'] = (
            "- Maintain balanced diet: fruits, vegetables, whole grains, lean proteins, healthy fats.\n"
            "- Control portion sizes to prevent gradual weight gain.\n"
            "- Limit processed foods, added sugars, and saturated fats.\n"
            "- Stay hydrated (6–8 glasses of water/day).\n"
            "- Include fiber-rich foods for digestive health."
        )
    else:  # Overweight or Obese
        plan['Diet'] = (
            "- Reduce calorie intake moderately (500 kcal/day deficit for gradual loss).\n"
            "- Prioritize vegetables, lean proteins (fish, tofu, legumes), and whole grains.\n"
            "- Avoid sugary drinks, refined carbs (white bread, pastries), and fried foods.\n"
            "- Eat mindfully: slow down, avoid distractions, stop when 80% full.\n"
            "- Use smaller plates to control portions."
        )

    # === EXERCISE ===
    if age < 18:
        plan['Exercise'] = (
            "- At least 60 minutes of moderate-to-vigorous physical activity daily (WHO).\n"
            "- Include aerobic, muscle-strengthening, and bone-strengthening activities.\n"
            "- Limit recreational screen time to <2 hours/day."
        )
    elif 18 <= age <= 64:
        if bmi_category == "Underweight":
            plan['Exercise'] = (
                "- Focus on strength training 2–3x/week to build muscle.\n"
                "- Limit excessive cardio (can burn needed calories).\n"
                "- Include light aerobic activity (walking, yoga) for heart health."
            )
        else:
            plan['Exercise'] = (
                "- 150–300 minutes of moderate aerobic activity weekly (e.g., brisk walking, cycling).\n"
                "- Include strength training 2x/week (major muscle groups).\n"
                "- Add daily movement: walking, stairs, standing desk.\n"
                "- For weight loss: aim for 250+ minutes/week of moderate activity."
            )
    else:  # age 65+
        plan['Exercise'] = (
            "- 150 minutes of moderate aerobic activity weekly (e.g., brisk walking, swimming).\n"
            "- Balance exercises 3x/week (tai chi, heel-to-toe walk) to prevent falls.\n"
            "- Strength training 2x/week (light weights, resistance bands).\n"
            "- Stay flexible with stretching or yoga."
        )

    # === LIFESTYLE ===
    plan['Lifestyle'] = (
        "- Sleep 7–9 hours per night (poor sleep affects hunger hormones).\n"
        "- Manage stress (meditation, deep breathing, hobbies) – stress leads to emotional eating.\n"
        "- Avoid smoking and limit alcohol (≤1 drink/day for women, ≤2 for men).\n"
        "- Monitor progress weekly (weight, waist circumference, energy levels).\n"
        "- Consult a doctor before starting any new diet/exercise if you have chronic conditions."
    )

    return plan

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        age = int(data['age'])
        weight_unit = data['weight_unit']
        height_unit = data['height_unit']

        if weight_unit == 'kg':
            weight_kg = float(data['weight'])
        else:  # lbs
            weight_kg = float(data['weight']) * 0.453592

        if height_unit == 'cm':
            height_m = float(data['height']) / 100.0
        else:  # ft/in
            feet = int(data['feet'])
            inches = float(data['inches'])
            total_inches = feet * 12 + inches
            height_m = total_inches * 0.0254

        bmi = round(weight_kg / (height_m ** 2), 1)
        category = classify_bmi(bmi)
        plan = generate_plan(category, age)

        # Format plan for HTML (convert newlines to <br>)
        formatted_plan = {k: v.replace('\n', '<br>') for k, v in plan.items()}

        return jsonify({
            'success': True,
            'bmi': bmi,
            'category': category,
            'plan': formatted_plan
        })
    except Exception as e:
        return jsonify({'success': False, 'error': 'Invalid input. Please check your entries.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
