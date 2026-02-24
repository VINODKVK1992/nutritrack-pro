"""Home dashboard page."""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from database import get_food_log_by_date, get_user_profile, get_health_metrics
from health_calculations import calculate_bmi, get_bmi_category

def show_home_dashboard(user_id):
    """Show home dashboard with calorie tracking and health metrics."""
    
    # Get user profile
    profile = get_user_profile(user_id)
    if not profile:
        st.info("👋 Welcome! Let's set up your profile to get started with personalized nutrition tracking.")
        return
    
    st.title("🏠 Home Dashboard")
    
    # Convert profile to dict for easier access
    profile_dict = dict(profile)
    
    # Check for active meal plans and show today's plan
    from database import get_meal_plans
    import json
    
    meal_plans = get_meal_plans(user_id, limit=1)
    if meal_plans:
        latest_plan = dict(meal_plans[0])
        try:
            meals_data = json.loads(latest_plan['meals_data'])
            if 'meal_plan' in meals_data:
                st.info("🍽️ **Today's Meal Plan Reminder**")
                with st.expander("👁️ View Today's Recommended Meals", expanded=False):
                    st.write(f"**Plan:** {latest_plan['plan_name']}")
                    st.write(f"**Total Calories:** {int(latest_plan['total_calories'])} cal")
                    
                    for meal in meals_data['meal_plan'][:4]:  # Show first 4 meals
                        st.write(f"**{meal['meal'].title()}** ({meal.get('time', 'N/A')}) - {int(meal.get('meal_total_calories', 0))} cal")
                        for food in meal.get('foods', [])[:2]:  # Show first 2 foods per meal
                            st.write(f"  • {food['name']} ({food['quantity']})")
                    
                    st.caption("📌 Go to Recommendations → Saved Plans to view full details")
                st.divider()
        except:
            pass
    
    # Header with key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Daily Goal", f"{int(profile_dict['daily_calorie_goal'])} cal")
    
    with col2:
        bmi = calculate_bmi(profile_dict['weight'], profile_dict['height'])
        st.metric("BMI", f"{bmi}", f"{get_bmi_category(bmi)}")
    
    with col3:
        st.metric("Weight", f"{profile_dict['weight']:.2f} kg")
    
    with col4:
        st.metric("Height", f"{profile_dict['height']} cm")
    
    st.divider()
    
    # Today's calorie tracking
    st.subheader("📊 Today's Calorie Intake")
    
    today = datetime.now().date()
    food_log = get_food_log_by_date(user_id, today)
    
    if food_log:
        # Add Clear All button
        col1, col2, col3 = st.columns([6, 1, 1])
        with col3:
            if st.button("🗑️ Clear All", type="secondary", help="Delete all food entries for today"):
                from database import delete_all_food_logs_by_date
                rows_deleted = delete_all_food_logs_by_date(user_id, today)
                if rows_deleted > 0:
                    st.success(f"✅ Deleted {rows_deleted} food entries!")
                    st.rerun()
                else:
                    st.error("❌ Failed to delete entries")
        
        # Display food table with delete buttons
        foods_data = []
        for log in food_log:
            log_dict = dict(log)
            foods_data.append({
                "ID": log_dict['id'],
                "Meal Type": log_dict.get('meal_type', 'Snack'),
                "Food": log_dict['food_name'],
                "Calories": int(log_dict['calories'] or 0),
                "Protein (g)": round(log_dict['protein'] or 0, 1),
                "Carbs (g)": round(log_dict['carbs'] or 0, 1),
                "Fat (g)": round(log_dict['fat'] or 0, 1)
            })
        
        df_foods = pd.DataFrame(foods_data)
        
        # Display table
        st.dataframe(df_foods.drop(columns=['ID']), use_container_width=True, hide_index=True)
        
        # Delete row selector
        selected_food = st.selectbox(
            "Select food to delete",
            options=[(row['ID'], f"{row['Food']} - {row['Calories']} cal") for _, row in df_foods.iterrows()],
            format_func=lambda x: x[1],
            key="delete_selector"
        )
        if st.button("❌ Delete Selected", type="secondary"):
            from database import delete_food_log
            if delete_food_log(selected_food[0]):
                st.success("✅ Deleted!")
                st.rerun()
        
        st.divider()
        
        # Calculate totals
        total_calories = sum(log['calories'] or 0 for log in food_log)
        total_protein = sum(log['protein'] or 0 for log in food_log)
        total_carbs = sum(log['carbs'] or 0 for log in food_log)
        total_fat = sum(log['fat'] or 0 for log in food_log)
        
        # Remaining calories
        remaining = profile_dict['daily_calorie_goal'] - total_calories
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Consumed", f"{int(total_calories)} cal", 
                     f"{int(total_calories - profile_dict['daily_calorie_goal'])} cal")
        with col2:
            st.metric("Remaining", f"{int(remaining)} cal")
        with col3:
            percentage = (total_calories / profile_dict['daily_calorie_goal']) * 100
            st.metric("Progress", f"{percentage:.1f}%")
        with col4:
            st.metric("Protein Goal", f"{int(total_protein)}g")
        
        # Calorie breakdown pie chart
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=['Protein', 'Carbs', 'Fat'],
                values=[total_protein * 4, total_carbs * 4, total_fat * 9],
                hole=0.4,
                marker=dict(colors=['#FF6B6B', '#4ECDC4', '#FFE66D'])
            )
        ])
        fig_pie.update_layout(
            title="Macronutrient Breakdown",
            height=400
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Calorie progress bar
        progress_value = min(total_calories / profile_dict['daily_calorie_goal'], 1.0)
        st.progress(progress_value, text=f"{int(total_calories)} / {int(profile_dict['daily_calorie_goal'])} cal")
        
    else:
        st.info("No food entries for today yet. Add your first meal to get started!")
    
    st.divider()
    
    # Weekly overview
    st.subheader("📈 Weekly Overview")
    
    # Get last 7 days
    dates = [(today - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(6, -1, -1)]
    
    weekly_data = []
    for date_str in dates:
        import datetime as dt
        date_obj = dt.datetime.strptime(date_str, '%Y-%m-%d').date()
        logs = get_food_log_by_date(user_id, date_obj)
        daily_total = sum(log['calories'] or 0 for log in logs)
        # Format date as DD/MM/YYYY for display
        display_date = date_obj.strftime('%d/%m/%Y')
        weekly_data.append({
            'Date': display_date,
            'Calories': daily_total,
            'Goal': profile_dict['daily_calorie_goal']
        })
    
    df_weekly = pd.DataFrame(weekly_data)
    
    # Line chart for weekly trend
    fig_weekly = px.line(
        df_weekly,
        x='Date',
        y=['Calories', 'Goal'],
        markers=True,
        title='Weekly Calorie Trend',
        labels={'value': 'Calories', 'variable': 'Type'},
        color_discrete_map={'Calories': '#FF6B6B', 'Goal': '#4ECDC4'}
    )
    fig_weekly.update_layout(height=400)
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    st.divider()
    
    # Recent health metrics
    st.subheader("💪 Health Metrics")
    
    start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    
    health_metrics = get_health_metrics(user_id, start_date, end_date)
    
    if health_metrics:
        metrics_data = []
        for metric in health_metrics[-7:]:  # Last 7 entries
            metric_dict = dict(metric)
            metrics_data.append({
                'Date': metric_dict['date'],
                'Weight': metric_dict['weight'],
                'BMI': metric_dict['bmi'],
                'Sleep (hrs)': metric_dict['sleep_hours'],
                'Water (L)': metric_dict['water_intake_liters'],
                'Exercise (min)': metric_dict['exercise_minutes']
            })
        
        df_metrics = pd.DataFrame(metrics_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_weight = px.line(
                df_metrics,
                x='Date',
                y='Weight',
                markers=True,
                title='Weight Trend',
                color_discrete_sequence=['#FF6B6B']
            )
            fig_weight.update_layout(height=350)
            st.plotly_chart(fig_weight, use_container_width=True)
        
        with col2:
            fig_bmi = px.line(
                df_metrics,
                x='Date',
                y='BMI',
                markers=True,
                title='BMI Trend',
                color_discrete_sequence=['#4ECDC4']
            )
            fig_bmi.update_layout(height=350)
            st.plotly_chart(fig_bmi, use_container_width=True)
        
        # Display metrics table
        st.dataframe(df_metrics, use_container_width=True, hide_index=True)
    else:
        st.info("No health metrics recorded yet. Add your first entry in the Health Metrics section.")
    
    st.divider()
    
    # Quick stats
    st.subheader("📋 Quick Stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Activity Level:** {profile_dict['activity_level'].title()}")
    
    with col2:
        st.info(f"**Dietary Preference:** {profile_dict['dietary_preference'] or 'Not specified'}")
    
    with col3:
        st.info(f"**BMR:** {int(profile_dict['bmr'])} cal/day")

if __name__ == "__main__":
    if st.session_state.get('logged_in'):
        show_home_dashboard(st.session_state.user_id)
    else:
        st.error("Please login first")
