import sys

def get_input_with_unit(prompt, unit_options):
    while True:
        try:
            print(prompt)
            for i, opt in enumerate(unit_options, 1):
                print(f"  {i}. {opt}")
            choice = int(input("Choose option number: "))
            if 1 <= choice <= len(unit_options):
                value = float(input(f"Enter value ({unit_options[choice-1]}): "))
                return value, choice
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def convert_to_metric(weight_val, weight_unit, height_val, height_unit):
    # Weight: 1 = kg, 2 = lbs
    if weight_unit == 2:
        weight_kg = weight_val * 0.453592
    else:
        weight_kg = weight_val

    # Height: 1 = cm, 2 = feet+inches
    if height_unit == 1:
        height_m = height_val / 100.0
    else:
        # We assume height_val is total inches if using ft/in — but better to ask separately
        feet = int(input("Enter feet: "))
        inches = float(input("Enter inches: "))
        total_inches = feet * 12 + inches
        height_m = total_inches * 0.0254

    return weight_kg, height_m

def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

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
    elif bmi_category in ["Overweight", "Obese"]:
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
            "- Include aerobic (running, cycling), muscle-strengthening (climbing, push-ups), and bone-strengthening (jumping) activities.\n"
            "- Limit screen time to <2 hours/day of recreational use."
        )
    elif 18 <= age <= 64:
        if bmi_category == "Underweight":
            plan['Exercise'] = (
                "- Focus on strength training 2–3x/week to build muscle (weights, resistance bands).\n"
                "- Limit excessive cardio (can burn needed calories).\n"
                "- Include light aerobic activity (walking, yoga) for heart health."
            )
        else:
            plan['Exercise'] = (
                "- 150–300 minutes of moderate aerobic activity OR 75–150 minutes of vigorous activity weekly (WHO/CDC).\n"
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

def main():
    print("=== Personalized BMI & Wellness Planner ===")
    print("Based on WHO, CDC, and Harvard School of Public Health Guidelines\n")

    try:
        age = int(input("Enter your age (years): "))
        if age < 2 or age > 120:
            print("Please enter a realistic age (2–120).")
            sys.exit(1)
    except ValueError:
        print("Invalid age.")
        sys.exit(1)

    weight_val, weight_unit = get_input_with_unit(
        "Select weight unit:",
        ["Kilograms (kg)", "Pounds (lbs)"]
    )

    height_val, height_unit = get_input_with_unit(
        "Select height unit:",
        ["Centimeters (cm)", "Feet and Inches"]
    )

    weight_kg, height_m = convert_to_metric(weight_val, weight_unit, height_val, height_unit)
    bmi = calculate_bmi(weight_kg, height_m)
    category = classify_bmi(bmi)

    print(f"\n📊 Your BMI: {bmi:.1f} → Category: {category}\n")

    plan = generate_plan(category, age)

    print("📋 Your Personalized Plan:\n")
    for section, advice in plan.items():
        print(f"🔹 {section}:")
        print(advice)
        print()

    print("ℹ️ Note: This is general advice. For personalized medical guidance, consult a healthcare professional.")

if __name__ == "__main__":
    main()
