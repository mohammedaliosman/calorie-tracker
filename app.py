import streamlit as st
import pandas as pd
import json
import os
import re
import hashlib
from datetime import date
from data import foods

st.set_page_config(page_title="Calorie Tracker", page_icon="🔥", layout="wide")

# --- CSS ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}

    [data-testid="stSidebar"] {
        display: none !important;
    }

    .main .block-container {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

    /* ============================
       أنيميشن
    ============================ */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes bounceIn {
        0%   { transform: scale(0.8); opacity: 0; }
        60%  { transform: scale(1.05); opacity: 1; }
        100% { transform: scale(1); }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-40px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes glow {
        0%   { box-shadow: 0 0 5px rgba(255,0,0,0.3); }
        50%  { box-shadow: 0 0 20px rgba(255,0,0,0.8); }
        100% { box-shadow: 0 0 5px rgba(255,0,0,0.3); }
    }

    /* ============================
       تطبيق الأنيميشن
    ============================ */
    h1 {
        color: #ff0000 !important;
        animation: fadeInDown 0.8s ease forwards;
    }
    h2, h3 {
        color: #ff0000 !important;
        animation: fadeInDown 0.6s ease forwards;
    }
    .main .block-container > div {
        animation: fadeInUp 0.7s ease forwards;
    }

    .stButton > button {
        background-color: #ff0000 !important;
        color: white !important;
        border: none;
        font-weight: bold;
        width: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease, background-color 0.3s ease !important;
        animation: fadeInUp 0.5s ease forwards;
    }
    .stButton > button:hover {
        transform: scale(1.04) !important;
        box-shadow: 0 6px 20px rgba(255, 0, 0, 0.4) !important;
        background-color: #cc0000 !important;
    }
    .stButton > button:active {
        transform: scale(0.97) !important;
    }

    .stProgress > div > div > div {
        transition: background-color 0.5s ease, width 0.8s ease !important;
    }

    .streak-card {
        background: linear-gradient(135deg, #ff0000, #ff6b6b);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        color: white !important;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 10px 0;
        animation: bounceIn 0.8s ease forwards, glow 3s ease-in-out infinite;
        transition: transform 0.3s ease;
    }
    .streak-card:hover {
        transform: scale(1.02);
    }

    .stSelectbox > div,
    .stNumberInput > div,
    .stTextInput > div {
        transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
        animation: fadeIn 0.6s ease forwards;
    }
    .stSelectbox > div:focus-within,
    .stNumberInput > div:focus-within,
    .stTextInput > div:focus-within {
        box-shadow: 0 0 10px rgba(255, 0, 0, 0.3) !important;
    }

    table {
        animation: slideInLeft 0.6s ease forwards;
    }

    .stSuccess, .stInfo, .stError {
        animation: fadeInDown 0.5s ease forwards;
    }

    .streamlit-expanderHeader {
        transition: background-color 0.3s ease !important;
    }
    .streamlit-expanderHeader:hover {
        background-color: rgba(255,0,0,0.1) !important;
    }

    .stRadio > div {
        animation: fadeIn 0.5s ease forwards;
    }

    /* ============================
       الجوال
    ============================ */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        h1 {
            font-size: 1.6rem !important;
            text-align: center;
        }
        [data-testid="column"] {
            width: 100% !important;
            flex: 100% !important;
            min-width: 100% !important;
        }
        .stButton > button {
            font-size: 1rem !important;
            padding: 12px !important;
        }
        .stSelectbox, .stNumberInput {
            font-size: 1rem !important;
        }
        table {
            font-size: 0.85rem !important;
            width: 100% !important;
        }
        .streak-card {
            font-size: 1rem !important;
            padding: 12px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================
# إدارة المستخدمين والبيانات
# ============================
DATA_DIR = "users_data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

def sanitize_username(username: str) -> str:
    username = username.strip()
    username = username.replace(" ", "_")
    username = re.sub(r"[^A-Za-z0-9_\-\.]", "", username)
    return username.lower()

def get_user_file(username):
    safe = sanitize_username(username)
    return f"{DATA_DIR}/{safe}.json"

def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def user_exists(username):
    return os.path.exists(get_user_file(username))

def email_in_use(email: str) -> bool:
    if not email:
        return False
    email = email.strip().lower()
    for fname in os.listdir(DATA_DIR):
        try:
            with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
                u = json.load(f)
                if u.get("email", "").strip().lower() == email:
                    return True
        except Exception:
            continue
    return False

def find_username_by_email(email: str):
    if not email:
        return None
    email = email.strip().lower()
    for fname in os.listdir(DATA_DIR):
        try:
            with open(os.path.join(DATA_DIR, fname), "r", encoding="utf-8") as f:
                u = json.load(f)
                if u.get("email", "").strip().lower() == email:
                    return fname.replace(".json", "")
        except Exception:
            continue
    return None

def load_user_data(username):
    file_path = get_user_file(username)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "streak": 0,
        "last_date": "",
        "meals": [],
        "daily_goal": 2000,
        "password_hash": None,
        "security_answer_hash": None,
        "email": None
    }

def save_user_data(username, data):
    with open(get_user_file(username), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============================
# الترجمة
# ============================
translations = {
    "en": {
        "title": "Calorie Tracker",
        "goal": "Daily Goal (cal)",
        "choose": "Food:",
        "amount": "Amount (g):",
        "add": "Add",
        "meals": "Your Meals",
        "remaining": "Remaining",
        "consumed": "Consumed",
        "clear": "Clear All",
        "streak": "Days Goal Completed",
        "goal_done": "✅ Goal completed today! +1 day added!",
        "goal_not_done": "Keep going to complete today's goal!",
        "settings": "⚙️ Settings",
        "language": "🌐 Language",
        "login": "Login / Register",
        "username": "Username",
        "password": "Password",
        "confirm_password": "Confirm Password",
        "register": "Register",
        "forgot_password": "Forgot Password",
        "email": "Email",
        "security_question": "Security question: What is your favorite color?",
        "reset_password": "Reset Password",
        "reset_success": "Password reset successful. Please login with your new password.",
        "user_exists": "Username already exists. Choose another username.",
        "email_in_use": "Email already in use. Use another email.",
        "login_failed": "Login failed. Check username/email and password.",
        "register_success": "Registration successful. You can now login."
    },
    "ar": {
        "title": "متتبع السعرات",
        "goal": "الهدف اليومي (سعرة)",
        "choose": "الطعام:",
        "amount": "الكمية (جرام):",
        "add": "أضف",
        "meals": "وجباتك",
        "remaining": "المتبقي",
        "consumed": "المستهلك",
        "clear": "مسح الكل",
        "streak": "أيام أكملت الهدف",
        "goal_done": "✅ أكملت هدفك اليوم! +1 يوم!",
        "goal_not_done": "استمر لإكمال هدف اليوم!",
        "settings": "⚙️ الإعدادات",
        "language": "🌐 اللغة",
        "login": "تسجيل الدخول / إنشاء حساب",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "confirm_password": "تأكيد كلمة المرور",
        "register": "إنشاء حساب",
        "forgot_password": "نسيت كلمة المرور",
        "email": "البريد الإلكتروني",
        "security_question": "سؤال أمني: ما هو لونك المفضل؟",
        "reset_password": "إعادة تعيين كلمة المرور",
        "reset_success": "تم إعادة تعيين كلمة المرور. الرجاء تسجيل الدخول بالكلمة الجديدة.",
        "user_exists": "اسم المستخدم موجود بالفعل. اختر اسمًا آخر.",
        "email_in_use": "البريد مستخدم بالفعل. استخدم بريدًا آخر.",
        "login_failed": "فشل تسجيل الدخول. تحقق من اسم المستخدم/البريد/كلمة المرور.",
        "register_success": "تم إنشاء الحساب بنجاح. يمكنك الآن تسجيل الدخول."
    }
}

# ============================
# تهيئة الحالة
# ============================
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "username" not in st.session_state:
    st.session_state.username = None
if "meals" not in st.session_state:
    st.session_state.meals = []
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "last_date" not in st.session_state:
    st.session_state.last_date = ""
if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 2000

lang = st.session_state.lang
t = translations[lang]

# ============================
# صفحة تسجيل الدخول
# ============================
if st.session_state.username is None:
    st.title("🔥 Calorie Tracker")

    mode = st.radio("", (t["login"], t["register"], t["forgot_password"]))

    if mode == t["login"]:
        username_input = st.text_input(t["username"] + " (Username or Email)")
        password_input = st.text_input(t["password"], type="password")
        if st.button("Submit"):
            if username_input and password_input:
                lookup = username_input.strip()
                if "@" in lookup and not user_exists(lookup):
                    found = find_username_by_email(lookup)
                    if found:
                        lookup = found
                if user_exists(lookup):
                    user_data = load_user_data(lookup)
                    if user_data.get("password_hash") and user_data["password_hash"] == hash_text(password_input):
                        st.session_state.username = lookup
                        st.session_state.meals = user_data["meals"]
                        st.session_state.streak = user_data["streak"]
                        st.session_state.last_date = user_data["last_date"]
                        st.session_state.daily_goal = user_data["daily_goal"]
                        st.rerun()
                    else:
                        st.error(t["login_failed"])
                else:
                    st.error(t["login_failed"])
        st.markdown("---")

    elif mode == t["register"]:
        st.subheader(t["register"])
        new_username = st.text_input(t["username"] + " (ID)")
        new_email = st.text_input(t["email"])
        new_password = st.text_input(t["password"], type="password")
        confirm_password = st.text_input(t["confirm_password"], type="password")
        security_answer = st.text_input(t["security_question"])
        if st.button(t["register"]):
            if not new_username or not new_password or not confirm_password or not security_answer or not new_email:
                st.error("Please fill all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif user_exists(new_username):
                st.error(t["user_exists"])
            elif not EMAIL_REGEX.match(new_email.strip()):
                st.error("Invalid email format.")
            elif email_in_use(new_email):
                st.error(t["email_in_use"])
            else:
                user_data = {
                    "streak": 0,
                    "last_date": "",
                    "meals": [],
                    "daily_goal": 2000,
                    "password_hash": hash_text(new_password),
                    "security_answer_hash": hash_text(security_answer.strip().lower()),
                    "email": new_email.strip().lower()
                }
                save_user_data(new_username, user_data)
                st.success(t["register_success"])
        st.markdown("---")

    elif mode == t["forgot_password"]:
        st.subheader(t["forgot_password"])
        fp_identifier = st.text_input("Username or Email for reset")
        fp_security = st.text_input(t["security_question"])
        fp_new_password = st.text_input(t["reset_password"], type="password")
        fp_confirm = st.text_input(t["confirm_password"], type="password")
        if st.button(t["reset_password"]):
            if not fp_identifier or not fp_security or not fp_new_password or not fp_confirm:
                st.error("Please fill all fields.")
            else:
                lookup = fp_identifier.strip()
                if "@" in lookup and not user_exists(lookup):
                    found = find_username_by_email(lookup)
                    if found:
                        lookup = found
                if not user_exists(lookup):
                    st.error("Username not found.")
                elif fp_new_password != fp_confirm:
                    st.error("Passwords do not match.")
                else:
                    user_data = load_user_data(lookup)
                    stored_sec_hash = user_data.get("security_answer_hash")
                    if stored_sec_hash and stored_sec_hash == hash_text(fp_security.strip().lower()):
                        user_data["password_hash"] = hash_text(fp_new_password)
                        save_user_data(lookup, user_data)
                        st.success(t["reset_success"])
                    else:
                        st.error("Security answer incorrect.")
        st.markdown("---")

    st.stop()

# ============================
# المنطق بعد الدخول
# ============================
daily_goal = st.session_state.daily_goal

if lang == "ar":
    st.markdown("""
    <style>
        [data-testid='stAppViewContainer'] { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# ============================
# العنوان
# ============================
st.title(f"🔥 {t['title']} - {st.session_state.username}")

# ============================
# الإعدادات
# ============================
with st.expander(t["settings"]):
    col1, col2 = st.columns(2)
    with col1:
        mobile_lang = st.selectbox(
            t["language"],
            options=["en", "ar"],
            format_func=lambda x: "English" if x == "en" else "العربية",
            index=0 if lang == "en" else 1
        )
        if mobile_lang != lang:
            st.session_state.lang = mobile_lang
            st.rerun()
    with col2:
        mobile_goal = st.number_input(
            t["goal"],
            min_value=500,
            value=daily_goal,
            step=100
        )
        if mobile_goal != daily_goal:
            st.session_state.daily_goal = mobile_goal
            existing = load_user_data(st.session_state.username)
            save_user_data(st.session_state.username, {
                "streak": st.session_state.streak,
                "last_date": st.session_state.last_date,
                "meals": st.session_state.meals,
                "daily_goal": mobile_goal,
                "password_hash": existing.get("password_hash"),
                "security_answer_hash": existing.get("security_answer_hash"),
                "email": existing.get("email")
            })
            st.rerun()

# ============================
# عداد الأيام
# ============================
st.markdown(f"""
<div class="streak-card">
    🏆 {t['streak']}: {st.session_state.streak}
</div>
""", unsafe_allow_html=True)

# ============================
# الإدخال
# ============================
col1, col2 = st.columns(2)
with col1:
    food_keys = list(foods.keys())
    food_display = [foods[k]["ar"] if lang == "ar" else k for k in food_keys]
    food_index = st.selectbox(
        t["choose"],
        range(len(food_keys)),
        format_func=lambda i: food_display[i]
    )
    food = food_keys[food_index]

with col2:
    grams = st.number_input(t["amount"], min_value=1, value=100)

if st.button(t["add"]):
    cal = (foods[food]["calories"] * grams) / 100
    food_name = foods[food]["ar"] if lang == "ar" else food
    st.session_state.meals.append({
        "food": food_name,
        "calories": round(cal, 1)
    })
    existing = load_user_data(st.session_state.username)
    save_user_data(st.session_state.username, {
        "streak": st.session_state.streak,
        "last_date": st.session_state.last_date,
        "meals": st.session_state.meals,
        "daily_goal": st.session_state.daily_goal,
        "password_hash": existing.get("password_hash"),
        "security_answer_hash": existing.get("security_answer_hash"),
        "email": existing.get("email")
    })
    st.rerun()

# ============================
# المنطق والتقدم
# ============================
if st.session_state.meals:
    df = pd.DataFrame(st.session_state.meals)
    consumed = df['calories'].sum()
    remaining = max(0, daily_goal - consumed)
    progress_pct = min(consumed / daily_goal, 1.0)

    if progress_pct < 0.4:
        emoji, color = "🏋️", "green"
    elif progress_pct < 0.8:
        emoji, color = "🔥", "orange"
    elif progress_pct < 1.0:
        emoji, color = "🚀", "red"
    else:
        emoji, color = "🏆", "red"

    st.write(f"### {emoji} {t['consumed']}: {consumed} | {t['remaining']}: {remaining}")

    st.markdown(f"""
        <style>
            .stProgress > div > div > div {{ background-color: {color} !important; }}
        </style>
    """, unsafe_allow_html=True)
    st.progress(progress_pct)

    today = str(date.today())
    if progress_pct >= 1.0 and st.session_state.last_date != today:
        st.session_state.streak += 1
        st.session_state.last_date = today
        existing = load_user_data(st.session_state.username)
        save_user_data(st.session_state.username, {
            "streak": st.session_state.streak,
            "last_date": today,
            "meals": st.session_state.meals,
            "daily_goal": st.session_state.daily_goal,
            "password_hash": existing.get("password_hash"),
            "security_answer_hash": existing.get("security_answer_hash"),
            "email": existing.get("email")
        })
        st.success(t["goal_done"])
    elif progress_pct < 1.0:
        st.info(t["goal_not_done"])

    st.divider()
    st.subheader(t["meals"])
    st.table(df)

    if st.button(t["clear"]):
        st.session_state.meals = []
        existing = load_user_data(st.session_state.username)
        save_user_data(st.session_state.username, {
            "streak": st.session_state.streak,
            "last_date": st.session_state.last_date,
            "meals": [],
            "daily_goal": st.session_state.daily_goal,
            "password_hash": existing.get("password_hash"),
            "security_answer_hash": existing.get("security_answer_hash"),
            "email": existing.get("email")
        })
        st.rerun()