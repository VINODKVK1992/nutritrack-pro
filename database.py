import sqlite3
import os
from datetime import datetime
import json

DB_PATH = "data/calorie_tracker.db"

def init_db():
    """Initialize SQLite database with required tables."""
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # User profiles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            dob DATE,
            age INTEGER,
            sex TEXT,
            height REAL,
            weight REAL,
            activity_level TEXT,
            dietary_preference TEXT,
            health_conditions TEXT,
            daily_calorie_goal REAL,
            bmr REAL,
            tdee REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Food log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            food_name TEXT NOT NULL,
            quantity TEXT,
            calories REAL,
            protein REAL,
            carbs REAL,
            fat REAL,
            fiber REAL,
            meal_type TEXT DEFAULT 'Snack',
            image_path TEXT,
            entry_date DATE,
            entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Check if meal_type column exists in existing table, add if missing
    cursor.execute("PRAGMA table_info(food_log)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'meal_type' not in columns:
        try:
            cursor.execute("ALTER TABLE food_log ADD COLUMN meal_type TEXT DEFAULT 'Snack'")
            print("Added meal_type column to food_log table")
        except Exception as e:
            print(f"Note: {e}")
    
    # Health metrics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE,
            weight REAL,
            bmi REAL,
            water_intake_liters REAL,
            sleep_hours REAL,
            exercise_minutes INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Food recommendations/meal plans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plan_name TEXT,
            plan_type TEXT,
            meals_data TEXT,
            total_calories REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_user(username, password, email):
    """Create a new user."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, password, email)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None

def get_user(username):
    """Get user by username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Get user by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def update_user_password(user_id, new_password):
    """Update user password."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (new_password, user_id)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False

def create_user_profile(user_id, age, sex, height, weight, activity_level, dietary_preference, health_conditions, daily_calorie_goal, bmr, tdee, dob=None):
    """Create user profile."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_profiles 
        (user_id, dob, age, sex, height, weight, activity_level, dietary_preference, health_conditions, daily_calorie_goal, bmr, tdee)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, dob, age, sex, height, weight, activity_level, dietary_preference, health_conditions, daily_calorie_goal, bmr, tdee))
    conn.commit()
    conn.close()

def get_user_profile(user_id):
    """Get user profile."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def update_user_profile(user_id, **kwargs):
    """Update user profile."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    update_fields = []
    values = []
    for key, value in kwargs.items():
        update_fields.append(f"{key} = ?")
        values.append(value)
    
    values.append(user_id)
    update_fields.append("updated_at = CURRENT_TIMESTAMP")
    
    query = f"UPDATE user_profiles SET {', '.join(update_fields)} WHERE user_id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def add_food_log(user_id, food_name, quantity, calories, protein, carbs, fat, fiber, meal_type='Snack', image_path=None, entry_date=None):
    """Add food to log."""
    try:
        if entry_date is None:
            entry_date = datetime.now().date()
        elif isinstance(entry_date, str):
            try:
                entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
            except Exception as date_err:
                print(f"ERROR converting date {entry_date}: {date_err}")
                entry_date = datetime.now().date()
        
        print(f"DEBUG: Inserting food_log - user_id={user_id}, food_name={food_name}, calories={calories}, entry_date={entry_date}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO food_log 
            (user_id, food_name, quantity, calories, protein, carbs, fat, fiber, meal_type, image_path, entry_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, food_name, quantity, calories, protein, carbs, fat, fiber, meal_type, image_path, entry_date))
        conn.commit()
        
        print(f"SUCCESS: Food log inserted with row id {cursor.lastrowid}")
        conn.close()
        return True
    except Exception as e:
        print(f"ERROR in add_food_log: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise

def get_food_log_by_date(user_id, date):
    """Get food log for a specific date."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM food_log WHERE user_id = ? AND entry_date = ? ORDER BY entry_time DESC",
        (user_id, date)
    )
    logs = cursor.fetchall()
    conn.close()
    return logs

def delete_food_log(log_id):
    """Delete a food log entry."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM food_log WHERE id = ?", (log_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"ERROR deleting food log: {str(e)}")
        return False

def delete_all_food_logs_by_date(user_id, date):
    """Delete all food log entries for a specific date."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM food_log WHERE user_id = ? AND entry_date = ?", (user_id, date))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()
        return rows_deleted
    except Exception as e:
        print(f"ERROR deleting all food logs: {str(e)}")
        return 0

def get_food_log_range(user_id, start_date, end_date):
    """Get food log for a date range."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM food_log WHERE user_id = ? AND entry_date BETWEEN ? AND ? ORDER BY entry_date DESC, entry_time DESC",
        (user_id, start_date, end_date)
    )
    logs = cursor.fetchall()
    conn.close()
    return logs

def add_health_metric(user_id, date, weight, bmi, water_intake_liters, sleep_hours, exercise_minutes, notes=""):
    """Add health metric."""
    if date is None:
        date = datetime.now().date()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO health_metrics 
        (user_id, date, weight, bmi, water_intake_liters, sleep_hours, exercise_minutes, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, date, weight, bmi, water_intake_liters, sleep_hours, exercise_minutes, notes))
    conn.commit()
    conn.close()

def get_health_metrics(user_id, start_date, end_date):
    """Get health metrics for a date range."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM health_metrics WHERE user_id = ? AND date BETWEEN ? AND ? ORDER BY date DESC",
        (user_id, start_date, end_date)
    )
    metrics = cursor.fetchall()
    conn.close()
    return metrics

def save_meal_plan(user_id, plan_name, plan_type, meals_data, total_calories):
    """Save meal plan."""
    try:
        print("="*80)
        print("SAVING MEAL PLAN TO DATABASE")
        print("="*80)
        print(f"User ID: {user_id}")
        print(f"Plan Name: {plan_name}")
        print(f"Plan Type: {plan_type}")
        print(f"Total Calories: {total_calories}")
        print(f"Meals Data Type: {type(meals_data)}")
        print(f"Meals Data Keys: {meals_data.keys() if isinstance(meals_data, dict) else 'Not a dict'}")
        
        # Convert to JSON string
        meals_json = json.dumps(meals_data)
        print(f"JSON Length: {len(meals_json)} characters")
        print(f"JSON Preview: {meals_json[:200]}...")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO meal_plans 
            (user_id, plan_name, plan_type, meals_data, total_calories)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, plan_name, plan_type, meals_json, total_calories))
        
        conn.commit()
        plan_id = cursor.lastrowid
        
        print(f"SUCCESS: Meal plan saved with ID {plan_id}")
        print("="*80 + "\n")
        
        # Verify it was saved
        cursor.execute("SELECT * FROM meal_plans WHERE id = ?", (plan_id,))
        saved_plan = cursor.fetchone()
        if saved_plan:
            print(f"VERIFICATION: Plan ID {plan_id} exists in database")
        else:
            print(f"WARNING: Plan ID {plan_id} not found after save!")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR in save_meal_plan: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        print("="*80 + "\n")
        return False

def get_meal_plans(user_id, limit=10):
    """Get recent meal plans."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM meal_plans WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    )
    plans = cursor.fetchall()
    conn.close()
    return plans

# Initialize database on import
if not os.path.exists(DB_PATH):
    init_db()
