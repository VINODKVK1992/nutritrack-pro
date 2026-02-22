"""Food history and statistics page."""
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from database import get_food_log_range, get_user_profile

def show_food_history(user_id):
    """Show food history and statistics."""
    
    st.title("📚 Food History")
    
    # Get user profile
    profile = get_user_profile(user_id)
    if not profile:
        st.error("Please set up your profile first")
        return
    
    profile_dict = dict(profile)
    daily_goal = profile_dict['daily_calorie_goal']
    
    today = datetime.now().date()
    
    # Date range selection
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("From", today - timedelta(days=30))
    
    with col2:
        end_date = st.date_input("To", today)
    
    if start_date > end_date:
        st.error("End date must be after start date")
        return
    
    # Get food log for range
    food_logs = get_food_log_range(user_id, start_date, end_date)
    
    if food_logs:
        # Process data
        food_data = []
        daily_totals = {}
        
        for log in food_logs:
            log_dict = dict(log)
            
            date = log_dict['entry_date']
            # Format date as DD/MM/YYYY for display
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            display_date = date_obj.strftime('%d/%m/%Y')
            
            food_data.append({
                'Date': display_date,
                'Food': log_dict['food_name'],
                'Quantity': log_dict['quantity'],
                'Calories': log_dict['calories'] or 0,
                'Protein (g)': log_dict['protein'] or 0,
                'Carbs (g)': log_dict['carbs'] or 0,
                'Fat (g)': log_dict['fat'] or 0,
                'Fiber (g)': log_dict['fiber'] or 0
            })
            
            # Calculate daily totals
            if date not in daily_totals:
                daily_totals[date] = {
                    'calories': 0,
                    'protein': 0,
                    'carbs': 0,
                    'fat': 0,
                    'fiber': 0,
                    'items': 0
                }
            
            daily_totals[date]['calories'] += log_dict['calories'] or 0
            daily_totals[date]['protein'] += log_dict['protein'] or 0
            daily_totals[date]['carbs'] += log_dict['carbs'] or 0
            daily_totals[date]['fat'] += log_dict['fat'] or 0
            daily_totals[date]['fiber'] += log_dict['fiber'] or 0
            daily_totals[date]['items'] += 1
        
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📋 All Foods", "📊 Daily Summary", "📈 Statistics", "🍕 Food Frequency"])
        
        with tab1:
            st.subheader("All Food Entries")
            
            df_foods = pd.DataFrame(food_data)
            
            # Filters
            col1, col2 = st.columns(2)
            
            with col1:
                selected_dates = st.multiselect(
                    "Filter by date",
                    sorted(df_foods['Date'].unique(), reverse=True),
                    default=sorted(df_foods['Date'].unique(), reverse=True)[:7]
                )
            
            with col2:
                sort_by = st.selectbox(
                    "Sort by",
                    ["Date (Recent First)", "Date (Oldest First)", "Calories (High to Low)", "Calories (Low to High)"]
                )
            
            # Filter and sort
            df_filtered = df_foods[df_foods['Date'].isin(selected_dates)]
            
            if sort_by == "Date (Recent First)":
                df_filtered = df_filtered.sort_values('Date', ascending=False)
            elif sort_by == "Date (Oldest First)":
                df_filtered = df_filtered.sort_values('Date', ascending=True)
            elif sort_by == "Calories (High to Low)":
                df_filtered = df_filtered.sort_values('Calories', ascending=False)
            elif sort_by == "Calories (Low to High)":
                df_filtered = df_filtered.sort_values('Calories', ascending=True)
            
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            
            # Download option
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                csv,
                file_name=f"food_history_{today}.csv",
                mime="text/csv"
            )
        
        with tab2:
            st.subheader("Daily Summary")
            
            daily_summary_data = []
            for date, totals in sorted(daily_totals.items(), reverse=True):
                daily_summary_data.append({
                    'Date': date,
                    'Items': totals['items'],
                    'Calories': int(totals['calories']),
                    'Protein (g)': int(totals['protein']),
                    'Carbs (g)': int(totals['carbs']),
                    'Fat (g)': int(totals['fat']),
                    'Fiber (g)': int(totals['fiber']),
                    'vs Goal': int(totals['calories'] - daily_goal)
                })
            
            df_summary = pd.DataFrame(daily_summary_data)
            
            # Color code based on goal
            def color_code(val):
                if isinstance(val, int):
                    if val < daily_goal * 0.8:
                        return 'background-color: #FFE66D'
                    elif val < daily_goal * 1.1:
                        return 'background-color: #95E1D3'
                    else:
                        return 'background-color: #FF6B6B'
                return ''
            
            st.dataframe(
                df_summary.style.applymap(color_code, subset=['Calories']),
                use_container_width=True,
                hide_index=True
            )
        
        with tab3:
            st.subheader("Statistics")
            
            # Calculate statistics
            total_meals = len(food_logs)
            total_calories = sum(daily_totals[d]['calories'] for d in daily_totals)
            avg_daily_calories = total_calories / len(daily_totals) if daily_totals else 0
            avg_daily_protein = sum(daily_totals[d]['protein'] for d in daily_totals) / len(daily_totals) if daily_totals else 0
            avg_daily_carbs = sum(daily_totals[d]['carbs'] for d in daily_totals) / len(daily_totals) if daily_totals else 0
            avg_daily_fat = sum(daily_totals[d]['fat'] for d in daily_totals) / len(daily_totals) if daily_totals else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Meals", total_meals)
            
            with col2:
                st.metric("Total Calories", f"{int(total_calories)}")
            
            with col3:
                st.metric("Avg Daily", f"{int(avg_daily_calories)}", delta=f"{int(avg_daily_calories - daily_goal)}")
            
            with col4:
                st.metric("Days Logged", len(daily_totals))
            
            st.divider()
            
            # Daily calorie chart
            df_summary_sorted = df_summary.sort_values('Date')
            
            # Add Goal column for comparison
            df_summary_sorted['Goal'] = int(daily_goal)
            
            fig_daily = px.bar(
                df_summary_sorted,
                x='Date',
                y='Calories',
                title='Daily Calorie Intake vs Goal',
                labels={'value': 'Calories'},
                color_discrete_sequence=['#FF6B6B']
            )
            fig_daily.add_scatter(
                x=df_summary_sorted['Date'],
                y=df_summary_sorted['Goal'],
                mode='lines',
                name='Goal',
                line=dict(color='#4ECDC4', width=3)
            )
            fig_daily.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig_daily, use_container_width=True)
            
            # Macronutrient breakdown
            avg_macros = {
                'Protein': avg_daily_protein * 4,
                'Carbs': avg_daily_carbs * 4,
                'Fat': avg_daily_fat * 9
            }
            
            fig_macros = go.Figure(data=[
                go.Pie(
                    labels=list(avg_macros.keys()),
                    values=list(avg_macros.values()),
                    hole=0.4,
                    marker=dict(colors=['#FF6B6B', '#4ECDC4', '#FFE66D'])
                )
            ])
            fig_macros.update_layout(
                title="Average Daily Macronutrient Breakdown",
                height=400
            )
            st.plotly_chart(fig_macros, use_container_width=True)
            
            # Macronutrient trends
            col1, col2, col3 = st.columns(3)
            
            with col1:
                fig_protein = px.line(
                    df_summary_sorted,
                    x='Date',
                    y='Protein (g)',
                    markers=True,
                    title='Protein Intake',
                    color_discrete_sequence=['#FF6B6B']
                )
                fig_protein.update_layout(height=350)
                st.plotly_chart(fig_protein, use_container_width=True)
            
            with col2:
                fig_carbs = px.line(
                    df_summary_sorted,
                    x='Date',
                    y='Carbs (g)',
                    markers=True,
                    title='Carbohydrates Intake',
                    color_discrete_sequence=['#4ECDC4']
                )
                fig_carbs.update_layout(height=350)
                st.plotly_chart(fig_carbs, use_container_width=True)
            
            with col3:
                fig_fat = px.line(
                    df_summary_sorted,
                    x='Date',
                    y='Fat (g)',
                    markers=True,
                    title='Fat Intake',
                    color_discrete_sequence=['#FFE66D']
                )
                fig_fat.update_layout(height=350)
                st.plotly_chart(fig_fat, use_container_width=True)
        
        with tab4:
            st.subheader("Food Frequency Analysis")
            
            # Count food items
            food_counts = {}
            for log in food_logs:
                log_dict = dict(log)
                food_name = log_dict['food_name']
                if food_name not in food_counts:
                    food_counts[food_name] = {'count': 0, 'calories': 0}
                food_counts[food_name]['count'] += 1
                food_counts[food_name]['calories'] += log_dict['calories'] or 0
            
            # Sort by frequency
            sorted_foods = sorted(food_counts.items(), key=lambda x: x[1]['count'], reverse=True)
            
            # Top foods
            top_n = min(15, len(sorted_foods))
            top_foods = sorted_foods[:top_n]
            
            food_names = [f[0][:20] for f in top_foods]
            food_frequencies = [f[1]['count'] for f in top_foods]
            
            fig_freq = px.bar(
                x=food_frequencies,
                y=food_names,
                orientation='h',
                title=f'Top {top_n} Most Frequently Consumed Foods',
                labels={'x': 'Frequency', 'y': 'Food'},
                color=food_frequencies,
                color_continuous_scale='RdYlGn'
            )
            fig_freq.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_freq, use_container_width=True)
            
            # Top calorie foods
            top_calorie_foods = sorted(sorted_foods, key=lambda x: x[1]['calories'], reverse=True)[:top_n]
            
            food_names_cal = [f[0][:20] for f in top_calorie_foods]
            food_cals = [f[1]['calories'] for f in top_calorie_foods]
            
            fig_cal = px.bar(
                x=food_cals,
                y=food_names_cal,
                orientation='h',
                title=f'Top {top_n} Foods by Total Calories',
                labels={'x': 'Total Calories', 'y': 'Food'},
                color=food_cals,
                color_continuous_scale='YlOrRd'
            )
            fig_cal.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_cal, use_container_width=True)
    
    else:
        st.info("No food entries in this date range. Start logging your meals!")

if __name__ == "__main__":
    if st.session_state.get('logged_in'):
        show_food_history(st.session_state.user_id)
    else:
        st.error("Please login first")
