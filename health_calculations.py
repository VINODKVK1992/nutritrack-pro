"""Health calculations module for BMI, BMR, TDEE, and other health metrics."""
from datetime import datetime

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate Body Mass Index.
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
    
    Returns:
        BMI value rounded to 2 decimals
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)

def get_bmi_category(bmi):
    """Get BMI category."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmr_harris_benedict(age, sex, weight_kg, height_cm):
    """
    Calculate Basal Metabolic Rate using Harris-Benedict equation.
    
    Args:
        age: Age in years
        sex: 'M' for male, 'F' for female
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
    
    Returns:
        BMR in calories per day
    """
    if sex.upper() == 'M':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:  # Female
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    
    return round(bmr, 2)

def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure based on activity level.
    
    Args:
        bmr: Basal Metabolic Rate
        activity_level: 'sedentary', 'light', 'moderate', 'active', 'very_active'
    
    Returns:
        TDEE in calories per day
    """
    activity_multipliers = {
        'sedentary': 1.2,        # Little or no exercise
        'light': 1.375,          # Light exercise 1-3 days/week
        'moderate': 1.55,        # Moderate exercise 3-5 days/week
        'active': 1.725,         # Heavy exercise 6-7 days/week
        'very_active': 1.9       # Very heavy exercise, physical job or training twice per day
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.5)
    tdee = bmr * multiplier
    return round(tdee, 2)

def calculate_daily_calorie_goal(tdee, goal='maintain'):
    """
    Calculate daily calorie goal based on fitness goal.
    
    Args:
        tdee: Total Daily Energy Expenditure
        goal: 'lose_weight', 'gain_muscle', 'maintain'
    
    Returns:
        Daily calorie goal
    """
    if goal == 'lose_weight':
        # 500 calorie deficit for ~0.5 kg loss per week
        return round(tdee - 500, 0)
    elif goal == 'gain_muscle':
        # 300 calorie surplus for muscle gain
        return round(tdee + 300, 0)
    else:  # maintain
        return round(tdee, 0)

def calculate_macros(daily_calories, macro_split='balanced'):
    """
    Calculate daily macronutrient targets.
    
    Args:
        daily_calories: Daily calorie goal
        macro_split: 'balanced', 'low_carb', 'high_protein'
    
    Returns:
        Dictionary with protein, carbs, fat targets in grams
    """
    macros = {}
    
    if macro_split == 'low_carb':
        # 40% protein, 30% fat, 30% carbs
        macros['protein_g'] = round((daily_calories * 0.40) / 4, 1)
        macros['fat_g'] = round((daily_calories * 0.30) / 9, 1)
        macros['carbs_g'] = round((daily_calories * 0.30) / 4, 1)
    elif macro_split == 'high_protein':
        # 35% protein, 35% carbs, 30% fat
        macros['protein_g'] = round((daily_calories * 0.35) / 4, 1)
        macros['carbs_g'] = round((daily_calories * 0.35) / 4, 1)
        macros['fat_g'] = round((daily_calories * 0.30) / 9, 1)
    else:  # balanced
        # 30% protein, 50% carbs, 20% fat
        macros['protein_g'] = round((daily_calories * 0.30) / 4, 1)
        macros['carbs_g'] = round((daily_calories * 0.50) / 4, 1)
        macros['fat_g'] = round((daily_calories * 0.20) / 9, 1)
    
    macros['calories'] = daily_calories
    return macros

def calculate_water_intake(weight_kg):
    """Calculate recommended daily water intake."""
    # General rule: 30-35 ml per kg of body weight
    return round(weight_kg * 0.035, 1)

def calculate_ideal_weight(height_cm, sex):
    """
    Calculate ideal weight range using Devine formula.
    
    Args:
        height_cm: Height in centimeters
        sex: 'M' or 'F'
    
    Returns:
        Tuple of (min_weight, max_weight) in kg
    """
    height_inches = height_cm / 2.54
    
    if sex.upper() == 'M':
        ideal_weight = 50 + (2.3 * (height_inches - 60))
    else:  # Female
        ideal_weight = 45.5 + (2.3 * (height_inches - 60))
    
    # Range is typically ±10%
    min_weight = round(ideal_weight * 0.9, 1)
    max_weight = round(ideal_weight * 1.1, 1)
    
    return min_weight, max_weight

def calculate_calories_burned_by_activity(activity, duration_minutes, weight_kg):
    """
    Estimate calories burned by specific activities.
    
    Args:
        activity: Type of activity
        duration_minutes: Duration in minutes
        weight_kg: Weight in kilograms
    
    Returns:
        Estimated calories burned
    """
    # MET (Metabolic Equivalent) values for various activities
    met_values = {
        'walking': 3.5,
        'running': 9.8,
        'cycling': 7.5,
        'swimming': 8.0,
        'yoga': 2.5,
        'strength_training': 6.0,
        'hiit': 10.0,
        'dancing': 5.5,
        'basketball': 8.0,
        'tennis': 7.3,
    }
    
    met = met_values.get(activity.lower(), 5.0)
    calories_burned = (met * weight_kg * duration_minutes) / 60
    
    return round(calories_burned, 1)

def get_health_insights(current_bmi, goal_weight, current_weight, daily_calories, tdee):
    """Generate health insights based on user data."""
    insights = []
    
    bmi_category = get_bmi_category(current_bmi)
    insights.append(f"Your current BMI is {current_bmi} ({bmi_category})")
    
    if goal_weight != current_weight:
        weight_diff = current_weight - goal_weight
        if weight_diff > 0:
            insights.append(f"You need to lose approximately {weight_diff:.1f} kg to reach your goal weight")
        else:
            insights.append(f"You need to gain approximately {abs(weight_diff):.1f} kg to reach your goal weight")
    
    calorie_diff = daily_calories - tdee
    if calorie_diff < 0:
        insights.append(f"You're in a {abs(calorie_diff):.0f} calorie deficit for weight loss (~{abs(calorie_diff)*7/3500:.1f} kg/week)")
    elif calorie_diff > 0:
        insights.append(f"You're in a {calorie_diff:.0f} calorie surplus for muscle gain (~{calorie_diff*7/3500:.1f} kg/week)")
    else:
        insights.append("You're maintaining your current weight")
    
    return insights
