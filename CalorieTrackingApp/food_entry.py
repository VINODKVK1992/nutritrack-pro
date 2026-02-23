"""Food entry page with searchable gallery and multi-item meal support."""
import streamlit as st
import os
from datetime import datetime
from PIL import Image
import pandas as pd
from database import add_food_log, get_user_profile
from api_service import extract_food_nutrition
from CalorieTrackingApp.food_database import search_foods, FOOD_DATABASE, get_common_foods

def show_food_entry(user_id):
    """Show food entry page with manual, gallery, image, and AI options."""
    
    st.title("🍽️ Add Food Entry")
    
    # Show success message if exists
    if 'food_save_msg' in st.session_state:
        st.success(st.session_state['food_save_msg'])
        del st.session_state['food_save_msg']
    
    # Get user profile for calorie goal
    profile = get_user_profile(user_id)
    if profile:
        profile_dict = dict(profile)
        daily_goal = profile_dict['daily_calorie_goal']
    else:
        st.error("Please set up your profile first")
        return
    
    # Initialize session state for meal items
    if 'meal_items' not in st.session_state:
        st.session_state.meal_items = []
    
    # Tabs for different entry methods
    tab1, tab2, tab3, tab4 = st.tabs(["🍔 Food Gallery", "📝 Manual Entry", "📸 Image Upload", "🤖 AI Analysis"])
    
    # ============ TAB 1: FOOD GALLERY WITH SEARCH & MULTI-SELECT ============
    with tab1:
        st.subheader("🍔 Food Gallery - Build Your Meal")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_query = st.text_input(
                "🔍 Search for foods",
                placeholder="Type: chicken, rice, apple, dal...",
                key="food_search"
            )
        with col2:
            show_common = st.checkbox("Show Popular", value=True)
        
        # Get foods to display - search happens automatically as user types
        if search_query and len(search_query) >= 2:  # Start searching after 2 characters
            display_foods = search_foods(search_query)
            st.caption(f"Found {len(display_foods)} foods matching '{search_query}'")
        elif show_common and not search_query:
            display_foods = get_common_foods(limit=16)
            st.caption(f"Showing {len(display_foods)} popular foods")
        else:
            # Show 40 foods from database
            display_foods = FOOD_DATABASE[:40]
            st.caption(f"Showing {len(display_foods)} foods from database")
        
        # Display food grid
        if display_foods:
            cols_per_row = 4
            for i in range(0, len(display_foods), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(display_foods):
                        food = display_foods[i + j]
                        with col:
                            # Create a food card
                            st.markdown(f"""
                            <div style='border: 1px solid #ddd; padding: 10px; border-radius: 8px; text-align: center;'>
                                <div style='font-size: 32px;'>{food['image']}</div>
                                <strong style='font-size: 12px;'>{food['name']}</strong><br>
                                <small>📊 {int(food['calories'])} cal | 🥩 {food['protein']}g</small>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Select button for this food
                            if st.button(f"Add", key=f"food_{i}_{j}", use_container_width=True):
                                # Check if item already exists in meal
                                existing_item = None
                                for meal_item in st.session_state.meal_items:
                                    if meal_item['name'] == food['name']:
                                        existing_item = meal_item
                                        break
                                
                                if existing_item:
                                    # Item already exists - increment quantity
                                    existing_item['quantity'] = existing_item.get('quantity', 1.0) + 1.0
                                    st.toast(f"✅ Updated {food['name']} (now x{existing_item['quantity']})")
                                else:
                                    # New item - add to meal
                                    item = {
                                        'name': food['name'],
                                        'calories': food['calories'],
                                        'protein': food['protein'],
                                        'carbs': food['carbs'],
                                        'fat': food['fat'],
                                        'image': food['image'],
                                        'quantity': 1.0  # Default quantity
                                    }
                                    st.session_state.meal_items.append(item)
                                    st.toast(f"✅ Added {food['name']} to your meal!")
                                st.rerun()
        else:
            st.info("No foods found. Try a different search term.")
        
        st.divider()
        
        # Display meal items being built
        st.subheader("🍽️ Your Meal")
        
        if st.session_state.meal_items:
            meal_df = pd.DataFrame(st.session_state.meal_items)
            
            # Display items with quantity adjustment
            for idx, item in enumerate(st.session_state.meal_items):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"{item['image']} **{item['name']}**")
                
                with col2:
                    quantity = st.number_input(
                        f"Quantity multiplier",
                        min_value=0.1,
                        max_value=10.0,
                        value=item.get('quantity', 1.0),
                        step=0.1,
                        key=f"qty_{idx}",
                        label_visibility="collapsed"
                    )
                    st.session_state.meal_items[idx]['quantity'] = quantity
                
                with col3:
                    if st.button("❌", key=f"remove_{idx}"):
                        st.session_state.meal_items.pop(idx)
                        st.rerun()
            
            st.divider()
            
            # Calculate total nutrition
            total_calories = sum(item['calories'] * item.get('quantity', 1.0) for item in st.session_state.meal_items)
            total_protein = sum(item['protein'] * item.get('quantity', 1.0) for item in st.session_state.meal_items)
            total_carbs = sum(item['carbs'] * item.get('quantity', 1.0) for item in st.session_state.meal_items)
            total_fat = sum(item['fat'] * item.get('quantity', 1.0) for item in st.session_state.meal_items)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Calories", int(total_calories))
            with col2:
                st.metric("🥩 Total Protein", f"{total_protein:.1f}g")
            with col3:
                st.metric("🌾 Total Carbs", f"{total_carbs:.1f}g")
            with col4:
                st.metric("🫒 Total Fat", f"{total_fat:.1f}g")
            
            # Save meal
            col1, col2 = st.columns(2)
            
            with col1:
                meal_type = st.selectbox(
                    "Meal Type",
                    ["Breakfast", "Lunch", "Dinner", "Snack"],
                    key="meal_type_gallery"
                )
            
            with col2:
                entry_date = st.date_input("Date", datetime.now().date(), key="date_gallery")
            
            if st.button("💾 Save Meal", use_container_width=True, type="primary"):
                try:
                    entry_date_str = entry_date.strftime('%Y-%m-%d') if hasattr(entry_date, 'strftime') else str(entry_date)
                    meal_name = f"Meal: {', '.join([item['name'].split('(')[0].strip() for item in st.session_state.meal_items])}"
                    num_items = len(st.session_state.meal_items)
                    
                    result = add_food_log(
                        user_id,
                        meal_name,
                        f"{num_items} items",
                        total_calories,
                        total_protein,
                        total_carbs,
                        total_fat,
                        0,
                        meal_type=meal_type,
                        image_path=None,
                        entry_date=entry_date_str
                    )
                    
                    st.session_state['food_save_msg'] = f"✅ Saved meal with {num_items} items ({int(total_calories)} cal)!"
                    st.session_state.meal_items = []
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving meal: {str(e)}")
                    import traceback
                    st.error(f"Traceback: {traceback.format_exc()}")
            
            if st.button("🔄 Clear Meal", use_container_width=True):
                st.session_state.meal_items = []
                st.rerun()
        else:
            st.info("👆 Select foods from the gallery above to build your meal")
    
    # ============ TAB 2: MANUAL ENTRY ============
    with tab2:
        st.subheader("📝 Manual Food Entry")
        
        col1, col2 = st.columns(2)
        
        with col1:
            food_name = st.text_input("Food Name", placeholder="e.g., Chicken Breast, Apple", key="manual_food_name")
        
        with col2:
            quantity = st.text_input("Quantity", placeholder="e.g., 100g, 1 medium, 2 slices", key="manual_qty")
        
        st.info("💡 **Tip:** You can leave nutrition fields empty and click 'Analyze' to auto-calculate using AI")
        
        use_ai = st.checkbox("🤖 Use AI to calculate nutrition automatically", value=False, key="manual_use_ai")
        
        col1, col2 = st.columns(2)
        
        with col1:
            calories = st.number_input("Calories", min_value=0, max_value=10000, value=0 if use_ai else 100, key="manual_cal")
        
        with col2:
            protein = st.number_input("Protein (g)", min_value=0.0, max_value=500.0, step=0.1, value=0.0 if use_ai else 1.0, key="manual_protein")
        
        col1, col2 = st.columns(2)
        
        with col1:
            carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=500.0, step=0.1, value=0.0 if use_ai else 1.0, key="manual_carbs")
        
        with col2:
            fat = st.number_input("Fat (g)", min_value=0.0, max_value=500.0, step=0.1, value=0.0 if use_ai else 1.0, key="manual_fat")
        
        fiber = st.number_input("Fiber (g)", min_value=0.0, max_value=500.0, step=0.1, value=0.0 if use_ai else 0.0, key="manual_fiber")
        
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"], key="meal_type_manual")
        
        entry_date = st.date_input("Date", datetime.now().date(), key="date_manual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if use_ai and st.button("🤖 Analyze with AI", use_container_width=True, type="secondary"):
                if food_name and quantity:
                    with st.spinner("Analyzing food..."):
                        result = extract_food_nutrition(f"{food_name}, {quantity}")
                        
                        if result['success']:
                            nutrition_data = result['data']
                            st.success("✅ AI analysis complete!")
                            
                            if 'food_items' in nutrition_data and len(nutrition_data['food_items']) > 0:
                                first_item = nutrition_data['food_items'][0]
                                st.info(f"""
                                **AI Analysis Results:**
                                - Calories: {int(nutrition_data.get('total_calories', first_item.get('calories', 0)))}
                                - Protein: {nutrition_data.get('total_protein_g', first_item.get('protein_g', 0))}g
                                - Carbs: {nutrition_data.get('total_carbs_g', first_item.get('carbs_g', 0))}g
                                - Fat: {nutrition_data.get('total_fat_g', first_item.get('fat_g', 0))}g
                                - Fiber: {nutrition_data.get('total_fiber_g', first_item.get('fiber_g', 0))}g
                                """)
                        else:
                            st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
                else:
                    st.warning("Please enter food name and quantity first")
        
        with col2:
            if st.button("✅ Add Food Entry", use_container_width=True, type="primary"):
                if food_name and calories >= 0:
                    try:
                        entry_date_str = entry_date.strftime('%Y-%m-%d') if hasattr(entry_date, 'strftime') else str(entry_date)
                        
                        add_food_log(
                            user_id,
                            food_name,
                            quantity,
                            calories,
                            protein,
                            carbs,
                            fat,
                            fiber,
                            meal_type=meal_type,
                            image_path=None,
                            entry_date=entry_date_str
                        )
                        st.session_state['food_save_msg'] = f"✅ Added {food_name} ({int(calories)} cal)"
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error saving: {str(e)}")
                        import traceback
                        st.error(f"Traceback: {traceback.format_exc()}")
                else:
                    st.error("Please fill in food name and calories")
    
    # ============ TAB 3: IMAGE UPLOAD ============
    with tab3:
        st.subheader("📸 Upload Food Image")
        
        # Initialize session state for image analysis
        if 'image_analysis_data' not in st.session_state:
            st.session_state.image_analysis_data = None
        if 'image_path_saved' not in st.session_state:
            st.session_state.image_path_saved = None
        if 'image_description_saved' not in st.session_state:
            st.session_state.image_description_saved = None
        
        uploaded_file = st.file_uploader(
            "Upload a food image",
            type=['jpg', 'jpeg', 'png', 'webp', 'bmp', 'gif', 'heic'],
            help="Upload a clear image of your food for analysis",
            key="image_upload"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Food Image", use_container_width=True)
            
            image_path = f"temp_{user_id}_{datetime.now().timestamp()}.jpg"
            image.save(image_path)
            
            food_description = st.text_area(
                "Describe the food (optional, helps with accuracy)",
                placeholder="e.g., 'grilled chicken with rice and broccoli'",
                key="image_desc"
            )
            
            if st.button("🤖 Analyze Image with AI", use_container_width=True, type="primary"):
                with st.spinner("Analyzing food image..."):
                    try:
                        result = extract_food_nutrition(
                            food_description or "Please analyze this food image",
                            image_path
                        )
                        
                        if result['success']:
                            # Store in session state
                            st.session_state.image_analysis_data = result['data']
                            st.session_state.image_path_saved = image_path
                            st.session_state.image_description_saved = food_description
                            st.success("✅ Food analysis complete!")
                            st.rerun()
                        else:
                            st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error analyzing image: {str(e)}")
        
        # Display analysis results if available
        if st.session_state.image_analysis_data:
            nutrition_data = st.session_state.image_analysis_data
            
            st.subheader("Food Analysis Results")
            
            if 'food_items' in nutrition_data:
                for item in nutrition_data['food_items']:
                    st.write(f"**{item['name']}** - {item['quantity']}")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Calories", int(item['calories']))
                    with col2:
                        st.metric("Protein", f"{item['protein_g']}g")
                    with col3:
                        st.metric("Carbs", f"{item['carbs_g']}g")
                    with col4:
                        st.metric("Fat", f"{item['fat_g']}g")
            
            st.divider()
            st.subheader("Total Nutrition")
            
            total_calories = nutrition_data.get('total_calories', 0)
            total_protein = nutrition_data.get('total_protein_g', 0)
            total_carbs = nutrition_data.get('total_carbs_g', 0)
            total_fat = nutrition_data.get('total_fat_g', 0)
            total_fiber = nutrition_data.get('total_fiber_g', 0)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Calories", int(total_calories))
            with col2:
                st.metric("Protein", f"{total_protein}g")
            with col3:
                st.metric("Carbs", f"{total_carbs}g")
            with col4:
                st.metric("Fat", f"{total_fat}g")
            with col5:
                st.metric("Fiber", f"{total_fiber}g")
            
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"], key="meal_type_image")
            entry_date = st.date_input("Date", datetime.now().date(), key="date_image")
            
            if st.button("💾 Save Food Entry", use_container_width=True, type="primary", key="save_image_entry"):
                try:
                    entry_date_str = entry_date.strftime('%Y-%m-%d') if hasattr(entry_date, 'strftime') else str(entry_date)
                    food_name = st.session_state.image_description_saved or "Image analyzed food"
                    
                    add_food_log(
                        user_id,
                        food_name,
                        "As analyzed",
                        total_calories,
                        total_protein,
                        total_carbs,
                        total_fat,
                        total_fiber,
                        meal_type=meal_type,
                        image_path=st.session_state.image_path_saved,
                        entry_date=entry_date_str
                    )
                    
                    st.session_state.image_analysis_data = None
                    st.session_state.image_path_saved = None
                    st.session_state.image_description_saved = None
                    st.session_state['food_save_msg'] = "✅ Food entry saved!"
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving: {str(e)}")
                    import traceback
                    st.error(f"Traceback: {traceback.format_exc()}")
    
    # ============ TAB 4: AI TEXT ANALYSIS ============
    with tab4:
        st.subheader("🤖 AI Food Analysis")
        
        # Initialize session state for AI analysis
        if 'ai_analysis_data' not in st.session_state:
            st.session_state.ai_analysis_data = None
        if 'ai_food_input_saved' not in st.session_state:
            st.session_state.ai_food_input_saved = None
        
        food_input = st.text_area(
            "Describe your meal in detail",
            placeholder="e.g., I had grilled chicken breast (150g), basmati rice (150g cooked), and steamed broccoli with olive oil",
            height=120,
            key="ai_analysis_input"
        )
        
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"], key="meal_type_ai")
        entry_date = st.date_input("Date", datetime.now().date(), key="date_ai")
        
        if st.button("🤖 Analyze with AI", use_container_width=True, type="primary", key="analyze_ai_text"):
            if food_input:
                with st.spinner("Analyzing your meal description..."):
                    try:
                        result = extract_food_nutrition(food_input)
                        
                        if result['success']:
                            # Store in session state
                            st.session_state.ai_analysis_data = result['data']
                            st.session_state.ai_food_input_saved = food_input
                            st.success("✅ Analysis complete!")
                            st.rerun()
                        else:
                            st.error(f"Analysis failed: {result.get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error analyzing: {str(e)}")
            else:
                st.warning("Please describe your meal first")
        
        # Display analysis results if available
        if st.session_state.ai_analysis_data:
            nutrition_data = st.session_state.ai_analysis_data
            
            st.subheader("Food Items Detected")
            
            if 'food_items' in nutrition_data:
                for item in nutrition_data['food_items']:
                    st.write(f"✓ **{item['name']}** - {item['quantity']}")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Cal", int(item['calories']))
                    with col2:
                        st.metric("Protein", f"{item['protein_g']}g")
                    with col3:
                        st.metric("Carbs", f"{item['carbs_g']}g")
                    with col4:
                        st.metric("Fat", f"{item['fat_g']}g")
            
            st.divider()
            st.subheader("Total Nutrition")
            
            total_calories = nutrition_data.get('total_calories', 0)
            total_protein = nutrition_data.get('total_protein_g', 0)
            total_carbs = nutrition_data.get('total_carbs_g', 0)
            total_fat = nutrition_data.get('total_fat_g', 0)
            total_fiber = nutrition_data.get('total_fiber_g', 0)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Calories", int(total_calories))
            with col2:
                st.metric("Protein", f"{total_protein}g")
            with col3:
                st.metric("Carbs", f"{total_carbs}g")
            with col4:
                st.metric("Fat", f"{total_fat}g")
            with col5:
                st.metric("Fiber", f"{total_fiber}g")
            
            if st.button("💾 Save Meal", use_container_width=True, type="primary", key="save_ai_meal"):
                try:
                    entry_date_str = entry_date.strftime('%Y-%m-%d') if hasattr(entry_date, 'strftime') else str(entry_date)
                    meal_description = st.session_state.ai_food_input_saved[:50] + "..." if len(st.session_state.ai_food_input_saved) > 50 else st.session_state.ai_food_input_saved
                    
                    add_food_log(
                        user_id,
                        meal_description,
                        "AI Analyzed",
                        total_calories,
                        total_protein,
                        total_carbs,
                        total_fat,
                        total_fiber,
                        meal_type=meal_type,
                        image_path=None,
                        entry_date=entry_date_str
                    )
                    
                    st.session_state.ai_analysis_data = None
                    st.session_state.ai_food_input_saved = None
                    st.session_state['food_save_msg'] = "✅ Meal saved successfully!"
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error saving: {str(e)}")
                    import traceback
                    st.error(f"Traceback: {traceback.format_exc()}")


if __name__ == "__main__":
    if st.session_state.get('logged_in'):
        show_food_entry(st.session_state.user_id)
    else:
        st.error("Please login first")
