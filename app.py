import streamlit as st
import pandas as pd
import json
import os
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

    h1, h2, h3 { color: #ff0000 !important; }
    .stButton > button {
        background-color: #ff0000 !important;
        color: white !important;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .stProgress > div > div > div { transition: background-color 0.5s ease; }

    .streak-card {
        background: linear-gradient(135deg, #ff0000, #ff6b6b);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        color: white !important;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 10px 0;
    }

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

def get_user_file(username):
    return f"{DATA_DIR}/{username}.json"

def load_user_data(username):
    file_path = get_user_file(username)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {"streak": 0, "last_date": "", "meals": [], "daily_goal": 2000}

def save_user_data(username, data):
    with open(get_user_file(username), "w") as f:
        json.dump(data, f)

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
        "username": "Username"
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
        "username": "اسم المستخدم"
    }
}

# ============================
# تهيئة الحالة
# ============================
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "username" not in st.session_state:
    st.session_state.username = None

lang = st.session_state.lang
t = translations[lang]

# ============================
# صفحة تسجيل الدخول
# ============================
if st.session_state.username is None:
    st.title("🔥 Calorie Tracker")
    username_input = st.text_input(t["username"])
    if st.button(t["login"]):
        if username_input:
            st.session_state.username = username_input
            # تحميل بيانات المستخدم
            data = load_user_data(username_input)
            st.session_state.meals = data["meals"]
            st.session_state.streak = data["streak"]
            st.session_state.last_date = data["last_date"]
            st.session_state.daily_goal = data["daily_goal"]
            st.rerun()
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
            save_user_data(st.session_state.username, {
                "streak": st.session_state.streak,
                "last_date": st.session_state.last_date,
                "meals": st.session_state.meals,
                "daily_goal": mobile_goal
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
    save_user_data(st.session_state.username, {
        "streak": st.session_state.streak,
        "last_date": st.session_state.last_date,
        "meals": st.session_state.meals,
        "daily_goal": st.session_state.daily_goal
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

    # ============================
    # حفظ التقدم
    # ============================
    today = str(date.today())
    if progress_pct >= 1.0 and st.session_state.last_date != today:
        st.session_state.streak += 1
        st.session_state.last_date = today
        save_user_data(st.session_state.username, {
            "streak": st.session_state.streak,
            "last_date": today,
            "meals": st.session_state.meals,
            "daily_goal": st.session_state.daily_goal
        })
        st.success(t["goal_done"])
    elif progress_pct < 1.0:
        st.info(t["goal_not_done"])

    st.divider()
    st.subheader(t["meals"])
    st.table(df)

    if st.button(t["clear"]):
        st.session_state.meals = []
        save_user_data(st.session_state.username, {
            "streak": st.session_state.streak,
            "last_date": st.session_state.last_date,
            "meals": [],
            "daily_goal": st.session_state.daily_goal
        })
        st.rerun()