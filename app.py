import streamlit as st

# ============================
# Food database
# ============================
foods = {
    "beef (lean)": {"calories": 250, "state": "cooked"},
    "turkey breast": {"calories": 135, "state": "cooked"},
    "lamb": {"calories": 294, "state": "cooked"},
    "duck": {"calories": 337, "state": "cooked"},
    "beef steak": {"calories": 271, "state": "cooked"},
    "lamb liver": {"calories": 139, "state": "cooked"},
    "sausage": {"calories": 301, "state": "cooked"},
    "smoked turkey": {"calories": 104, "state": "cooked"},
    "salmon": {"calories": 208, "state": "cooked"},
    "tilapia": {"calories": 128, "state": "cooked"},
    "shrimp": {"calories": 99, "state": "cooked"},
    "tuna": {"calories": 132, "state": "cooked"},
    "egg": {"calories": 155, "state": "cooked"},
    "tofu": {"calories": 76, "state": "raw"},
    "rice (raw)": {"calories": 365, "state": "raw"},
    "oats (raw)": {"calories": 389, "state": "raw"},
    "quinoa (raw)": {"calories": 368, "state": "raw"},
    "bulgur (raw)": {"calories": 342, "state": "raw"},
    "couscous (raw)": {"calories": 376, "state": "raw"},
    "spaghetti (raw)": {"calories": 371, "state": "raw"},
    "noodles (raw)": {"calories": 138, "state": "raw"},
    "wheat bran": {"calories": 216, "state": "raw"},
    "soya": {"calories": 446, "state": "raw"},
    "rice (cooked)": {"calories": 130, "state": "cooked"},
    "oats (cooked)": {"calories": 68, "state": "cooked"},
    "quinoa (cooked)": {"calories": 120, "state": "cooked"},
    "bulgur (cooked)": {"calories": 83, "state": "cooked"},
    "couscous (cooked)": {"calories": 112, "state": "cooked"},
    "spaghetti (cooked)": {"calories": 158, "state": "cooked"},
    "jareesh (cooked)": {"calories": 95, "state": "cooked"},
    "bread (white)": {"calories": 265, "state": "raw"},
    "bread (brown)": {"calories": 247, "state": "raw"},
    "saj bread": {"calories": 290, "state": "raw"},
    "toast (white)": {"calories": 265, "state": "raw"},
    "croissant": {"calories": 406, "state": "raw"},
    "donut": {"calories": 452, "state": "raw"},
    "crackers": {"calories": 450, "state": "raw"},
    "chapati": {"calories": 410, "state": "raw"},
    "chickpeas (raw)": {"calories": 364, "state": "raw"},
    "lentils (raw)": {"calories": 353, "state": "raw"},
    "white beans (raw)": {"calories": 333, "state": "raw"},
    "red beans (raw)": {"calories": 333, "state": "raw"},
    "lupini beans (raw)": {"calories": 371, "state": "raw"},
    "fava beans (raw)": {"calories": 341, "state": "raw"},
    "chickpeas (cooked)": {"calories": 164, "state": "cooked"},
    "lentils (cooked)": {"calories": 116, "state": "cooked"},
    "white beans (cooked)": {"calories": 139, "state": "cooked"},
    "red beans (cooked)": {"calories": 127, "state": "cooked"},
    "lupini beans (cooked)": {"calories": 119, "state": "cooked"},
    "fava beans (cooked)": {"calories": 110, "state": "cooked"},
    "mixed legumes": {"calories": 140, "state": "cooked"},
    "peas": {"calories": 81, "state": "cooked"},
    "green beans": {"calories": 88, "state": "cooked"},
    "olive oil": {"calories": 884, "state": "raw"},
    "corn oil": {"calories": 884, "state": "raw"},
    "butter": {"calories": 717, "state": "raw"},
    "ghee": {"calories": 900, "state": "raw"},
    "mayonnaise": {"calories": 680, "state": "raw"},
    "tahini": {"calories": 595, "state": "raw"},
    "peanut butter": {"calories": 588, "state": "raw"},
    "avocado": {"calories": 160, "state": "raw"},
    "almonds": {"calories": 579, "state": "raw"},
    "walnuts": {"calories": 654, "state": "raw"},
    "pistachios": {"calories": 562, "state": "raw"},
    "cashews": {"calories": 553, "state": "raw"},
    "hazelnuts": {"calories": 628, "state": "raw"},
    "coconut": {"calories": 354, "state": "raw"},
    "sunflower seeds": {"calories": 584, "state": "raw"},
    "pumpkin seeds": {"calories": 559, "state": "raw"},
    "flaxseeds": {"calories": 534, "state": "raw"},
    "chia seeds": {"calories": 486, "state": "raw"},
    "apple": {"calories": 52, "state": "raw"},
    "banana": {"calories": 89, "state": "raw"},
    "date": {"calories": 277, "state": "raw"},
    "strawberry": {"calories": 32, "state": "raw"},
    "orange": {"calories": 47, "state": "raw"},
    "grapes": {"calories": 69, "state": "raw"},
    "mango": {"calories": 60, "state": "raw"},
    "watermelon": {"calories": 30, "state": "raw"},
    "blackberry": {"calories": 43, "state": "raw"},
    "blueberry": {"calories": 57, "state": "raw"},
    "cherry": {"calories": 50, "state": "raw"},
    "pear": {"calories": 57, "state": "raw"},
    "peach": {"calories": 39, "state": "raw"},
    "apricot": {"calories": 48, "state": "raw"},
    "fig": {"calories": 74, "state": "raw"},
    "dried fig": {"calories": 249, "state": "raw"},
    "raisins": {"calories": 299, "state": "raw"},
    "pineapple": {"calories": 50, "state": "raw"},
    "kiwi": {"calories": 61, "state": "raw"},
    "pomegranate": {"calories": 83, "state": "raw"},
    "lemon": {"calories": 29, "state": "raw"},
    "grapefruit": {"calories": 42, "state": "raw"},
    "broccoli": {"calories": 34, "state": "raw"},
    "cucumber": {"calories": 15, "state": "raw"},
    "tomato": {"calories": 18, "state": "raw"},
    "spinach": {"calories": 23, "state": "raw"},
    "potato (boiled)": {"calories": 87, "state": "cooked"},
    "sweet potato": {"calories": 86, "state": "cooked"},
    "bell pepper": {"calories": 31, "state": "raw"},
    "zucchini": {"calories": 17, "state": "raw"},
    "eggplant": {"calories": 25, "state": "raw"},
    "cauliflower": {"calories": 25, "state": "raw"},
    "cabbage": {"calories": 25, "state": "raw"},
    "lettuce": {"calories": 15, "state": "raw"},
    "arugula": {"calories": 25, "state": "raw"},
    "parsley": {"calories": 36, "state": "raw"},
    "garlic": {"calories": 149, "state": "raw"},
    "onion": {"calories": 40, "state": "raw"},
    "carrot": {"calories": 41, "state": "raw"},
    "mushroom": {"calories": 22, "state": "raw"},
    "radish": {"calories": 16, "state": "raw"},
    "turnip": {"calories": 28, "state": "raw"},
    "beetroot": {"calories": 43, "state": "raw"},
    "okra": {"calories": 33, "state": "raw"},
    "molokhia": {"calories": 35, "state": "raw"},
    "corn": {"calories": 86, "state": "raw"},
    "black olives": {"calories": 115, "state": "raw"},
    "green olives": {"calories": 145, "state": "raw"},
    "milk": {"calories": 61, "state": "raw"},
    "yogurt": {"calories": 59, "state": "raw"},
    "cheese (cheddar)": {"calories": 403, "state": "raw"},
    "cheese (feta)": {"calories": 264, "state": "raw"},
    "cheese (mozzarella)": {"calories": 280, "state": "raw"},
    "cheese (cottage)": {"calories": 98, "state": "raw"},
    "labneh": {"calories": 154, "state": "raw"},
    "cream": {"calories": 245, "state": "raw"},
    "condensed milk": {"calories": 322, "state": "raw"},
    "cooking cream": {"calories": 195, "state": "raw"},
    "ice cream (vanilla)": {"calories": 207, "state": "raw"},
    "almond milk": {"calories": 15, "state": "raw"},
    "soy milk": {"calories": 33, "state": "raw"},
    "honey": {"calories": 304, "state": "raw"},
    "white sugar": {"calories": 387, "state": "raw"},
    "jam": {"calories": 250, "state": "raw"},
    "date molasses": {"calories": 290, "state": "raw"},
    "dark chocolate": {"calories": 546, "state": "raw"},
    "cocoa powder": {"calories": 228, "state": "raw"},
    "plain cake": {"calories": 297, "state": "raw"},
    "ketchup": {"calories": 112, "state": "raw"},
    "mustard": {"calories": 66, "state": "raw"},
    "vinegar": {"calories": 18, "state": "raw"},
    "tomato sauce": {"calories": 82, "state": "raw"},
    "chicken stock cube": {"calories": 198, "state": "raw"},
    "potato chips": {"calories": 536, "state": "raw"},
    "popcorn (no oil)": {"calories": 387, "state": "raw"},
}

# ============================
# إعداد الصفحة
# ============================
st.set_page_config(page_title="Calorie Tracker", page_icon="🏋️", layout="wide")

# ============================
# CSS
# ============================
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

# ============================
# Translations
# ============================
translations = {
    "en": {
        "title": "🏋️ Calorie Tracker", "settings": "⚙️ Settings", "daily_goal": "Daily calorie goal (kcal):",
        "filter_foods": "🔍 Filter Foods", "show_foods": "Show foods:", "all": "All",
        "raw_only": "Raw only", "cooked_only": "Cooked only", "add_meal": "🍽️ Add a Meal",
        "choose_food": "Choose a food:", "amount": "Amount (grams):", "per_100g": "Per 100g",
        "add_button": "➕ Add Meal", "added_msg": "✅ Added", "today_meals": "📋 Today's Meals",
        "food": "Food", "grams": "Grams", "calories": "Calories", "state": "State",
        "raw": "🟤 Raw", "cooked": "🟢 Cooked", "total": "🔥 Total", "goal": "🎯 Goal",
        "remaining": "✅ Remaining", "exceeded": "⚠️ Exceeded", "clear": "🗑️ Clear All Meals",
        "no_meals": "No meals added yet.", "view_foods": "🥗 View All Available Foods",
        "search": "🔍 Search for a food:", "ai_coming": "🤖 AI Assistant — Coming Soon!",
    },
    "ar": {
        "title": "🏋️ تتبع السعرات الحرارية", "settings": "⚙️ الإعدادات", "daily_goal": "هدفك اليومي (kcal):",
        "filter_foods": "🔍 تصفية الأطعمة", "show_foods": "عرض الأطعمة:", "all": "الكل",
        "raw_only": "نيئة فقط", "cooked_only": "مطبوخة فقط", "add_meal": "🍽️ إضافة وجبة",
        "choose_food": "اختر طعاماً:", "amount": "الكمية (جرام):", "per_100g": "لكل 100 جرام",
        "add_button": "➕ إضافة وجبة", "added_msg": "✅ تمت الإضافة", "today_meals": "📋 وجبات اليوم",
        "food": "الطعام", "grams": "الجرام", "calories": "السعرات", "state": "الحالة",
        "raw": "🟤 نيئ", "cooked": "🟢 مطبوخ", "total": "🔥 المجموع", "goal": "🎯 الهدف",
        "remaining": "✅ المتبقي", "exceeded": "⚠️ تجاوزت الهدف", "clear": "🗑️ مسح كل الوجبات",
        "no_meals": "لم تضف وجبات بعد.", "view_foods": "🥗 عرض كل الأطعمة المتاحة",
        "search": "🔍 ابحث عن طعام:", "ai_coming": "🤖 المساعد الذكي — قريباً!",
    }
}

# Language selection
st.sidebar.markdown("## 🌍 Language / اللغة")
lang = st.sidebar.selectbox("Language", options=["en", "ar"], label_visibility="collapsed",
                            format_func=lambda x: "English 🇬🇧" if x == "en" else "العربية 🇸🇦")
t = translations[lang]

if lang == "ar":
    st.markdown("<style>.stApp { direction: rtl; text-align: right; }</style>", unsafe_allow_html=True)

# Sidebar
daily_goal = st.sidebar.number_input(t["daily_goal"], min_value=500, max_value=5000, value=2000)
state_filter = st.sidebar.radio(t["show_foods"], options=["all", "raw", "cooked"],
                                format_func=lambda x: t["all"] if x == "all" else (
                                    t["raw_only"] if x == "raw" else t["cooked_only"]))

# Main Logic
st.title(t["title"])
if "meals" not in st.session_state: st.session_state.meals = []


# Filtering logic
def get_filtered_foods(filter_key):
    if filter_key == "raw": return {k: v for k, v in foods.items() if v["state"] == "raw"}
    if filter_key == "cooked": return {k: v for k, v in foods.items() if v["state"] == "cooked"}
    return foods


filtered_foods = get_filtered_foods(state_filter)

# Add Meal
st.subheader(t["add_meal"])
col1, col2, col3 = st.columns(3)
with col1: food = st.selectbox(t["choose_food"], list(filtered_foods.keys()))
with col2: grams = st.number_input(t["amount"], min_value=1, value=100)
with col3:
    if food:
        food_info = foods[food]
        st.metric(label=f"{t['per_100g']} ({food_info['state']})", value=f"{food_info['calories']} kcal")

if st.button(t["add_button"], use_container_width=True):
    cal = (foods[food]["calories"] * grams) / 100
    st.session_state.meals.append(
        {"food": food, "grams": grams, "calories": round(cal, 1), "state": foods[food]["state"]})
    st.success(f"{t['added_msg']} {food}")

# Display Meals
st.divider()
st.subheader(t["today_meals"])
if st.session_state.meals:
    total = 0
    for i, meal in enumerate(st.session_state.meals):
        st.write(f"🍴 {meal['food']} | {meal['grams']}g | {meal['calories']} kcal | ({t[meal['state']]})")
        total += meal['calories']

    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric(t["total"], f"{round(total)} kcal")
    col2.metric(t["goal"], f"{daily_goal} kcal")
    rem = daily_goal - total
    col3.metric(t["remaining"] if rem >= 0 else t["exceeded"], f"{round(abs(rem))} kcal")

    if st.button(t["clear"]): st.session_state.meals = []; st.rerun()
else:
    st.info(t["no_meals"])

# View Foods
with st.expander(t["view_foods"]):
    search = st.text_input(t["search"])
    for k, v in foods.items():
        if search.lower() in k.lower(): st.write(
            f"{'🟤' if v['state'] == 'raw' else '🟢'} **{k}** → {v['calories']} kcal/100g")