"""User profile setup page."""
import streamlit as st
from datetime import datetime
from database import get_user_profile, create_user_profile, update_user_profile, get_user_by_id, update_user_password
from health_calculations import calculate_bmr_harris_benedict, calculate_tdee, calculate_daily_calorie_goal, get_bmi_category, calculate_bmi
from auth import hash_password, verify_password

def calculate_age_from_dob(dob):
    """Calculate age from date of birth."""
    today = datetime.now().date()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

def show_profile_setup(user_id):
    """Show user profile setup and editing page."""
    
    st.title("👤 Your Profile")
    
    # Get existing profile
    profile = get_user_profile(user_id)
    
    if profile:
        st.success("✅ Profile already set up. You can update your information below.")
        profile_dict = dict(profile)
    else:
        st.info("ℹ️ Let's set up your profile to calculate your daily calorie needs.")
        profile_dict = None
    
    st.divider()
    
    # Profile form
    col1, col2 = st.columns(2)
    
    with col1:
        # Date of Birth or Age input
        dob_input_method = st.radio(
            "How would you like to enter your age?",
            ["Date of Birth", "Direct Age Entry"],
            horizontal=True
        )
        
        dob = None  # Initialize DOB variable
        
        if dob_input_method == "Date of Birth":
            default_dob = datetime.now().date()
            if profile_dict and profile_dict.get('dob'):
                # Use existing DOB from database
                try:
                    default_dob = datetime.strptime(profile_dict['dob'], '%Y-%m-%d').date()
                except:
                    pass
            elif profile_dict and profile_dict.get('age'):
                # Estimate DOB from age if no DOB exists
                default_dob = datetime(datetime.now().year - profile_dict['age'], 1, 1).date()
            
            dob = st.date_input(
                "Date of Birth",
                value=default_dob,
                min_value=datetime(1920, 1, 1).date(),
                max_value=datetime.now().date(),
                format="DD/MM/YYYY"
            )
            age = calculate_age_from_dob(dob)
            st.info(f"📅 Age: **{age} years old** | DOB: **{dob.strftime('%d/%m/%Y')}**")
        else:
            dob = None
            age = st.number_input(
                "Age (years)",
                min_value=13.0,
                max_value=120.0,
                value=float(profile_dict['age']) if profile_dict and profile_dict['age'] else 30.0,
                step=1.0
            )
            age = int(age)
        
        sex = st.radio(
            "Sex",
            ["Male", "Female"],
            index=0 if profile_dict and profile_dict['sex'] == 'M' else 1
        )
        sex_code = 'M' if sex == 'Male' else 'F'
    
    with col2:
        # Height with unit selection
        height_unit = st.radio(
            "Height Unit",
            ["Centimeters (cm)", "Feet & Inches (ft'in\")"],
            horizontal=True
        )
        
        if height_unit == "Centimeters (cm)":
            height_cm = st.number_input(
                "Height (cm)",
                min_value=100.0,
                max_value=250.0,
                value=float(profile_dict['height']) if profile_dict and profile_dict['height'] else 170.0,
                step=0.1
            )
        else:
            # Feet and inches input
            col_ft, col_in = st.columns(2)
            with col_ft:
                feet = st.number_input(
                    "Feet",
                    min_value=3.0,
                    max_value=8.0,
                    value=5.0 if not profile_dict else float(profile_dict['height']) / 30.48 // 1,
                    step=1.0
                )
            with col_in:
                inches = st.number_input(
                    "Inches",
                    min_value=0.0,
                    max_value=11.99,
                    value=7.0 if not profile_dict else (float(profile_dict['height']) / 2.54) % 12,
                    step=0.5
                )
            # Convert to cm
            height_cm = (feet * 12 + inches) * 2.54
        
        weight_unit = st.radio(
            "Weight Unit",
            ["Kilograms (kg)", "Pounds (lbs)"],
            horizontal=True
        )
        
        if weight_unit == "Kilograms (kg)":
            weight_kg = st.number_input(
                "Weight (kg)",
                min_value=30.0,
                max_value=200.0,
                value=float(profile_dict['weight']) if profile_dict and profile_dict['weight'] else 70.0,
                step=0.1
            )
        else:
            weight_lbs = st.number_input(
                "Weight (lbs)",
                min_value=66.0,
                max_value=440.0,
                value=float(profile_dict['weight']) * 2.20462 if profile_dict and profile_dict['weight'] else 154.0,
                step=0.1
            )
            # Convert to kg
            weight_kg = weight_lbs / 2.20462
        
        weight = weight_kg
    
    st.divider()
    
    # Activity level
    st.subheader("🏃 Activity Level")
    
    activity_descriptions = {
        'sedentary': 'Little or no exercise',
        'light': 'Light exercise 1-3 days/week',
        'moderate': 'Moderate exercise 3-5 days/week',
        'active': 'Heavy exercise 6-7 days/week',
        'very_active': 'Very heavy exercise or physical job'
    }
    
    activity_level = st.selectbox(
        "Select your activity level:",
        options=list(activity_descriptions.keys()),
        format_func=lambda x: f"{x.replace('_', ' ').title()} - {activity_descriptions[x]}",
        index=2 if not profile_dict else list(activity_descriptions.keys()).index(profile_dict['activity_level'])
    )
    
    st.divider()
    
    # Fitness goal
    st.subheader("🎯 Fitness Goal")
    
    fitness_goal = st.radio(
        "What is your fitness goal?",
        ["Lose Weight", "Maintain Weight", "Gain Muscle"],
        horizontal=True
    )
    
    goal_map = {
        'Lose Weight': 'lose_weight',
        'Maintain Weight': 'maintain',
        'Gain Muscle': 'gain_muscle'
    }
    goal = goal_map[fitness_goal]
    
    st.divider()
    
    # Dietary preferences
    st.subheader("🍽️ Dietary Preferences")
    
    dietary_prefs = st.multiselect(
        "Select your dietary preferences:",
        ["Non-Vegetarian", "Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Low-Carb", "No Preferences"],
        default=["No Preferences"] if not profile_dict or not profile_dict['dietary_preference'] else profile_dict['dietary_preference'].split(", ")
    )
    dietary_preference = ", ".join(dietary_prefs) if dietary_prefs else "No Preferences"
    
    health_conditions = st.text_area(
        "Any health conditions or allergies? (optional)",
        value=profile_dict['health_conditions'] if profile_dict and profile_dict['health_conditions'] else ""
    )
    
    st.divider()
    
    # Calculate health metrics
    st.subheader("📊 Your Health Metrics")
    
    bmi = calculate_bmi(weight, height_cm)
    bmi_category = get_bmi_category(bmi)
    bmr = calculate_bmr_harris_benedict(age, sex_code, weight, height_cm)
    tdee = calculate_tdee(bmr, activity_level)
    daily_calorie_goal = calculate_daily_calorie_goal(tdee, goal)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("BMI", f"{bmi}", bmi_category)
    
    with col2:
        st.metric("BMR", f"{int(bmr)} cal/day")
    
    with col3:
        st.metric("TDEE", f"{int(tdee)} cal/day")
    
    with col4:
        st.metric("Daily Goal", f"{int(daily_calorie_goal)} cal/day")
    
    # Display health insights
    st.info(
        f"**Health Summary:**\n\n"
        f"- Your Basal Metabolic Rate (BMR) is {int(bmr)} calories/day (energy at rest)\n"
        f"- With {activity_level.replace('_', ' ').lower()} activity, you burn ~{int(tdee)} calories/day\n"
        f"- To {goal.replace('_', ' ').lower()}, aim for **{int(daily_calorie_goal)} calories/day**\n"
        f"- Your BMI is {bmi} ({bmi_category})"
    )
    
    st.divider()
    
    # Macro split preferences
    st.subheader("🥗 Macronutrient Split")
    
    macro_split = st.selectbox(
        "Choose your preferred macro split:",
        ["Balanced (30% Protein, 50% Carbs, 20% Fat)",
         "Low Carb (40% Protein, 30% Carbs, 30% Fat)",
         "High Protein (35% Protein, 35% Carbs, 30% Fat)"],
        index=0
    )
    
    macro_map = {
        "Balanced (30% Protein, 50% Carbs, 20% Fat)": "balanced",
        "Low Carb (40% Protein, 30% Carbs, 30% Fat)": "low_carb",
        "High Protein (35% Protein, 35% Carbs, 30% Fat)": "high_protein"
    }
    macro_split_key = macro_map[macro_split]
    
    st.divider()
    
    # Save button
    if st.button("💾 Save Profile", use_container_width=True, type="primary"):
        try:
            if profile_dict:
                # Update existing profile
                update_user_profile(
                    user_id,
                    age=age,
                    sex=sex_code,
                    height=height_cm,
                    weight=weight,
                    activity_level=activity_level,
                    dietary_preference=dietary_preference,
                    health_conditions=health_conditions,
                    daily_calorie_goal=daily_calorie_goal,
                    bmr=bmr,
                    tdee=tdee,
                    dob=dob
                )
                st.success("✅ Profile Saved Successfully!")
                st.balloons()
            else:
                # Create new profile
                create_user_profile(
                    user_id,
                    age=age,
                    sex=sex_code,
                    height=height_cm,
                    weight=weight,
                    activity_level=activity_level,
                    dietary_preference=dietary_preference,
                    health_conditions=health_conditions,
                    daily_calorie_goal=daily_calorie_goal,
                    bmr=bmr,
                    tdee=tdee,
                    dob=dob
                )
                st.success("✅ Profile Saved Successfully!")
                st.balloons()
            
            # Store macro split in session
            st.session_state['macro_split'] = macro_split_key
            
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error saving profile: {str(e)}")
    
    # Password Change Section
    st.divider()
    st.subheader("🔐 Security Settings")
    
    with st.expander("Change Password"):
        col1, col2 = st.columns(2)
        
        with col1:
            current_password = st.text_input("Current Password", type="password", key="current_pwd")
        with col2:
            st.write("")  # Spacer
        
        new_password = st.text_input("New Password", type="password", key="new_pwd")
        confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_pwd")
        
        if st.button("✅ Update Password", key="update_pwd_btn"):
            # Validate inputs
            if not current_password:
                st.error("❌ Please enter your current password")
            elif not new_password:
                st.error("❌ Please enter a new password")
            elif not confirm_new_password:
                st.error("❌ Please confirm your new password")
            elif new_password != confirm_new_password:
                st.error("❌ New passwords do not match")
            elif len(new_password) < 6:
                st.error("❌ New password must be at least 6 characters long")
            else:
                # Get user from database
                user = get_user_by_id(st.session_state.user_id)
                if user:
                    # Verify current password
                    if verify_password(current_password, user[2]):  # user[2] is password hash
                        # Update password
                        new_password_hash = hash_password(new_password)
                        if update_user_password(st.session_state.user_id, new_password_hash):
                            st.success("✅ Password updated successfully!")
                        else:
                            st.error("❌ Failed to update password")
                    else:
                        st.error("❌ Current password is incorrect")
                else:
                    st.error("❌ User not found")

if __name__ == "__main__":
    if st.session_state.get('logged_in'):
        show_profile_setup(st.session_state.user_id)
    else:
        st.error("Please login first")
