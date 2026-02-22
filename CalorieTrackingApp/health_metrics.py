"""Health metrics tracking page."""
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from database import add_health_metric, get_health_metrics, get_user_profile
from health_calculations import calculate_bmi, get_bmi_category, calculate_water_intake

def show_health_metrics(user_id):
    """Show health metrics tracking page."""
    
    st.title("💪 Health Metrics")
    
    # Get user profile
    profile = get_user_profile(user_id)
    if not profile:
        st.error("Please set up your profile first")
        return
    
    profile_dict = dict(profile)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Add Metrics", "📈 Trends", "📋 History"])
    
    with tab1:
        st.subheader("Log Today's Metrics")
        
        today = datetime.now().date()
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input(
                "Weight (kg)",
                min_value=30.0,
                max_value=200.0,
                value=float(profile_dict['weight']),
                step=0.1
            )
        
        with col2:
            bmi = calculate_bmi(weight, profile_dict['height'])
            bmi_category = get_bmi_category(bmi)
            st.metric("Calculated BMI", f"{bmi}", bmi_category)
        
        st.divider()
        
        st.subheader("Daily Activities")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            water_intake = st.number_input(
                "Water Intake (liters)",
                min_value=0.0,
                max_value=20.0,
                value=calculate_water_intake(weight),
                step=0.1,
                help="Daily water intake recommendation"
            )
        
        with col2:
            sleep_hours = st.number_input(
                "Sleep (hours)",
                min_value=0.0,
                max_value=24.0,
                value=7.0,
                step=0.5
            )
        
        with col3:
            exercise_minutes = st.number_input(
                "Exercise (minutes)",
                min_value=0.0,
                max_value=1440.0,
                value=30.0,
                step=5.0
            )
        
        st.divider()
        
        notes = st.text_area(
            "Notes (optional)",
            placeholder="How are you feeling today? Any observations?",
            height=100
        )
        
        metric_date = st.date_input("Date", today)
        
        if st.button("💾 Save Metrics", use_container_width=True, type="primary"):
            try:
                add_health_metric(
                    user_id,
                    metric_date,
                    weight,
                    bmi,
                    water_intake,
                    sleep_hours,
                    exercise_minutes,
                    notes
                )
                st.success("✅ Health metrics saved!")
                st.balloons()
            except Exception as e:
                st.error(f"Error saving metrics: {str(e)}")
    
    with tab2:
        st.subheader("Health Trends")
        
        # Date range selection
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("From", today - timedelta(days=30))
        
        with col2:
            end_date = st.date_input("To", today)
        
        if start_date <= end_date:
            # Get metrics for date range
            metrics = get_health_metrics(user_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            
            if metrics:
                # Convert to dataframe
                metrics_data = []
                for metric in metrics:
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
                
                # Sort by date
                df_metrics['Date'] = pd.to_datetime(df_metrics['Date'])
                df_metrics = df_metrics.sort_values('Date')
                
                # Key stats
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    weight_change = df_metrics['Weight'].iloc[-1] - df_metrics['Weight'].iloc[0]
                    st.metric("Weight Change", f"{weight_change:.1f} kg", delta=f"{weight_change:.1f}")
                
                with col2:
                    avg_bmi = df_metrics['BMI'].mean()
                    st.metric("Avg BMI", f"{avg_bmi:.1f}")
                
                with col3:
                    avg_sleep = df_metrics['Sleep (hrs)'].mean()
                    st.metric("Avg Sleep", f"{avg_sleep:.1f} hrs")
                
                with col4:
                    total_exercise = df_metrics['Exercise (min)'].sum()
                    st.metric("Total Exercise", f"{int(total_exercise)} min")
                
                st.divider()
                
                # Weight trend chart
                fig_weight = px.line(
                    df_metrics,
                    x='Date',
                    y='Weight',
                    markers=True,
                    title='Weight Trend',
                    color_discrete_sequence=['#FF6B6B'],
                    labels={'Weight': 'Weight (kg)'}
                )
                fig_weight.update_layout(height=400, hovermode='x unified')
                st.plotly_chart(fig_weight, use_container_width=True)
                
                # BMI trend chart
                fig_bmi = px.line(
                    df_metrics,
                    x='Date',
                    y='BMI',
                    markers=True,
                    title='BMI Trend',
                    color_discrete_sequence=['#4ECDC4']
                )
                fig_bmi.update_layout(height=400, hovermode='x unified')
                st.plotly_chart(fig_bmi, use_container_width=True)
                
                # Sleep and exercise charts
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_sleep = px.bar(
                        df_metrics,
                        x='Date',
                        y='Sleep (hrs)',
                        title='Sleep Hours',
                        color_discrete_sequence=['#FFE66D'],
                        labels={'Sleep (hrs)': 'Hours'}
                    )
                    fig_sleep.update_layout(height=350)
                    st.plotly_chart(fig_sleep, use_container_width=True)
                
                with col2:
                    fig_exercise = px.bar(
                        df_metrics,
                        x='Date',
                        y='Exercise (min)',
                        title='Exercise Minutes',
                        color_discrete_sequence=['#95E1D3'],
                        labels={'Exercise (min)': 'Minutes'}
                    )
                    fig_exercise.update_layout(height=350)
                    st.plotly_chart(fig_exercise, use_container_width=True)
                
                # Water intake chart
                fig_water = px.line(
                    df_metrics,
                    x='Date',
                    y='Water (L)',
                    markers=True,
                    title='Water Intake',
                    color_discrete_sequence=['#87CEEB']
                )
                fig_water.update_layout(height=350)
                st.plotly_chart(fig_water, use_container_width=True)
            
            else:
                st.info("No metrics recorded in this date range. Start logging your metrics!")
        
        else:
            st.error("End date must be after start date")
    
    with tab3:
        st.subheader("Metrics History")
        
        # Get all metrics
        start_date = (today - timedelta(days=90)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
        
        metrics = get_health_metrics(user_id, start_date, end_date)
        
        if metrics:
            # Convert to dataframe
            metrics_data = []
            for metric in metrics:
                metric_dict = dict(metric)
                metrics_data.append({
                    'Date': metric_dict['date'],
                    'Weight (kg)': metric_dict['weight'],
                    'BMI': metric_dict['bmi'],
                    'BMI Status': get_bmi_category(metric_dict['bmi']),
                    'Sleep (hrs)': metric_dict['sleep_hours'],
                    'Water (L)': metric_dict['water_intake_liters'],
                    'Exercise (min)': metric_dict['exercise_minutes'],
                    'Notes': metric_dict['notes'] or '-'
                })
            
            df_history = pd.DataFrame(metrics_data)
            df_history['Date'] = pd.to_datetime(df_history['Date'])
            df_history = df_history.sort_values('Date', ascending=False)
            
            # Display with pagination
            st.dataframe(df_history, use_container_width=True, hide_index=True)
            
            # Download option
            csv = df_history.to_csv(index=False)
            st.download_button(
                "📥 Download as CSV",
                csv,
                file_name=f"health_metrics_{today}.csv",
                mime="text/csv"
            )
        
        else:
            st.info("No metrics recorded yet. Start tracking your health!")

if __name__ == "__main__":
    if st.session_state.get('logged_in'):
        show_health_metrics(st.session_state.user_id)
    else:
        st.error("Please login first")
