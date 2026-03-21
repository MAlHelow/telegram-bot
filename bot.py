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

# --- قاعدة البيانات (الهيكل الشامل) ---
DATA_BASE = {
    "💊 قسم الصيدلة": {
        "الترم الأول": {
            "📚 القسم النظري": {
                "🧪 كيمياء عقاقير": {"المستند الأول": ["التسجيل الأول"], "المستند الثاني": ["التسجيل الثاني"], "المستند الثالث": ["التسجيل الثالث", "التسجيل الرابع"], "المستند الرابع": ["التسجيل الخامس"]},
                "💉 علم الأمراض": {"المستند الأول": [], "المستند الثاني": ["التسجيل الثاني"], "المستند الثالث": ["التسجيل الثالث"], "المستند الرابع": ["التسجيل الرابع", "التسجيل الخامس"], "المستند الخامس": ["التسجيل السادس", "التسجيل السابع", "التسجيل الثامن"], "المستند السادس": ["التسجيل التاسع"], "المستند السابع": ["التسجيل العاشر"], "المستند الثامن": ["التسجيل الحادي عشر"], "المستند التاسع": ["التسجيل الثاني عشر"]},
                "💊 مهارات مهنية": {"المستند الأول": ["التسجيل الأول"], "المستند الثاني": ["التسجيل الثاني"], "المستند الثالث": ["التسجيل الثالث"], "المستند الرابع": ["التسجيل الرابع"], "المستند الخامس": ["التسجيل الخامس"]},
                "🧬 تحليل آلي نظري": {"المستند الأول": [], "المستند الثاني": ["التسجيل الأول", "التسجيل الثاني", "التسجيل الثالث", "التسجيل الرابع", "التسجيل الخامس"], "المستند الثالث": []},
                "💊 كيمياء صيدلانية": {"المستند الأول": [], "المستند الثاني": ["التسجيل الثاني", "التسجيل الثالث"], "المستند الثالث": ["التسجيل الرابع", "التسجيل الخامس", "التسجيل السادس"], "المستند الرابع": ["التسجيل السابع", "التسجيل الثامن", "التسجيل التاسع"]},
                "💊 علم أدوية": {"المستند الأول": ["ت 1", "ت 2", "ت 3", "ت 4", "ت 5"], "المستند الثاني": ["ت 6", "ت 7", "ت 8", "ت 9", "ت 10", "ت 11"]},
                "🔬 أحياء دقيقة نظري": {f"المستند {i}": [] for i in range(1, 9)},
                "🧪 تقنية صيدلانية نظري": {"المستند الأول": ["ت 1", "ت 2"], "المستند الثاني": ["ت 3", "ت 4"], "المستند الثالث": ["ت 5"]}
            },
            "🛠️ القسم العملي": {
                "💊 تقنية صيدلانية عملي": {f"المستند {i}": [] for i in range(1, 6)},
                "🔬 أحياء دقيقة عملي": {"المستند الوحيد": []},
                "🧬 تحليل آلي عملي": {f"المستند {i}": [] for i in range(1, 7)}
            }
        },
        "الترم الثاني": {}, "الترم الثالث": {}, "الترم الرابع": {}, "الترم الخامس": {}, "الترم السادس": {}
    },
    "🩺 قسم مساعد طبيب": {},
    "🦷 قسم طب الأسنان": {},
    "🤱 قسم القبالة": {}
}

# --- إدارة الأزرار والردود ---
user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(dept) for dept in DATA_BASE.keys()]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "مرحباً بك دكتور محمد في المنصة التعليمية!\nاختر القسم الدراسي:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in DATA_BASE.keys())
def handle_dept(message):
    dept = message.text
    if not DATA_BASE[dept]:
        bot.reply_to(message, f"قسم {dept} قيد التجهيز حالياً. سيتم تفعيله قريباً بالتعاون مع مندوبي الدفعة!")
        return
    
    user_state[message.chat.id] = {'dept': dept}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    semesters = ["الترم الأول", "الترم الثاني", "الترم الثالث", "الترم الرابع", "الترم الخامس", "الترم السادس"]
    markup.add(*[types.KeyboardButton(s) for s in semesters], "⬅️ العودة للرئيسية")
    bot.send_message(message.chat.id, f"تم اختيار {dept}. اختر الترم:", reply_markup=markup)

@bot.message_handler(func=lambda m: "الترم" in m.text)
def handle_semester(message):
    chat_id = message.chat.id
    if chat_id not in user_state: return start(message)
    
    semester = message.text
    dept = user_state[chat_id]['dept']
    
    if semester not in DATA_BASE[dept] or not DATA_BASE[dept][semester]:
        bot.reply_to(message, f"بيانات {semester} لقسم {dept} لم ترفع بعد.")
        return

    user_state[chat_id]['semester'] = semester
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 القسم النظري", "🛠️ القسم العملي", "⬅️ العودة للرئيسية")
    bot.send_message(message.chat.id, "اختر النوع:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["📚 القسم النظري", "🛠️ القسم العملي"])
def handle_type(message):
    chat_id = message.chat.id
    if chat_id not in user_state: return start(message)
    
    m_type = message.text
    dept = user_state[chat_id]['dept']
    sem = user_state[chat_id]['semester']
    
    subjects = DATA_BASE[dept][sem][m_type]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*[types.KeyboardButton(sub) for sub in subjects.keys()], "⬅️ العودة للرئيسية")
    bot.send_message(message.chat.id, f"مواد {m_type}:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "⬅️ العودة للرئيسية")
def go_home(message): start(message)

@bot.message_handler(func=lambda m: True)
def last_step(message):
    # رسالة ذكية تظهر عند الضغط على اسم المادة
    if any(sub in message.text for sub in ["كيمياء", "علم", "أحياء", "مهارات", "تحليل", "تقنية"]):
        bot.reply_to(message, f"⏳ جاري رفع مستندات وتسجيلات '{message.text}'. ستكون متاحة هنا فور اكتمال الرفع!")
    else:
        bot.send_message(message.chat.id, "يرجى استخدام الأزرار للتنقل.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
