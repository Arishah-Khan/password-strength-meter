
import streamlit as st
import random
import string
import hashlib
import requests

st.set_page_config(
    page_title="Field-Based Password Strength Meter & Generator",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

password_rules = {
    "Financial Field": {
        "length": 12,
        "special": 2,
        "uppercase": 1,
        "lowercase": 1,
        "digits": 1,
    },
    "Social Networks": {
        "length": 10,
        "special": 1,
        "uppercase": 1,
        "lowercase": 1,
        "digits": 1,
    },
    "Technology & IT": {
        "length": 14,
        "special": 2,
        "uppercase": 2,
        "lowercase": 2,
        "digits": 2,
    },
    "Healthcare Services": {
        "length": 12,
        "special": 1,
        "uppercase": 1,
        "lowercase": 1,
        "digits": 1,
        "description": "Healthcare services deal with sensitive data that needs protection.",
        "complexity": "High"
    },
    "Online Retail": {
        "length": 12,
        "special": 2,
        "uppercase": 1,
        "lowercase": 1,
        "digits": 2,
    },
    "Educational Institutions": {
        "length": 10,
        "special": 1,
        "uppercase": 1,
        "lowercase": 1,
        "digits": 1,
      
    },
    "Government Agencies": {
        "length": 16,
        "special": 3,
        "uppercase": 2,
        "lowercase": 2,
        "digits": 3,
    },
    "Consumer Goods Retail": {
        "length": 12,
        "special": 2,
        "uppercase": 1,
        "lowercase": 1,
        "digits": 2,

    },
    "Investment & Finance": {
        "length": 14,
        "special": 2,
        "uppercase": 2,
        "lowercase": 2,
        "digits": 3,
    },
}

st.markdown(
    """
    <style>
    @media (max-width: 600px) {
        h1 {
            font-size: 26px !important;
            color: #2E86C1;
        }
        h2 {
            font-size: 22px !important;
            color: #2874A6;
        }
        h3 {
            font-size: 20px !important;
            color: #1B4F72;
        }
        .stSlider {
            font-size: 14px !important;
        }
        .stButton button {
            font-size: 15px !important;
        }
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4CAF50, #2196F3) !important;
        border-radius: 8px;
    }

    .stButton > button {
        background-color: #2196F3;
        color: white;
        border-radius: 8px;
        padding: 12px 22px;
        font-size: 16px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: white;
        colour: #2196F3
        transform: scale(1.05);
    }

    .stSuccess {
        color: #2ECC71;
        font-weight: bold;
        font-size: 18px;
    }
    .stWarning {
        color: #F39C12;
        font-weight: bold;
        font-size: 18px;
    }
    .stError {
        color: #E74C3C;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

SPECIAL_CHARACTERS = r""" !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""

def password_strength(password):
    score = 0
    
    if any(c.isupper() for c in password): score += 2  
    if any(c.islower() for c in password): score += 2 
    if any(c.isdigit() for c in password): score += 2 
    if any(c in SPECIAL_CHARACTERS for c in password): score += 2  
    
    if len(password) >= 12: score += 2  
    
    if score >= 9:
        return "Strong", score
    elif score >= 6:
        return "Medium", score
    else:
        return "Weak", score

def validate_password(password, rules):
    errors = []
    if len(password) < rules["length"]:
        errors.append(f"Password must be at least {rules['length']} characters long.")
    if sum(1 for c in password if c.isupper()) < rules["uppercase"]:
        errors.append(f"Must include at least {rules['uppercase']} uppercase letter(s).")
    if sum(1 for c in password if c.islower()) < rules["lowercase"]:
        errors.append(f"Must include at least {rules['lowercase']} lowercase letter(s).")
    if sum(1 for c in password if c.isdigit()) < rules["digits"]:
        errors.append(f"Must include at least {rules['digits']} digit(s).")
    if sum(1 for c in password if c in SPECIAL_CHARACTERS) < rules["special"]:
        errors.append(f"Must include at least {rules['special']} special character(s).")
    return errors

def check_password_breach(password):
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    if response.status_code == 200:
        for line in response.text.splitlines():
            if line.split(":")[0] == suffix:
                return int(line.split(":")[1])
    return 0

def generate_custom_password(length, uppercase, lowercase, digits, special):
    password_chars = (
        random.choices(string.ascii_uppercase, k=uppercase) +
        random.choices(string.ascii_lowercase, k=lowercase) +
        random.choices(string.digits, k=digits) +
        random.choices(SPECIAL_CHARACTERS, k=special)
    )
    password_chars += random.choices(string.ascii_letters + string.digits + SPECIAL_CHARACTERS, k=length - len(password_chars))
    random.shuffle(password_chars)
    return "".join(password_chars)

def custom_password(uppercase, lowercase, digits, special):
    password_chars = (
        random.choices(string.ascii_uppercase, k=uppercase) +
        random.choices(string.ascii_lowercase, k=lowercase) +
        random.choices(string.digits, k=digits) +
        random.choices(SPECIAL_CHARACTERS, k=special)
    )
    password_chars += random.choices(string.ascii_letters + string.digits + SPECIAL_CHARACTERS)
    random.shuffle(password_chars)
    return "".join(password_chars)

st.title("Field-Based Password Strength Meter & Generator")

field = st.selectbox("Select your field:", ["Select Field"] + list(password_rules.keys()))

if "field" not in st.session_state:
    st.session_state.field = field
if field != st.session_state.field:
    st.session_state.field = field
    st.session_state.choice = None  

if field != "Select Field":
    st.info(f"Password Rules for {field}: {password_rules[field]}")
    rules = password_rules[field]
    choice = st.radio("What do you want to do?:", ["Analyze your password strength", "Create a strong password"], key="choice")
    
    if choice == "Analyze your password strength":
        user_password = st.text_input("Type your password to check its strength:", type="password")
        
        if user_password:
            strength, score = password_strength(user_password)
            st.progress(score / 10)
            st.write(f"**Password Strength Level:** {strength}")
            
            errors = validate_password(user_password, rules)
            if errors:
                for error in errors:
                    st.warning(error)
            else:
                st.success("Your password meets field requirements!")
                if st.button("Verify if your password is leaked"):
                    with st.spinner("Checking for breaches..."):
                        breaches = check_password_breach(user_password)
                        if breaches > 0:
                            st.error(f"Your password was found in {breaches} breaches! Choose another password.")
                        else:
                            st.success("Your password is safe!")
                            st.text_input("Copy your password:", value=user_password, disabled=False)

    elif choice == "Create a strong password":
        length = st.slider("Password length:", rules["length"], rules["length"] + 8, rules["length"])
        uppercase = st.slider("Uppercase letters:", 0, length, rules["uppercase"])
        lowercase = st.slider("Lowercase letters:", 0, length - uppercase, rules["lowercase"])
        digits = st.slider("Numbers:", 0, length - uppercase - lowercase, rules["digits"])
        special = st.slider("Special characters:", 0, length - uppercase - lowercase - digits, rules["special"])

        total_chars = uppercase + lowercase + digits + special

        temp_password = generate_custom_password(length, uppercase, lowercase, digits, special)
        temp = custom_password(uppercase, lowercase, digits, special)
        strength, score = password_strength(temp)
        st.progress(min(score / 5, 1.0))
        st.write(f"**Password Strength:** {strength}")

        missing_requirements = []
        if uppercase < rules["uppercase"]:
            missing_requirements.append(f"Must include at least {rules['uppercase']} uppercase letter(s).")
        if lowercase < rules["lowercase"]:
            missing_requirements.append(f"Must include at least {rules['lowercase']} lowercase letter(s).")
        if digits < rules["digits"]:
            missing_requirements.append(f"Must include at least {rules['digits']} digit(s).")
        if special < rules["special"]:
            missing_requirements.append(f"Must include at least {rules['special']} special character(s).")

        if length < rules["length"]:
            missing_requirements.append(f"Password must be at least {rules['length']} characters long.")

        if total_chars != length:
            missing_requirements.append(f"Your total characters do not match the selected password length. Please adjust the values.")

        if missing_requirements:
            for requirement in missing_requirements:
                st.warning(requirement)

            generate_button_enabled = False
        else:
            st.success("Your password meets all the field requirements!")
            generate_button_enabled = True

        if generate_button_enabled:
            if st.button("Generate Password"):
                st.text_input("Your generated password:", value=temp_password, disabled=False)
                st.info("Click inside the box and press Ctrl + C to copy.")