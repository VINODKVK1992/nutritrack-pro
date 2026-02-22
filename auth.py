"""Authentication module for user login and registration."""
import hashlib
import hmac
import streamlit as st
from database import create_user, get_user

def hash_password(password):
    """Hash password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed_password):
    """Verify password against hash."""
    return hash_password(password) == hashed_password

def validate_password_strength(password):
    """Validate password strength with strict rules."""
    import re
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
    
    return True, "Password is strong"

def register_user(username, email, password, confirm_password):
    """
    Register a new user.
    
    Args:
        username: Username
        email: Email address
        password: Password
        confirm_password: Password confirmation
    
    Returns:
        Tuple of (success, message, user_id)
    """
    # Validation
    if not username or not email or not password:
        return False, "Please fill all fields", None
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters", None
    
    if password != confirm_password:
        return False, "Passwords do not match", None
    
    # Validate password strength
    is_strong, message = validate_password_strength(password)
    if not is_strong:
        return False, message, None
    
    if "@" not in email:
        return False, "Invalid email address", None
    
    # Check if user exists
    if get_user(username):
        return False, "Username already exists", None
    
    # Create user
    hashed_password = hash_password(password)
    user_id = create_user(username, hashed_password, email)
    
    if user_id:
        return True, "Registration successful! Please log in.", user_id
    else:
        return False, "Email already registered", None

def login_user(username, password):
    """
    Authenticate user.
    
    Args:
        username: Username
        password: Password
    
    Returns:
        Tuple of (success, message, user)
    """
    if not username or not password:
        return False, "Please enter username and password", None
    
    user = get_user(username)
    
    if not user:
        return False, "Invalid username", None
    
    if not verify_password(password, user[2]):  # user[2] is password hash
        return False, "Invalid password", None
    
    return True, "Login successful", user

def init_session_state():
    """Initialize session state for authentication."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
