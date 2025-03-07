import re
import random
import streamlit as st

# Common Weak Passwords List
blacklist_passwords = ["password", "123456", "qwerty", "password123", "admin", "letmein", "123456789", "iloveyou", "welcome"]

# Function to generate a strong password
def generate_strong_password(length=12):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    return "".join(random.choice(characters) for _ in range(length))

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Blacklist Check
    if password in blacklist_passwords:
        return 0, "❌ Weak Password - Commonly used, choose a unique password.", ["❌ This password is too common."]

    # Length Check
    if len(password) >= 12:
        score += 2  
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 2  
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Strength Rating & Progress Bar
    if score >= 5:
        return score, "✅ Strong Password!", feedback
    elif score >= 3:
        return score, "⚠️ Moderate Password - Consider adding more security features.", feedback
    else:
        return score, "❌ Weak Password - Improve it using the suggestions above.", feedback

# Streamlit UI
st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="centered")


st.markdown("""
   <h1 style='color: #ff007f; text-align: center;'>🔐 Password Strength Meter</h1> 
    <p style='text-align: center;'>Check your password strength & generate secure passwords instantly!</p>
    """, unsafe_allow_html=True)

# User Password Input
password = st.text_input("🔑 Enter your password:", type="password", )

if password:
    strength_score, strength_msg, suggestions = check_password_strength(password)
    
    try:
        # Show Strength Progress Bar (Ensuring value is between 0 and 1)
        progress_value = min(strength_score / 5, 1.0)
        st.progress(progress_value)
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}. Please enter a valid password.")

    # Show Strength Result
    st.subheader(strength_msg)
    
    for suggestion in suggestions:
        st.warning(suggestion)

# Generate Strong Password
st.markdown("---")
st.subheader("⚡ Generate a Strong Password")
length = st.slider("Select Password Length:", min_value=8, max_value=20, value=12)

if st.button("🔄 Generate Password"):
    strong_password = generate_strong_password(length)
    st.success(f"💡 Suggested Strong Password: `{strong_password}`")


# Custom CSS Styling
st.markdown("""
<style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        color: white;
    }

    /* Headings */
    h2 {
        color: white;
        text-align: center;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #ff007f, #ff4f00);
         color: white !important;   /* Ensure text is visible */
         font-weight: bold;   /* Make text bold */
        width: 100%;
        border-radius: 8px;
        transition: 0.3s;
        font-size: 16px;
        padding: 10px;
        border: none;
        
    }

   .stButton>button:hover {
    background: linear-gradient(90deg, #ff4f00, #ff007f);
    transform: scale(1.03);
    box-shadow: 0px 6px 15px rgba(255, 79, 0, 0.5);
    color: white !important;  /* 👈 Text color fix */
}

    /* Input Box */
    .stTextInput>div>div>input {
        background-color: #1a1a2e;
        color: white;
        border: 2px solid #ff007f;
        border-radius: 5px;
        padding: 8px;
        font-size: 16px;
    }

    /* Slider Bar */
    .stSlider .css-1aumxhk {
        background-color: #ff007f !important;
    }

    /* Section Dividers */
    hr {
        border: 1px solid #ff4f00;
    }

</style>
""", unsafe_allow_html=True)
