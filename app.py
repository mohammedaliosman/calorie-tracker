import streamlit as st
import pandas as pd
from data import foods

st.set_page_config(page_title="Calorie Tracker", page_icon="🔥", layout="wide")

# --- إخفاء شريط GitHub وStreamlit ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    [data-testid="stStatusWidget"] {display: none;}

    /* تحسين الجوال */
    @media (max-width: 768px) {
        h1 { font-size: 1.5rem !important; }
        h2, h3 { font-size: 1.2rem !important; }
        .stButton > button { font-size: 0.9rem !important; padding: 8px !important; }
        [data-testid="stSidebar"] { min-width: 80% !important; }
        .stSelectbox, .stNumberInput { font-size: 0.9rem !important; }
        table { font-size: 0.8rem !important; }
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

    /* بطاقة العداد */
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
</style>
""", unsafe_allow_html=True)

# الترجمة
translations = {
    "en": {
        "title": "Calorie Tracker",
        "lang": "Language",
        "goal": "Daily Goal (cal)",
        "choose": "Food:",
        "amount": "Amount (g):",
        "add": "Add",
        "meals": "Your Meals",
        "remaining": "Remaining",
        "consumed": "Consumed",
        "clear": "Clear All",
        "streak": "🏆 Days Goal Completed",
        "goal_done": "✅ Goal completed today! +1 day added!",
        "goal_not_done": "Keep going to complete today's goal!",
    },
    "ar": {
        "title": "متتبع السعرات",
        "lang": "اللغة",
        "goal": "الهدف اليومي (سعرة)",
        "choose": "الطعام:",
        "amount": "الكمية (جرام):",
        "add": "أضف",
        "meals": "وجباتك",
        "remaining": "المتبقي",
        "consumed": "المستهلك",
        "clear": "مسح الكل",
        "streak": "🏆 أيام أكملت الهدف",
        "goal_done": "✅ أكملت هدفك اليوم! +1 يوم!",
        "goal_not_done": "استمر لإكمال هدف اليوم!",
    }
}

# الشريط الجانبي
lang = st.sidebar.selectbox(
    "🌐 Language / اللغة",
    options=["en", "ar"],
    format_func=lambda x: "English" if x == "en" else "العربية"
)
t = translations[lang]
daily_goal = st.sidebar.number_input(t["goal"], min_value=500, value=2000, step=100)

if lang == "ar":
    st.markdown("""
    <style>
        [data-testid='stAppViewContainer'] { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

st.title(f"🔥 {t['title']}")

# ============================
# تهيئة session_state
# ============================
if "meals" not in st.session_state:
    st.session_state.meals = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "goal_counted" not in st.session_state:
    st.session_state.goal_counted = False

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
    food = st.selectbox(t["choose"], list(foods.keys()))
with col2:
    grams = st.number_input(t["amount"], min_value=1, value=100)

if st.button(t["add"]):
    cal = (foods[food]["calories"] * grams) / 100
    st.session_state.meals.append({"food": food, "calories": round(cal, 1)})
    st.rerun()

# ============================
# المنطق والتقدم
# ============================
if st.session_state.meals:
    df = pd.DataFrame(st.session_state.meals)
    consumed = df['calories'].sum()
    remaining = max(0, daily_goal - consumed)
    progress_pct = min(consumed / daily_goal, 1.0)

    # تحديد الإيموجي واللون
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
    # عداد الأيام - يضيف يوم عند إكمال الهدف
    # ============================
    if progress_pct >= 1.0 and not st.session_state.goal_counted:
        st.session_state.streak += 1
        st.session_state.goal_counted = True
        st.success(t["goal_done"])
    elif progress_pct < 1.0:
        st.info(t["goal_not_done"])

    st.divider()
    st.subheader(t["meals"])
    st.table(df)

    if st.button(t["clear"]):
        st.session_state.meals = []
        st.session_state.goal_counted = False
        st.rerun()