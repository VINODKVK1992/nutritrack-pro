"""API service for OpenAI integration and nutrition data extraction."""
import os
import json
import base64
from io import BytesIO
from pathlib import Path
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file in project root
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize OpenAI client
def get_openai_client():
    """Get OpenAI client with API key from environment or Streamlit secrets."""
    # Try environment variable first
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Debug: Check if key was loaded
    if api_key:
        print(f"✓ API key loaded from environment (length: {len(api_key)})")
    
    # Fallback to Streamlit secrets if env var not found
    if not api_key:
        try:
            api_key = st.secrets.get("openai_api_key")
            if api_key:
                print("✓ API key loaded from secrets.toml")
        except:
            pass
    
    if not api_key:
        print("✗ No API key found in environment or secrets.toml")
        raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable or add to .streamlit/secrets.toml")
    
    return OpenAI(api_key=api_key)

def extract_food_nutrition(food_description, image_path=None):
    """
    Extract nutritional information from food description or image using OpenAI.
    
    Args:
        food_description: Description of food (e.g., "1 medium apple, 2 slices of bread")
        image_path: Optional path to food image
    
    Returns:
        Dictionary with nutritional data
    """
    try:
        client = get_openai_client()
        
        # Prepare the prompt
        system_prompt = """You are a nutrition expert AI. When given a food description or image, 
        analyze it and provide nutritional information in JSON format.
        
        Return ONLY valid JSON with these fields:
        {
            "food_items": [
                {
                    "name": "food name",
                    "quantity": "amount and unit",
                    "calories": number,
                    "protein_g": number,
                    "carbs_g": number,
                    "fat_g": number,
                    "fiber_g": number
                }
            ],
            "total_calories": number,
            "total_protein_g": number,
            "total_carbs_g": number,
            "total_fat_g": number,
            "total_fiber_g": number,
            "confidence": "high/medium/low",
            "notes": "any relevant notes"
        }
        
        Be accurate with portion sizes and nutritional values. If unsure about exact values,
        provide reasonable estimates based on USDA food database standards."""
        
        user_message = f"Please analyze this food and provide nutritional information: {food_description}"
        
        # If image is provided, encode it
        if image_path and os.path.exists(image_path):
            try:
                with open(image_path, 'rb') as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                
                # Determine image type
                image_type = "jpeg" if image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg') else "png"
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    max_tokens=1024,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/{image_type};base64,{image_data}",
                                    },
                                },
                                {
                                    "type": "text",
                                    "text": f"{system_prompt}\n\n{user_message}"
                                }
                            ],
                        }
                    ],
                )
            except Exception as e:
                # Fallback to text-only if vision fails
                st.warning(f"Image analysis failed, using text description: {str(e)}")
                response = client.chat.completions.create(
                    model="gpt-4",
                    max_tokens=1024,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                )
        else:
            response = client.chat.completions.create(
                model="gpt-4",
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
            )
        
        # Parse response
        response_text = response.choices[0].message.content
        
        # Try to extract JSON from response
        try:
            nutrition_data = json.loads(response_text)
        except json.JSONDecodeError:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                nutrition_data = json.loads(json_match.group())
            else:
                raise ValueError("Could not parse nutrition data from response")
        
        return {
            "success": True,
            "data": nutrition_data
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }

def generate_food_recommendations(user_profile, dietary_preferences, daily_calorie_goal, plan_duration="Single Day", selected_meals=None):
    """
    Generate personalized food recommendations using OpenAI.
    
    Args:
        user_profile: Dictionary with user health data
        dietary_preferences: User's dietary preferences/restrictions
        daily_calorie_goal: Daily calorie target
        plan_duration: Duration of plan ("Single Day", "1 Week", "1 Month")
        selected_meals: List of meals to include (e.g., ["Breakfast", "Lunch", "Dinner"])
    
    Returns:
        Dictionary with meal recommendations
    """
    try:
        client = get_openai_client()
        
        # Determine number of days
        num_days = 1
        if plan_duration == "1 Week":
            num_days = 7
        elif plan_duration == "1 Month":
            num_days = 30
        
        # Build system prompt based on duration
        if num_days == 1:
            system_prompt = """You are a professional nutritionist. Provide personalized meal recommendations.
            Return ONLY valid JSON format. NO explanations, NO markdown, ONLY JSON.
            
            CRITICAL: foods MUST be an array of objects with name, quantity, calories, protein_g, carbs_g, fat_g
            
            Return EXACTLY this structure:
            {
                "meal_plan": [
                    {
                        "day": 1,
                        "day_name": "Day 1",
                        "meal": "breakfast",
                        "time": "08:00",
                        "foods": [
                            {"name": "Oatmeal", "quantity": "1 cup", "calories": 150, "protein_g": 5, "carbs_g": 27, "fat_g": 3}
                        ],
                        "meal_total_calories": 150,
                        "tips": "preparation tips"
                    }
                ],
                "daily_totals": {"calories": 1500, "protein_g": 75, "carbs_g": 150, "fat_g": 50},
                "notes": "general notes"
            }"""
        elif num_days == 7:
            system_prompt = """You are a professional nutritionist. Create a 7-DAY meal plan with DIFFERENT meals for each day.
            Return ONLY valid JSON format. NO explanations, NO markdown, ONLY JSON.
            
            CRITICAL RULES:
            1. Generate meals for ALL 7 DAYS (Monday through Sunday)
            2. Each day must have unique meals
            3. foods MUST be an array of objects with name, quantity, calories, protein_g, carbs_g, fat_g
            4. Do NOT use simple string arrays for foods
            
            Return EXACTLY this structure:
            {
                "meal_plan": [
                    {
                        "day": 1,
                        "day_name": "Monday",
                        "meal": "breakfast",
                        "time": "08:00",
                        "foods": [
                            {"name": "Oatmeal", "quantity": "1 cup", "calories": 150, "protein_g": 5, "carbs_g": 27, "fat_g": 3}
                        ],
                        "meal_total_calories": 150,
                        "tips": "preparation tips"
                    }
                ],
                "daily_totals": {"calories": 1500, "protein_g": 75, "carbs_g": 150, "fat_g": 50},
                "notes": "general notes"
            }"""
        else:  # 30 days
            system_prompt = """You are a professional nutritionist. Create a 30-DAY meal plan.
            Return ONLY valid JSON. Keep it CONCISE - 1-2 foods per meal.
            
            Return EXACTLY this structure:
            {
                "meal_plan": [
                    {
                        "day": 1,
                        "day_name": "Week 1 - Monday",
                        "meal": "breakfast",
                        "time": "08:00",
                        "foods": [
                            {"name": "Oatmeal", "quantity": "1 cup", "calories": 150, "protein_g": 5, "carbs_g": 27, "fat_g": 3}
                        ],
                        "meal_total_calories": 150,
                        "tips": "Quick prep"
                    }
                ],
                "daily_totals": {"calories": 1500, "protein_g": 75, "carbs_g": 150, "fat_g": 50},
                "notes": "Balanced plan"
            }"""
        
        age = user_profile.get('age', 'unknown')
        sex = user_profile.get('sex', 'unknown')
        activity_level = user_profile.get('activity_level', 'moderate')
        bmi = user_profile.get('bmi', 'unknown')
        
        meals_text = ", ".join(selected_meals) if selected_meals else "all meals"
        
        if num_days == 1:
            duration_text = "Provide a balanced meal plan for ONE day."
        elif num_days == 7:
            duration_text = f"""Provide a 7-DAY meal plan (Monday-Sunday).
            IMPORTANT: Keep it concise. Include {meals_text} for each day with 1-2 foods per meal."""
        else:
            duration_text = f"""Provide a 30-DAY meal plan.
            IMPORTANT: Keep it very concise. Include {meals_text} for each day with 1-2 foods per meal."""
        
        user_message = f"""Create a personalized meal plan with these details:
        - Age: {age}
        - Sex: {sex}
        - Activity Level: {activity_level}
        - BMI Category: {bmi}
        - Daily Calorie Goal: {daily_calorie_goal} calories
        - Dietary Preferences: {dietary_preferences}
        - Meals to Include: {meals_text}
        - Goal: Healthy eating aligned with calorie target
        
        {duration_text}"""
        
        # Use higher token limit for longer plans
        max_tokens = 1200 if num_days == 1 else (2000 if num_days == 7 else 3000)
        
        response = client.chat.completions.create(
            model="gpt-4",
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )
        
        response_text = response.choices[0].message.content
        
        # Log the raw response for debugging
        print(f"\n{'='*80}")
        print("AI RESPONSE RECEIVED")
        print(f"{'='*80}")
        print(f"Response length: {len(response_text)} characters")
        print(f"First 500 chars: {response_text[:500]}")
        print(f"{'='*80}\n")
        
        # Clean response text - remove markdown code blocks if present
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        try:
            recommendations = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"JSON PARSE ERROR: {str(e)}")
            print(f"Cleaned response (first 1000 chars): {response_text[:1000]}")
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                try:
                    recommendations = json.loads(json_match.group())
                    print("Successfully extracted JSON using regex")
                except Exception as regex_error:
                    print(f"Regex extraction also failed: {str(regex_error)}")
                    raise ValueError(f"Could not parse JSON. Error at line {e.lineno} col {e.colno}. Try 'Single Day' plan instead of weekly/monthly.")
            else:
                print("No JSON pattern found in response")
                raise ValueError(f"No valid JSON found in AI response. Try 'Single Day' plan or regenerate.")
        
        return {
            "success": True,
            "data": recommendations
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }

def analyze_health_metrics(health_history):
    """
    Analyze health metrics trends and provide insights using OpenAI.
    
    Args:
        health_history: List of health metric dictionaries
    
    Returns:
        Dictionary with analysis and recommendations
    """
    try:
        client = get_openai_client()
        
        system_prompt = """You are a health coach. Analyze the provided health metrics and provide
        insights and actionable recommendations. Return ONLY valid JSON.
        
        Return this structure:
        {
            "trends": ["trend 1", "trend 2", ...],
            "positive_observations": ["observation 1", ...],
            "areas_for_improvement": ["area 1", ...],
            "recommendations": ["recommendation 1", ...],
            "risk_factors": ["risk 1", ...],
            "motivational_message": "personalized motivation"
        }"""
        
        user_message = f"""Please analyze these health metrics and provide insights:
        
        Health Data:
        {json.dumps(health_history, indent=2, default=str)}
        
        Provide constructive analysis and actionable recommendations."""
        
        response = client.chat.completions.create(
            model="gpt-4",
            max_tokens=1500,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
        )
        
        response_text = response.choices[0].message.content
        
        try:
            analysis = json.loads(response_text)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
            else:
                raise ValueError("Could not parse analysis")
        
        return {
            "success": True,
            "data": analysis
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "data": None
        }
