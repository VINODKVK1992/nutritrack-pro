"""Food recommendations page."""
import streamlit as st
from datetime import datetime
from database import get_user_profile, save_meal_plan, get_meal_plans
from api_service import generate_food_recommendations
import json
import io
import pandas as pd

def show_food_recommendations(user_id):
    """Show personalized food recommendations."""
    
    st.title("🍎 Food Recommendations")
    
    # Get user profile
    profile = get_user_profile(user_id)
    if not profile:
        st.error("Please set up your profile first")
        return
    
    profile_dict = dict(profile)
    
    st.info(
        f"📊 **Your Profile:** {profile_dict['age']} years old, "
        f"{profile_dict['activity_level'].replace('_', ' ').title()}, "
        f"Daily Goal: {int(profile_dict['daily_calorie_goal'])} calories"
    )
    
    st.divider()
    
    # Tabs
    tab1, tab2 = st.tabs(["🤖 Generate Recommendations", "📋 Saved Plans"])
    
    with tab1:
        st.subheader("Get Your Personalized Meal Plan")
        
        # Plan duration selection
        col1, col2 = st.columns(2)
        
        with col1:
            plan_duration = st.selectbox(
                "Select meal plan duration",
                ["Single Day", "1 Week", "1 Month"],
                key="plan_duration"
            )
        
        with col2:
            st.write("**Current Dietary Preferences:**")
            st.write(profile_dict['dietary_preference'] or "No preferences specified")
        
        st.divider()
        
        # Meal selection for the day
        st.subheader("Select Meals to Include")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            include_breakfast = st.checkbox("🌅 Breakfast", value=True, key="breakfast")
        with col2:
            include_lunch = st.checkbox("🍽️ Lunch", value=True, key="lunch")
        with col3:
            include_snacks = st.checkbox("🍿 Snacks", value=True, key="snacks")
        with col4:
            include_dinner = st.checkbox("🌙 Dinner", value=True, key="dinner")
        
        st.divider()
        
        # Additional preferences
        dietary_focus = st.multiselect(
            "What would you like the meal plan to focus on?",
            [
                "Weight Loss", 
                "Muscle Gain", 
                "Balanced Nutrition", 
                "Quick Meals", 
                "Budget-Friendly",
                "Pregnancy Planning (Women)",
                "Fertility Boost (Women)",
                "Fertility Boost (Men)",
                "Pre-Conception Diet",
                "High Protein",
                "Low Carb",
                "Heart Healthy",
                "Diabetes Friendly",
                "Anti-Inflammatory",
                "Gut Health",
                "Energy Boost",
                "Immune Support"
            ],
            default=["Balanced Nutrition"],
            key="dietary_focus"
        )
        
        cuisine_preference = st.multiselect(
            "Preferred cuisines (if any)",
            ["Indian", "Italian", "Mediterranean", "Asian", "American", "Mexican", "No Preference"],
            default=["No Preference"],
            key="cuisine"
        )
        
        allergies = st.text_area(
            "Any allergies or foods to avoid?",
            placeholder="e.g., nuts, shellfish, dairy",
            height=50,
            key="allergies"
        )
        
        cooking_time = st.selectbox(
            "Preferred cooking time",
            ["Quick (under 20 min)", "Medium (20-40 min)", "Flexible (no limit)"],
            key="cooking_time"
        )
        
        plan_name = st.text_input(
            "Name for this plan (optional)",
            placeholder=f"e.g., {datetime.now().strftime('%A')}'s Meal Plan",
            key="plan_name"
        )
        
        st.divider()
        
        if st.button("🤖 Generate Meal Plan", use_container_width=True, type="primary"):
            # Build meal selection string
            selected_meals = []
            if include_breakfast:
                selected_meals.append("Breakfast")
            if include_lunch:
                selected_meals.append("Lunch")
            if include_snacks:
                selected_meals.append("Snacks")
            if include_dinner:
                selected_meals.append("Dinner")
            
            if not selected_meals:
                st.error("Please select at least one meal type")
            else:
                with st.spinner("🔄 Generating personalized meal plan..."):
                    try:
                        # Prepare user data
                        user_data = {
                            'age': profile_dict['age'],
                            'sex': profile_dict['sex'],
                            'activity_level': profile_dict['activity_level'],
                            'bmi': 'Normal' if 18.5 <= profile_dict.get('bmi', 22) < 25 else 'Other'
                        }
                        
                        dietary_prefs = f"{profile_dict['dietary_preference']}, {', '.join(dietary_focus)}"
                        if allergies:
                            dietary_prefs += f", Avoid: {allergies}"
                        if cuisine_preference and 'No Preference' not in cuisine_preference:
                            dietary_prefs += f", Prefer: {', '.join(cuisine_preference)}"
                        
                        dietary_prefs += f", Include meals: {', '.join(selected_meals)}"
                        
                        # Add specific instructions for weekly/monthly plans
                        if plan_duration == "1 Week":
                            dietary_prefs += f", Duration: {plan_duration} - IMPORTANT: Generate 7 DIFFERENT daily meal plans (Day 1 through Day 7 or Monday through Sunday). Each day should have UNIQUE meals with variety. Do not repeat the same meals across days."
                        elif plan_duration == "1 Month":
                            dietary_prefs += f", Duration: {plan_duration} - IMPORTANT: Generate 30 DIFFERENT daily meal plans. Ensure variety across all days."
                        else:
                            dietary_prefs += f", Duration: {plan_duration}"
                        
                        # Generate recommendations
                        result = generate_food_recommendations(
                            user_data,
                            dietary_prefs,
                            int(profile_dict['daily_calorie_goal']),
                            plan_duration=plan_duration,
                            selected_meals=selected_meals
                        )
                        
                        if result['success']:
                            recommendations = result['data']
                            
                            # Store in session state for saving later
                            st.session_state['generated_plan'] = {
                                'recommendations': recommendations,
                                'plan_duration': plan_duration,
                                'plan_name': plan_name
                            }
                            
                            st.success("✅ Meal plan generated successfully!")
                            st.rerun()
                            
                            # Display meal plan
                            st.subheader("Your Personalized Meal Plan")
                            
                            # Print to console
                            print("\n" + "="*80)
                            print("MEAL PLAN GENERATED")
                            print("="*80)
                            print(f"Plan Duration: {plan_duration}")
                            print(f"Meals Included: {', '.join(selected_meals)}")
                            print(f"Generated at: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                            print("="*80 + "\n")
                            
                            if 'meal_plan' in recommendations:
                                # Group meals by day
                                meals_by_day = {}
                                for meal in recommendations['meal_plan']:
                                    day = meal.get('day', 1)
                                    day_name = meal.get('day_name', f'Day {day}')
                                    if day not in meals_by_day:
                                        meals_by_day[day] = {'day_name': day_name, 'meals': []}
                                    meals_by_day[day]['meals'].append(meal)
                                
                                # Display by day
                                for day in sorted(meals_by_day.keys()):
                                    day_data = meals_by_day[day]
                                    st.subheader(f"📅 {day_data['day_name']}")
                                    
                                    for meal in day_data['meals']:
                                        with st.expander(f"🍽️ {meal['meal'].title()} - {meal.get('time', 'N/A')}"):
                                            st.write(f"**Meal Time:** {meal.get('time', 'N/A')}")
                                            st.write(f"**Calories:** {int(meal.get('meal_total_calories', 0))}")
                                            
                                            st.write("**Foods:**")
                                            for food in meal.get('foods', []):
                                                st.write(
                                                    f"- **{food['name']}** ({food['quantity']}) - "
                                                    f"{int(food['calories'])} cal, "
                                                    f"P:{food['protein_g']}g, "
                                                    f"C:{food['carbs_g']}g, "
                                                    f"F:{food['fat_g']}g"
                                                )
                                            
                                            if meal.get('tips'):
                                                st.info(f"💡 **Tip:** {meal['tips']}")
                                    
                                    st.divider()
                            
                            # Daily totals
                            st.divider()
                            st.subheader("Daily Totals")
                            
                            daily_totals = recommendations.get('daily_totals', {})
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric(
                                    "Calories",
                                    f"{int(daily_totals.get('calories', 0))}",
                                    delta=f"{int(daily_totals.get('calories', 0) - profile_dict['daily_calorie_goal'])}"
                                )
                            
                            with col2:
                                st.metric("Protein", f"{daily_totals.get('protein_g', 0):.0f}g")
                            
                            with col3:
                                st.metric("Carbs", f"{daily_totals.get('carbs_g', 0):.0f}g")
                            
                            with col4:
                                st.metric("Fat", f"{daily_totals.get('fat_g', 0):.0f}g")
                            
                            # Print totals to console
                            print("="*80)
                            print("DAILY TOTALS")
                            print("="*80)
                            print(f"Total Calories: {int(daily_totals.get('calories', 0))} cal")
                            print(f"Total Protein: {daily_totals.get('protein_g', 0):.1f}g")
                            print(f"Total Carbs: {daily_totals.get('carbs_g', 0):.1f}g")
                            print(f"Total Fat: {daily_totals.get('fat_g', 0):.1f}g")
                            print("="*80 + "\n")
                            
                            # Notes
                            if recommendations.get('notes'):
                                st.divider()
                                st.info(f"📝 **Notes:** {recommendations['notes']}")
                            
                            # Download and Save options
                            st.divider()
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Create DataFrame for download with day information
                                meal_data = []
                                
                                for meal in recommendations.get('meal_plan', []):
                                    day_label = meal.get('day_name', f"Day {meal.get('day', 1)}")
                                    
                                    for food in meal.get('foods', []):
                                        meal_data.append({
                                            'Day': day_label,
                                            'Meal Type': meal['meal'].title(),
                                            'Time': meal.get('time', 'N/A'),
                                            'Food Name': food['name'],
                                            'Quantity': food['quantity'],
                                            'Calories': int(food['calories']),
                                            'Protein (g)': food['protein_g'],
                                            'Carbs (g)': food['carbs_g'],
                                            'Fat (g)': food['fat_g']
                                        })
                                
                                df = pd.DataFrame(meal_data)
                                
                                # Download as CSV
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download as CSV",
                                    data=csv,
                                    file_name=f"meal_plan_{plan_duration.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            
                            with col2:
                                # Download as Excel with better formatting
                                output = io.BytesIO()
                                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                    df.to_excel(writer, sheet_name='Meal Plan', index=False)
                                    
                                    # Get workbook and worksheet
                                    workbook = writer.book
                                    worksheet = writer.sheets['Meal Plan']
                                    
                                    # Auto-adjust column widths
                                    for column in worksheet.columns:
                                        max_length = 0
                                        column_letter = column[0].column_letter
                                        for cell in column:
                                            try:
                                                if len(str(cell.value)) > max_length:
                                                    max_length = len(str(cell.value))
                                            except:
                                                pass
                                        adjusted_width = min(max_length + 2, 50)
                                        worksheet.column_dimensions[column_letter].width = adjusted_width
                                
                                output.seek(0)
                                
                                st.download_button(
                                    label="📊 Download as Excel",
                                    data=output.getvalue(),
                                    file_name=f"meal_plan_{plan_duration.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    use_container_width=True
                                )
                            
                            with col2:
                                if st.button("💾 Save This Meal Plan", use_container_width=True, key="save_meal_plan_btn", type="primary"):
                                    try:
                                        plan_name_final = plan_name or f"Meal Plan - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                                        
                                        print(f"\n{'='*80}")
                                        print("ATTEMPTING TO SAVE MEAL PLAN")
                                        print(f"{'='*80}")
                                        print(f"User ID: {user_id}")
                                        print(f"Plan Name: {plan_name_final}")
                                        print(f"Plan Duration: {plan_duration}")
                                        print(f"Daily Totals Calories: {daily_totals.get('calories', 0)}")
                                        print(f"Recommendations keys: {recommendations.keys()}")
                                        print(f"Number of meals: {len(recommendations.get('meal_plan', []))}")
                                        
                                        result = save_meal_plan(
                                            user_id,
                                            plan_name_final,
                                            plan_duration,
                                            recommendations,
                                            daily_totals.get('calories', 0)
                                        )
                                        
                                        print(f"Save result: {result}")
                                        print(f"{'='*80}\n")
                                        
                                        if result:
                                            st.success("✅ Meal plan saved successfully!")
                                            st.balloons()
                                            import time
                                            time.sleep(1)
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to save meal plan. Check console logs.")
                                    except Exception as e:
                                        st.error(f"❌ Error saving plan: {str(e)}")
                                        import traceback
                                        print(f"ERROR: {traceback.format_exc()}")
                                        st.error(traceback.format_exc())
                        
                        else:
                            st.error(f"❌ Failed to generate recommendations: {result.get('error', 'Unknown error')}")
                    
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        # Display generated plan if exists
        if 'generated_plan' in st.session_state:
            plan_data = st.session_state['generated_plan']
            recommendations = plan_data['recommendations']
            plan_duration = plan_data['plan_duration']
            plan_name = plan_data['plan_name']
            
            st.divider()
            st.subheader("Your Personalized Meal Plan")
            
            if 'meal_plan' in recommendations:
                meals_by_day = {}
                for meal in recommendations['meal_plan']:
                    day = meal.get('day', 1)
                    day_name = meal.get('day_name', f'Day {day}')
                    if day not in meals_by_day:
                        meals_by_day[day] = {'day_name': day_name, 'meals': []}
                    meals_by_day[day]['meals'].append(meal)
                
                for day in sorted(meals_by_day.keys()):
                    day_data = meals_by_day[day]
                    st.subheader(f"📅 {day_data['day_name']}")
                    for meal in day_data['meals']:
                        with st.expander(f"🍽️ {meal['meal'].title()} - {meal.get('time', 'N/A')}"):
                            st.write(f"**Calories:** {int(meal.get('meal_total_calories', 0))}")
                            for food in meal.get('foods', []):
                                st.write(f"- **{food['name']}** ({food['quantity']}) - {int(food['calories'])} cal")
                    st.divider()
            
            daily_totals = recommendations.get('daily_totals', {})
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Calories", f"{int(daily_totals.get('calories', 0))}")
            with col2:
                st.metric("Protein", f"{daily_totals.get('protein_g', 0):.0f}g")
            with col3:
                st.metric("Carbs", f"{daily_totals.get('carbs_g', 0):.0f}g")
            with col4:
                st.metric("Fat", f"{daily_totals.get('fat_g', 0):.0f}g")
            
            st.divider()
            if st.button("💾 Save Meal Plan", use_container_width=True, type="primary"):
                plan_name_final = plan_name or f"Meal Plan - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                result = save_meal_plan(user_id, plan_name_final, plan_duration, recommendations, daily_totals.get('calories', 0))
                if result:
                    st.success("✅ Saved!")
                    del st.session_state['generated_plan']
                    st.balloons()
                    import time
                    time.sleep(1)
                    st.rerun()
    
    with tab2:
        st.subheader("Your Saved Meal Plans")
        
        saved_plans = get_meal_plans(user_id)
        
        if saved_plans:
            for plan in saved_plans:
                plan_dict = dict(plan)
                # Format date as DD/MM/YYYY
                created_date = datetime.strptime(plan_dict['created_at'][:10], '%Y-%m-%d').strftime('%d/%m/%Y')
                
                with st.expander(f"📋 {plan_dict['plan_name']} - {created_date}", expanded=False):
                    st.write(f"**Duration:** {plan_dict['plan_type']}")
                    st.write(f"**Total Calories (per day):** {int(plan_dict['total_calories'])}")
                    st.write(f"**Created:** {created_date}")
                    
                    st.divider()
                    
                    # Parse meals data
                    try:
                        meals_data = json.loads(plan_dict['meals_data'])
                        
                        if 'meal_plan' in meals_data:
                            st.subheader("🍽️ Meal Plan Details")
                            
                            # Group meals by day
                            meals_by_day = {}
                            for meal in meals_data['meal_plan']:
                                day = meal.get('day', 1)
                                day_name = meal.get('day_name', f'Day {day}')
                                if day not in meals_by_day:
                                    meals_by_day[day] = {'day_name': day_name, 'meals': []}
                                meals_by_day[day]['meals'].append(meal)
                            
                            # Display by day
                            for day in sorted(meals_by_day.keys()):
                                day_data = meals_by_day[day]
                                st.write(f"**📅 {day_data['day_name']}**")
                                
                                for meal in day_data['meals']:
                                    st.write(f"  • **{meal['meal'].title()}** ({meal.get('time', 'N/A')}) - {int(meal.get('meal_total_calories', 0))} cal")
                                    for food in meal.get('foods', []):
                                        st.write(f"    - {food['name']} ({food['quantity']}) - {int(food['calories'])} cal")
                                
                                st.write("")  # Add spacing
                        
                        # Daily totals
                        if 'daily_totals' in meals_data:
                            st.divider()
                            st.subheader("📊 Daily Totals")
                            daily_totals = meals_data['daily_totals']
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Calories", f"{int(daily_totals.get('calories', 0))}")
                            with col2:
                                st.metric("Protein", f"{daily_totals.get('protein_g', 0):.0f}g")
                            with col3:
                                st.metric("Carbs", f"{daily_totals.get('carbs_g', 0):.0f}g")
                            with col4:
                                st.metric("Fat", f"{daily_totals.get('fat_g', 0):.0f}g")
                        
                        # Shopping list removed
                        
                        # Notes
                        if meals_data.get('notes'):
                            st.divider()
                            st.info(f"📝 **Notes:** {meals_data['notes']}")
                    
                    except Exception as e:
                        st.error(f"Error displaying meal plan: {str(e)}")
                        st.write("Raw data:", plan_dict['meals_data'][:200] + "...")
        
        else:
            st.info("👉 No saved meal plans yet. Generate your first plan above!")

if __name__ == "__main__":
    if st.session_state.get('logged_in'):
        show_food_recommendations(st.session_state.user_id)
    else:
        st.error("Please login first")
