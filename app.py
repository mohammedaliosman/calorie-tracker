import streamlit as st
import pandas as pd
from data import foods  # تأكد أن ملف data.py موجود في نفس المجلد

# إعداد الصفحة
st.set_page_config(page_title="Calorie Tracker", page_icon="🔥", layout="wide")

# --- التصميم الجديد (أسود، أحمر، أبيض) ---
st.markdown("""
<style>
    /* خلفية التطبيق */
    .stApp { background-color: #000000; color: #ffffff; }

    /* تغيير الألوان للعناصر */
    h1, h2, h3 { color: #ff0000 !important; font-weight: bold !important; }

    /* الأزرار باللون الأحمر */
    .stButton > button { background-color: #ff0000 !important; color: #ffffff !important; border: none; font-weight: bold; }

    /* القائمة الجانبية */
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; }

    /* الجدول */
    th { color: #ff0000 !important; }
    td { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# الترجمة
translations = {
    "en": {"title": "Calorie Tracker", "lang_label": "Select Language", "choose": "Choose food:",
           "amount": "Amount (g):", "add": "Add Meal", "meals": "Your Meals", "clear": "Clear All"},
    "ar": {"title": "متتبع السعرات", "lang_label": "اختر اللغة", "choose": "اختر الطعام:", "amount": "الكمية (جرام):",
           "add": "أضف وجبة", "meals": "وجباتك الحالية", "clear": "مسح الكل"}
}

# وضع مبدل اللغة في أعلى القائمة الجانبية ليكون واضحاً
lang = st.sidebar.selectbox("🌐 Language / اللغة", options=["en", "ar"],
                            format_func=lambda x: "English" if x == "en" else "العربية")
t = translations[lang]

# ضبط الاتجاه للعربية
if lang == "ar":
    st.markdown("<style>[data-testid='stAppViewContainer'] { direction: rtl; text-align: right; }</style>",
                unsafe_allow_html=True)

st.title(f"🔥 {t['title']}")

if "meals" not in st.session_state: st.session_state.meals = []

# واجهة الإدخال
col1, col2 = st.columns(2)
with col1: food = st.selectbox(t["choose"], list(foods.keys()))
with col2: grams = st.number_input(t["amount"], min_value=1, value=100)

if st.button(t["add"]):
    cal = (foods[food]["calories"] * grams) / 100
    st.session_state.meals.append({"food": food, "calories": round(cal, 1)})
    st.rerun()

# عرض البيانات (الطريقة القديمة البسيطة)
st.divider()
if st.session_state.meals:
    st.subheader(t["meals"])
    df = pd.DataFrame(st.session_state.meals)
    st.table(df)  # جدول بسيط ومباشر

    if st.button(t["clear"]):
        st.session_state.meals = []
        st.rerun()