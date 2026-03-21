import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- سيرفر الإيهام لـ Render المجاني ---
app = Flask('')
@app.route('/')
def home(): return "المنصة التعليمية تعمل بنجاح!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- إعداد البوت بالتوكن الخاص بك ---
API_TOKEN = '8728241420:AAF6rmQfHyLRBJx-CfyBf44ol3F4atSOZXg'
bot = telebot.TeleBot(API_TOKEN)

# --- قاعدة البيانات ---
DATA_BASE = {
    "💊 قسم الصيدلة": {
        "الترم الأول": {
            "📚 القسم النظري": {
                "🧪 كيمياء عقاقير": {"المستند الأول": ["ت 1"], "المستند الثاني": ["ت 2"], "المستند الثالث": ["ت 3"], "المستند الرابع": ["ت 4"]},
                "💉 علم الأمراض": {"المستند 1": [], "المستند 2": [], "المستند 3": [], "المستند 4": [], "المستند 5": [], "المستند 6": [], "المستند 7": [], "المستند 8": [], "المستند 9": []},
                "💊 مهارات مهنية": {"المستند 1": [], "المستند 2": [], "المستند 3": [], "المستند 4": [], "المستند 5": []},
                "🧬 تحليل آلي نظري": {"المستند 1": [], "المستند 2": [], "المستند 3": []},
                "💊 كيمياء صيدلانية": {"المستند 1": [], "المستند 2": [], "المستند 3": [], "المستند 4": []},
                "💊 علم أدوية": {"المستند 1": [], "المستند 2": []},
                "🔬 أحياء دقيقة نظري": {f"المستند {i}": [] for i in range(1, 9)},
                "🧪 تقنية صيدلانية نظري": {"المستند 1": [], "المستند 2": [], "المستند 3": []}
            },
            "🛠️ القسم العملي": {
                "💊 تقنية صيدلانية عملي": {f"المستند {i}": [] for i in range(1, 6)},
                "🔬 أحياء دقيقة عملي": {"المستند الوحيد": []},
                "🧬 تحليل آلي عملي": {f"المستند {i}": [] for i in range(1, 7)}
            }
        },
        "الترم الثاني": {}, "الترم الثالث": {}, "الترم الرابع": {}, "الترم الخامس": {}, "الترم السادس": {}
    },
    "🩺 قسم مساعد طبيب": {}, "🦷 قسم طب الأسنان": {}, "🤱 قسم القبالة": {}
}

# --- إدارة التنقل ---
user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(dept) for dept in DATA_BASE.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "مرحباً بك دكتور محمد!\nاختر القسم الدراسي:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in DATA_BASE.keys())
def handle_dept(message):
    dept = message.text
    if not DATA_BASE[dept]:
        bot.reply_to(message, f"قسم {dept} قيد التجهيز حالياً...")
        return
    user_state[message.chat.id] = {'dept': dept}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    semesters = ["الترم الأول", "الترم الثاني", "الترم الثالث", "الترم الرابع", "الترم الخامس", "الترم السادس"]
    markup.add(*[types.KeyboardButton(s) for s in semesters], "⬅️ العودة للرئيسية")
    bot.send_message(message.chat.id, "اختر الترم:", reply_markup=markup)

@bot.message_handler(func=lambda m: "الترم" in m.text)
def handle_semester(message):
    chat_id = message.chat.id
    if chat_id not in user_state: return start(message)
    user_state[chat_id]['semester'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 القسم النظري", "🛠️ القسم العملي", "⬅️ العودة للرئيسية")
    bot.send_message(chat_id, "اختر النوع:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["📚 القسم النظري", "🛠️ القسم العملي"])
def handle_type(message):
    chat_id = message.chat.id
    if chat_id not in user_state: return start(message)
    m_type = message.text
    user_state[chat_id]['type'] = m_type
    dept = user_state[chat_id]['dept']
    sem = user_state[chat_id]['semester']
    
    subjects = DATA_BASE[dept][sem][m_type]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # قائمة المواد مع الإيموجيات كما في صورتك
    subject_buttons = {
        "كيمياء عقاقير": "🧪 كيمياء عقاقير",
        "علم الأمراض": "💉 علم الأمراض",
        "مهارات مهنية": "💊 مهارات مهنية",
        "تحليل آلي نظري": "🧬 تحليل آلي نظري",
        "كيمياء صيدلانية": "💊 كيمياء صيدلانية",
        "علم أدوية": "💊 علم أدوية",
        "أحياء دقيقة نظري": "🔬 أحياء دقيقة نظري",
        "تقنية صيدلانية نظري": "🧪 تقنية صيدلانية نظري"
    }

    buttons = []
    for sub in subjects.keys():
        # تنظيف اسم المادة من الإيموجي للبحث عنه في القائمة
        clean_name = sub.replace("🧪 ", "").replace("💉 ", "").replace("💊 ", "").replace("🧬 ", "").replace("🔬 ", "").strip()
        display = subject_buttons.get(clean_name, sub)
        buttons.append(types.KeyboardButton(display))
    
    markup.add(*buttons, "⬅️ العودة للرئيسية")
    bot.send_message(chat_id, f"مواد {m_type}:", reply_markup=markup)

@bot.message_handler(func=lambda m: any(word in m.text for word in ["كيمياء", "علم", "أحياء", "مهارات", "تحليل", "تقنية"]))
def handle_subject_click(message):
    chat_id = message.chat.id
    if chat_id not in user_state or 'type' not in user_state[chat_id]: return start(message)

    text = message.text
    dept = user_state[chat_id]['dept']
    sem = user_state[chat_id]['semester']
    m_type = user_state[chat_id]['type']
    
    # البحث عن المادة بمطابقة جزئية لتفادي مشكلة الإيموجي
    found_sub = None
    for sub_name in DATA_BASE[dept][sem][m_type].keys():
        clean_sub = sub_name.replace("🧪 ", "").replace("💉 ", "").replace("💊 ", "").replace("🧬 ", "").replace("🔬 ", "").strip()
        if clean_sub in text:
            found_sub = sub_name
            break
    
    if found_sub:
        docs = DATA_BASE[dept][sem][m_type][found_sub]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if not docs:
            bot.reply_to(message, f"⏳ جاري رفع محاضرات {found_sub}...")
            return
        for doc in docs.keys():
            markup.add(f"📄 {found_sub} - {doc}")
        markup.add("⬅️ العودة للرئيسية")
        bot.send_message(chat_id, f"محاضرات {found_sub}:", reply_markup=markup)
    else:
        bot.reply_to(message, "⏳ القسم قيد التحديث...")

@bot.message_handler(func=lambda m: m.text == "⬅️ العودة للرئيسية")
def go_home(message): start(message)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
