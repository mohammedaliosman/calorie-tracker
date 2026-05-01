import streamlit as st
import pandas as pd
import plotly.express as px
from data import foods

st.set_page_config(page_title="Calorie Tracker", page_icon="🍎", layout="centered")

# --- CSS للتجميل ---
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    .main-card { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    h1 { color: #ff4b4b; text-align: center; font-family: 'Arial'; }
    .stButton > button { border-radius: 50px; background-color: #ff4b4b; color: white; border: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🍎 رفيق السعرات الذكي")

# إعداد الهدف اليومي
goal = st.sidebar.number_input("🎯 حدد هدفك اليومي (سعرة):", min_value=500, value=2000, step=100)

if "meals" not in st.session_state: st.session_state.meals = []

# واجهة إضافة الوجبات
col1, col2 = st.columns(2)
with col1: food = st.selectbox("اختر ما أكلته:", list(foods.keys()))
with col2: grams = st.number_input("الكمية (جرام):", min_value=1, value=100)

if st.button("➕ أضف للوجبات"):
    cal = (foods[food]["calories"] * grams) / 100
    st.session_state.meals.append({"food": food, "calories": round(cal, 1)})
    st.rerun()

# عرض البيانات بشكل حيوي
if st.session_state.meals:
    df = pd.DataFrame(st.session_state.meals)
    total_calories = df['calories'].sum()

    # 1. شريط التقدم (بصري ومفهوم للجميع)
    progress = min(total_calories / goal, 1.0)
    st.write(f"### لقد استهلكت {total_calories} من {goal} سعرة")
    st.progress(progress)

    if total_calories >= goal:
        st.balloons()  # احتفال!
        st.success("🎉 أحسنت! لقد وصلت لهدفك اليوم!")

    # 2. رسم بياني "دونات" (سهل وممتع)
    fig = px.pie(df, values='calories', names='food', hole=0.6,
                 title="توزيع السعرات في وجباتك",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    if st.button("🗑️ ابدأ يوم جديد"):
        st.session_state.meals = []
        st.rerun()