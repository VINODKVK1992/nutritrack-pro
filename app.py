"""Main Streamlit Application - Calorie Tracking System"""
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

import streamlit as st
from datetime import datetime
from auth import init_session_state, login_user, register_user
from database import init_db
from components import apply_custom_css, show_header, show_footer, show_about_page, show_contact_page, show_features_page
from CalorieTrackingApp.home import show_home_dashboard
from CalorieTrackingApp.profile import show_profile_setup
from CalorieTrackingApp.food_entry import show_food_entry
from CalorieTrackingApp.health_metrics import show_health_metrics
from CalorieTrackingApp.food_recommendations import show_food_recommendations
from CalorieTrackingApp.food_history import show_food_history

# Page configuration
st.set_page_config(
    page_title="🥗 NutriTrack Pro",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 50px;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize
init_db()
init_session_state()

def show_login_page():
    """Show login/register page."""
    show_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        
        # Tabs for login and register
        tab1, tab2 = st.tabs(["🔓 Login", "📝 Register"])
        
        with tab1:
            st.subheader("Login to Your Account")
            
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            if st.button("Login", use_container_width=True, type="primary"):
                if username and password:
                    success, message, user = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user[0]
                        st.session_state.username = user[1]
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter username and password")
        
        with tab2:
            st.subheader("Create a New Account")
            
            new_username = st.text_input("Choose a username", key="register_username")
            new_email = st.text_input("Email address", key="register_email")
            
            st.info("🔒 **Password Requirements:**\n"
                   "- At least 8 characters\n"
                   "- One uppercase letter (A-Z)\n"
                   "- One lowercase letter (a-z)\n"
                   "- One number (0-9)\n"
                   "- One special character (!@#$%^&*)")
            
            new_password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm password", type="password", key="confirm_password")
            
            if st.button("Register", use_container_width=True, type="primary"):
                if new_username and new_email and new_password:
                    success, message, user_id = register_user(new_username, new_email, new_password, confirm_password)
                    if success:
                        st.success(message + " Redirecting to login...")
                        st.balloons()
                        import time
                        time.sleep(5)
                        # Clear form fields
                        for key in ['register_username', 'register_email', 'register_password', 'confirm_password']:
                            if key in st.session_state:
                                del st.session_state[key]
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please fill all fields")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("✅ AI-Powered Analysis")
        with col2:
            st.info("📊 Smart Tracking")
        with col3:
            st.warning("🎯 Personalized Plans")
    
    show_footer()

def show_main_app():
    """Show main application after login."""
    
    # Sidebar
    with st.sidebar:
        st.title(f"👋 Welcome, {st.session_state.username}!")
        st.divider()
        
        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Home", "👤 Profile", "🍽️ Food Entry", "💪 Health Metrics", 
             "🍎 Recommendations", "📚 History", "⚙️ Settings"]
        )
        
        st.divider()
        
        # Quick stats
        st.subheader("📊 Quick Stats")
        
        from database import get_user_profile, get_food_log_by_date
        from datetime import datetime
        
        profile = get_user_profile(st.session_state.user_id)
        if profile:
            profile_dict = dict(profile)
            st.metric("Daily Goal", f"{int(profile_dict['daily_calorie_goal'])} cal")
            
            today = datetime.now().date()
            food_log = get_food_log_by_date(st.session_state.user_id, today)
            if food_log:
                total_calories = sum(log['calories'] or 0 for log in food_log)
                remaining = profile_dict['daily_calorie_goal'] - total_calories
                st.metric("Today's Total", f"{int(total_calories)} cal")
                st.metric("Remaining", f"{int(remaining)} cal")
            else:
                st.metric("Today's Total", "0 cal")
                st.metric("Remaining", f"{int(profile_dict['daily_calorie_goal'])} cal")
        
        st.divider()
        
        # Change Password option
        if st.button("🔐 Change Password", use_container_width=True):
            st.session_state.show_password_change = not st.session_state.get('show_password_change', False)
            st.rerun()
        
        # Password change form
        if st.session_state.get('show_password_change', False):
            with st.container():
                st.markdown("---")
                st.subheader("Change Your Password")
                
                from auth import hash_password, verify_password
                from database import get_user_by_id, update_user_password
                
                col1, col2 = st.columns(2)
                
                with col1:
                    current_pwd = st.text_input("Current Password", type="password", key="current_pwd_sidebar")
                with col2:
                    st.write("")  # Spacer
                
                new_pwd = st.text_input("New Password", type="password", key="new_pwd_sidebar")
                confirm_pwd = st.text_input("Confirm New Password", type="password", key="confirm_pwd_sidebar")
                
                if st.button("✅ Update Password", use_container_width=True, key="update_pwd_sidebar"):
                    if not current_pwd:
                        st.error("Please enter current password")
                    elif not new_pwd:
                        st.error("Please enter new password")
                    elif len(new_pwd) < 6:
                        st.error("New password must be at least 6 characters")
                    elif new_pwd != confirm_pwd:
                        st.error("Passwords do not match")
                    else:
                        user = get_user_by_id(st.session_state.user_id)
                        if user and verify_password(current_pwd, user[2]):
                            new_password_hash = hash_password(new_pwd)
                            if update_user_password(st.session_state.user_id, new_password_hash):
                                st.success("✅ Password updated successfully!")
                                st.session_state.show_password_change = False
                                st.rerun()
                            else:
                                st.error("Failed to update password")
                        else:
                            st.error("Current password is incorrect")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.rerun()
    
    # Main content
    if page == "🏠 Home":
        show_home_dashboard(st.session_state.user_id)
    
    elif page == "👤 Profile":
        show_profile_setup(st.session_state.user_id)
    
    elif page == "🍽️ Food Entry":
        show_food_entry(st.session_state.user_id)
    
    elif page == "💪 Health Metrics":
        show_health_metrics(st.session_state.user_id)
    
    elif page == "🍎 Recommendations":
        show_food_recommendations(st.session_state.user_id)
    
    elif page == "📚 History":
        show_food_history(st.session_state.user_id)
    
    elif page == "⚙️ Settings":
        st.title("⚙️ Settings")
        
        st.subheader("Account Settings")
        
        from database import get_user_by_id
        user = get_user_by_id(st.session_state.user_id)
        user_dict = dict(user)
        
        st.info(f"""
        **Username:** {user_dict['username']}
        **Email:** {user_dict['email']}
        **Member Since:** {user_dict['created_at'][:10]}
        """)
        
        st.divider()
        
        st.subheader("About This App")
        st.markdown("""
        ### 🥗 Calorie Tracker v1.0
        
        A comprehensive health and nutrition tracking application powered by AI.
        
        **Features:**
        - 🔐 Secure user authentication
        - 📊 Advanced analytics and visualizations
        - 🤖 AI-powered food recognition
        - 🍽️ Personalized meal plans
        - 💪 Health metrics tracking
        - 📈 Progress monitoring
        
        **Technologies Used:**
        - Streamlit for UI
        - SQLite for database
        - OpenAI GPT-4 for AI analysis
        - Plotly for visualizations
        
        **Developer:** Your Name
        **Version:** 1.0
        **Last Updated:** February 2026
        
        Made with ❤️ for better health tracking
        """)

# Main app logic
if st.session_state.logged_in:
    show_main_app()
else:
    # Check for footer navigation on login page
    if st.session_state.get('footer_nav'):
        page = st.session_state.footer_nav
        
        if page == "About":
            show_about_page()
            show_footer(show_back_to_login=True)
        elif page == "Features":
            show_features_page()
            show_footer(show_back_to_login=True)
        elif page == "Contact":
            show_contact_page()
            show_footer(show_back_to_login=True)
        elif page == "Privacy":
            st.markdown("""
            <div class="main-header">
                <h1>🔒 Privacy Policy</h1>
                <p>Your Privacy Matters to Us</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### Information We Collect
            
            We collect information you provide directly to us, including:
            - Account information (username, email, password)
            - Health metrics (weight, height, age, activity level)
            - Food intake and nutrition data
            - Usage data and preferences
            
            ### How We Use Your Information
            
            - To provide and improve our services
            - To personalize your experience
            - To generate AI-powered recommendations
            - To communicate with you about updates
            
            ### Data Security
            
            We implement industry-standard security measures to protect your data:
            - Encrypted data transmission
            - Secure password hashing
            - Regular security audits
            - Limited access controls
            
            ### Your Rights
            
            You have the right to:
            - Access your personal data
            - Request data deletion
            - Export your data
            - Opt-out of communications
            
            ### Contact Us
            
            For privacy concerns, contact: privacy@nutritrackpro.com
            
            Last Updated: February 2026
            """)
            show_footer(show_back_to_login=True)
        elif page == "Terms":
            st.markdown("""
            <div class="main-header">
                <h1>📜 Terms of Service</h1>
                <p>Terms and Conditions</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### Acceptance of Terms
            
            By accessing and using NutriTrack Pro, you accept and agree to be bound by these Terms of Service.
            
            ### Use of Service
            
            You agree to:
            - Provide accurate information
            - Keep your account secure
            - Use the service lawfully
            - Not share your account credentials
            
            ### Medical Disclaimer
            
            NutriTrack Pro is not a substitute for professional medical advice. Always consult with healthcare professionals before making significant dietary changes.
            
            ### Intellectual Property
            
            All content, features, and functionality are owned by NutriTrack Pro and protected by copyright laws.
            
            ### Limitation of Liability
            
            NutriTrack Pro is provided "as is" without warranties. We are not liable for any damages arising from use of the service.
            
            ### Changes to Terms
            
            We reserve the right to modify these terms at any time. Continued use constitutes acceptance of changes.
            
            ### Contact
            
            For questions about these terms, contact: legal@nutritrackpro.com
            
            Last Updated: February 2026
            """)
            show_footer(show_back_to_login=True)
    else:
        show_login_page()
