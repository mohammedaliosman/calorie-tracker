import streamlit as st
import pandas as pd
from data import foods

st.set_page_config(page_title="Calorie Tracker", page_icon="🔥", layout="wide")

# --- CSS للتصميم الاحترافي (يدعم الدارك واللايت) ---
st.markdown("""
<style>
    /* تنسيق العناوين والأزرار باللون الأحمر */
    h1, h2, h3 { color: #ff0000 !important; }
    .stButton > button { background-color: #ff0000 !important; color: white !important; border: none; font-weight: bold; }

    /* تنسيق الأرقام والبيانات */
    [data-testid="stMetricValue"] { color: #ff0000 !important; }

    /* شريط التقدم (تنسيق مخصص) */
    .stProgress > div > div > div { transition: background-color 0.5s ease; }
</style>
""", unsafe_allow_html=True)

# الترجمة
translations = {
    "en": {"title": "Calorie Tracker", "lang": "Language", "goal": "Daily Goal (cal)", "choose": "Food:",
           "amount": "Amount (g):", "add": "Add", "meals": "Your Meals", "remaining": "Remaining",
           "consumed": "Consumed", "clear": "Clear All"},
    "ar": {"title": "متتبع السعرات", "lang": "اللغة", "goal": "الهدف اليومي (سعرة)", "choose": "الطعام:",
           "amount": "الكمية (جرام):", "add": "أضف", "meals": "وجباتك", "remaining": "المتبقي", "consumed": "المستهلك",
           "clear": "مسح الكل"}
}

# الشريط الجانبي
lang = st.sidebar.selectbox("🌐 Language / اللغة", options=["en", "ar"],
                            format_func=lambda x: "English" if x == "en" else "العربية")
t = translations[lang]
daily_goal = st.sidebar.number_input(t["goal"], min_value=500, value=2000, step=100)

if lang == "ar":
    st.markdown("<style>[data-testid='stAppViewContainer'] { direction: rtl; text-align: right; }</style>",
                unsafe_allow_html=True)

st.title(f"🔥 {t['title']}")

if "meals" not in st.session_state: st.session_state.meals = []

# الإدخال
col1, col2 = st.columns(2)
with col1: food = st.selectbox(t["choose"], list(foods.keys()))
with col2: grams = st.number_input(t["amount"], min_value=1, value=100)

if st.button(t["add"]):
    cal = (foods[food]["calories"] * grams) / 100
    st.session_state.meals.append({"food": food, "calories": round(cal, 1)})
    st.rerun()

# المنطق والتقدم
if st.session_state.meals:
    df = pd.DataFrame(st.session_state.meals)
    consumed = df['calories'].sum()
    remaining = max(0, daily_goal - consumed)
    progress_pct = min(consumed / daily_goal, 1.0)

    # اختيار لون الشريط حسب النسبة
    color = "green" if progress_pct < 0.5 else "orange" if progress_pct < 0.8 else "red"

    # عرض التقدم
    st.write(f"**{t['consumed']}:** {consumed} | **{t['remaining']}:** {remaining}")
    st.markdown(f"""
        <style>
            .stProgress > div > div > div {{ background-color: {color} !important; }}
        </style>
    """, unsafe_allow_html=True)
    st.progress(progress_pct)

    st.divider()
    st.subheader(t["meals"])
    st.table(df)

    if st.button(t["clear"]):
        st.session_state.meals = []
        st.rerun()