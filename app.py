import streamlit as st
import pandas as pd
import plotly.express as px
from data import foods  # استدعاء البيانات من الملف الجديد

st.set_page_config(page_title="Calorie Tracker", page_icon="🏋️", layout="wide")

# CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); }
    h1 { background: linear-gradient(90deg, #00c9ff, #92fe9d); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5rem !important; font-weight: 800 !important; text-align: center; padding: 20px 0; }
    h2, h3 { color: #00c9ff !important; font-weight: 700 !important; }
    [data-testid="stMetric"] { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(0, 201, 255, 0.3); border-radius: 15px; padding: 15px; }
    [data-testid="stMetricValue"] { color: #00c9ff !important; font-size: 1.8rem !important; font-weight: 800 !important; }
    [data-testid="stMetricLabel"] { color: #92fe9d !important; font-weight: 600 !important; }
    .stButton > button { background: linear-gradient(90deg, #00c9ff, #92fe9d); color: #0f2027 !important; border: none; border-radius: 25px; font-weight: 700; width: 100%; }
    [data-testid="stSidebar"] { background: rgba(15, 32, 39, 0.95) !important; }
    p, div, span, label { color: #e0e0e0 !important; }
</style>
""", unsafe_allow_html=True)

# Translations
translations = {
    "en": {"title": "🏋️ Calorie Tracker", "add_meal": "🍽️ Add a Meal", "choose_food": "Choose a food:",
           "amount": "Amount (grams):", "add_button": "➕ Add Meal", "today_meals": "📋 Today's Meals",
           "total": "🔥 Total", "clear": "🗑️ Clear All Meals", "analytics": "📊 Analytics"},
    "ar": {"title": "🏋️ تتبع السعرات الحرارية", "add_meal": "🍽️ إضافة وجبة", "choose_food": "اختر طعاماً:",
           "amount": "الكمية (جرام):", "add_button": "➕ إضافة وجبة", "today_meals": "📋 وجبات اليوم",
           "total": "🔥 المجموع", "clear": "🗑️ مسح كل الوجبات", "analytics": "📊 التحليلات"}
}

lang = st.sidebar.selectbox("Language", options=["en", "ar"],
                            format_func=lambda x: "English 🇬🇧" if x == "en" else "العربية 🇸🇦")
t = translations[lang]

if lang == "ar": st.markdown("<style>.stApp { direction: rtl; text-align: right; }</style>", unsafe_allow_html=True)

st.title(t["title"])
if "meals" not in st.session_state: st.session_state.meals = []

# UI
col1, col2 = st.columns(2)
with col1: food = st.selectbox(t["choose_food"], list(foods.keys()))
with col2: grams = st.number_input(t["amount"], min_value=1, value=100)

if st.button(t["add_button"], use_container_width=True):
    cal = (foods[food]["calories"] * grams) / 100
    st.session_state.meals.append({"food": food, "calories": round(cal, 1)})
    st.rerun()

st.divider()
if st.session_state.meals:
    st.subheader(t["today_meals"])
    df = pd.DataFrame(st.session_state.meals)
    st.table(df)

    st.subheader(t["analytics"])
    fig = px.bar(df, x='food', y='calories', color='calories', color_continuous_scale='Viridis')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    if st.button(t["clear"]): st.session_state.meals = []; st.rerun()