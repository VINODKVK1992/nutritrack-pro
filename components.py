"""UI components for header, footer, and styling."""
import streamlit as st

def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown("""
    <style>
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Footer styling */
    .main-footer {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-top: 3rem;
        color: white;
        text-align: center;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    
    .footer-links a {
        color: white;
        text-decoration: none;
        font-weight: 500;
        transition: opacity 0.3s;
    }
    
    .footer-links a:hover {
        opacity: 0.7;
    }
    
    /* Card styling */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    """Display professional header."""
    st.markdown("""
    <div class="main-header">
        <h1>🥗 NutriTrack Pro</h1>
        <p>Your Personal AI-Powered Nutrition & Health Companion</p>
    </div>
    """, unsafe_allow_html=True)

def show_footer(show_back_to_login=False):
    """Display professional footer."""
    if show_back_to_login:
        if st.button("🔙 Back to Login", type="primary"):
            st.session_state.footer_nav = None
            st.rerun()
        st.divider()
    
    st.markdown("""
    <div class="main-footer">
        <p style="margin-top: 1rem; opacity: 0.9;">
            © 2026 NutriTrack Pro. All rights reserved.<br>
            Powered by AI • Built with ❤️ for Better Health
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center; margin-top: 1rem;'>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("📖 About Us", use_container_width=True):
            st.session_state.footer_nav = "About"
            st.rerun()
    with col2:
        if st.button("✨ Features", use_container_width=True):
            st.session_state.footer_nav = "Features"
            st.rerun()
    with col3:
        if st.button("📞 Contact", use_container_width=True):
            st.session_state.footer_nav = "Contact"
            st.rerun()
    with col4:
        if st.button("🔒 Privacy", use_container_width=True):
            st.session_state.footer_nav = "Privacy"
            st.rerun()
    with col5:
        if st.button("📜 Terms", use_container_width=True):
            st.session_state.footer_nav = "Terms"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def show_about_page():
    """Display About Us page."""
    st.markdown("""
    <div class="main-header">
        <h1>📖 About NutriTrack Pro</h1>
        <p>Empowering Your Health Journey with AI Technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### 🎯 Our Mission
        
        At NutriTrack Pro, we believe that everyone deserves access to personalized nutrition guidance. 
        Our mission is to make healthy eating simple, accessible, and enjoyable through cutting-edge 
        AI technology.
        
        ### 💡 What We Do
        
        We combine artificial intelligence with nutritional science to provide:
        - **Personalized Meal Plans** tailored to your goals
        - **Smart Food Tracking** with AI-powered analysis
        - **Health Insights** based on your data
        - **Expert Recommendations** for better nutrition
        """)
    
    with col2:
        st.markdown("""
        ### 🌟 Why Choose Us?
        
        **AI-Powered Intelligence**  
        Advanced algorithms analyze your nutrition and provide personalized recommendations.
        
        **Easy to Use**  
        Track food with photos, text, or our extensive database - it's that simple!
        
        **Comprehensive Tracking**  
        Monitor calories, macros, health metrics, and progress all in one place.
        
        **Privacy First**  
        Your data is secure and private. We never share your information.
        """)
    
    st.divider()
    
    st.markdown("""
    ### 👥 Our Team
    
    We're a passionate team of nutritionists, data scientists, and developers dedicated to 
    revolutionizing how people approach their health and nutrition.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **🔬 Nutrition Experts**  
        Certified nutritionists ensuring accuracy
        """)
    
    with col2:
        st.info("""
        **💻 Tech Innovators**  
        AI engineers building smart solutions
        """)
    
    with col3:
        st.info("""
        **🎨 UX Designers**  
        Creating intuitive experiences
        """)

def show_contact_page():
    """Display Contact Us page."""
    st.markdown("""
    <div class="main-header">
        <h1>📞 Contact Us</h1>
        <p>We'd Love to Hear From You!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### 📧 Get in Touch
        
        Have questions, feedback, or need support? We're here to help!
        
        **Contact Person:** Santhi  
        **Email:** santhi@nutritrackpro.com  
        **Phone:** +1 (314) 555-0123  
        **Hours:** Monday - Friday, 9 AM - 6 PM CST
        
        ### 🌐 Connect With Us
        
        **Twitter:** @NutriTrackPro  
        **Instagram:** @nutritrackpro  
        **LinkedIn:** NutriTrack Pro  
        **Facebook:** /NutriTrackPro
        
        ### 📍 Office Location
        
        NutriTrack Pro  
        Maryland Heights  
        Saint Louis, MO 63043  
        United States
        """)
    
    with col2:
        st.markdown("### 💬 Send Us a Message")
        
        with st.form("contact_form"):
            name = st.text_input("Your Name *")
            email = st.text_input("Your Email *")
            subject = st.selectbox("Subject", [
                "General Inquiry",
                "Technical Support",
                "Feature Request",
                "Bug Report",
                "Partnership Opportunity",
                "Other"
            ])
            message = st.text_area("Your Message *", height=150)
            
            submitted = st.form_submit_button("📤 Send Message", use_container_width=True, type="primary")
            
            if submitted:
                if name and email and message:
                    st.success("✅ Thank you! Your message has been sent. We'll get back to you within 24 hours.")
                else:
                    st.error("❌ Please fill in all required fields.")
    
    st.divider()
    
    st.markdown("""
    ### ❓ Frequently Asked Questions
    """)
    
    with st.expander("How do I get started?"):
        st.write("Simply create an account, set up your profile with your health goals, and start tracking your meals!")
    
    with st.expander("Is my data secure?"):
        st.write("Yes! We use industry-standard encryption and never share your personal data with third parties.")
    
    with st.expander("Can I cancel my subscription anytime?"):
        st.write("Absolutely! You can cancel your subscription at any time from your account settings.")
    
    with st.expander("Do you offer a mobile app?"):
        st.write("We're currently working on mobile apps for iOS and Android. Stay tuned for updates!")

def show_features_page():
    """Display Features page."""
    st.markdown("""
    <div class="main-header">
        <h1>✨ Features</h1>
        <p>Everything You Need for Your Health Journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🍽️ Smart Food Tracking
        
        **Multiple Entry Methods**
        - 📸 Upload food photos for instant analysis
        - 🤖 Describe meals in natural language
        - 📝 Manual entry with our extensive database
        - 🔍 Search 10,000+ foods instantly
        
        **AI-Powered Analysis**
        - Automatic nutrition calculation
        - Portion size estimation
        - Meal composition breakdown
        """)
        
        st.markdown("""
        ### 📊 Comprehensive Analytics
        
        **Track Everything**
        - Daily calorie intake vs goals
        - Macronutrient distribution
        - Weekly and monthly trends
        - Food frequency analysis
        
        **Visual Insights**
        - Interactive charts and graphs
        - Progress tracking over time
        - Export data as CSV/Excel
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 AI Meal Planning
        
        **Personalized Plans**
        - Single day, weekly, or monthly plans
        - Customized to your dietary preferences
        - Considers allergies and restrictions
        - Adapts to your fitness goals
        
        **Smart Recommendations**
        - Balanced nutrition suggestions
        - Recipe ideas and cooking tips
        - Meal timing optimization
        """)
        
        st.markdown("""
        ### 💪 Health Metrics
        
        **Complete Health Tracking**
        - Weight and BMI monitoring
        - Sleep hours tracking
        - Water intake logging
        - Exercise minutes recording
        
        **Health Insights**
        - BMR and TDEE calculations
        - Ideal weight recommendations
        - Progress visualization
        """)
    
    st.divider()
    
    st.markdown("### 🎯 Goal-Based Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.success("""
        **Weight Loss**
        - Calorie deficit planning
        - Progress tracking
        - Motivation tips
        """)
    
    with col2:
        st.info("""
        **Muscle Gain**
        - High protein meal plans
        - Calorie surplus guidance
        - Workout integration
        """)
    
    with col3:
        st.warning("""
        **Maintenance**
        - Balanced nutrition
        - Sustainable habits
        - Long-term health
        """)
