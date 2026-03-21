import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- إعداد سيرفر وهمي لتجنب إغلاق Render المجاني ---
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل بنجاح!"

def run():
    # Render يرسل المنفذ تلقائياً عبر متغير البيئة PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- إعداد البوت ---
API_TOKEN = '8728241420:AAF6rmQfHyLRBJx-CfyBf44ol3F4atSOZXg' # ضع التوكن هنا
bot = telebot.TeleBot(API_TOKEN)

# --- قاعدة بيانات المواد والمستندات ---
COURSES = {
    "📚 القسم النظري": {
        "🧪 كيمياء عقاقير": {
            "المستند الأول": ["التسجيل الأول"],
            "المستند الثاني": ["التسجيل الثاني"],
            "المستند الثالث": ["التسجيل الثالث", "التسجيل الرابع"],
            "المستند الرابع": ["التسجيل الخامس"]
        },
        "💉 علم الأمراض": {
            "المستند الأول": [],
            "المستند الثاني": ["التسجيل الثاني"],
            "المستند الثالث": ["التسجيل الثالث"],
            "المستند الرابع": ["التسجيل الرابع", "التسجيل الخامس"],
            "المستند الخامس": ["التسجيل السادس", "التسجيل السابع", "التسجيل الثامن"],
            "المستند السادس": ["التسجيل التاسع"],
            "المستند السابع": ["التسجيل العاشر"],
            "المستند الثامن": ["التسجيل الحادي عشر"],
            "المستند التاسع": ["التسجيل الثاني عشر"]
        },
        "💊 مهارات مهنية": {
            "المستند الأول": ["التسجيل الأول"],
            "المستند الثاني": ["التسجيل الثاني"],
            "المستند الثالث": ["التسجيل الثالث"],
            "المستند الرابع": ["التسجيل الرابع"],
            "المستند الخامس": ["التسجيل الخامس"]
        },
        "🧬 تحليل آلي نظري": {
            "المستند الأول": [],
            "المستند الثاني": ["التسجيل الأول", "التسجيل الثاني", "التسجيل الثالث", "التسجيل الرابع", "التسجيل الخامس"],
            "المستند الثالث": []
        },
        "💊 كيمياء صيدلانية": {
            "المستند الأول": [],
            "المستند الثاني": ["التسجيل الثاني", "التسجيل الثالث"],
            "المستند الثالث": ["التسجيل الرابع", "التسجيل الخامس", "التسجيل السادس"],
            "المستند الرابع": ["التسجيل السابع", "التسجيل الثامن", "التسجيل التاسع"]
        },
        "💊 علم أدوية": {
            "المستند الأول": ["التسجيل الأول", "التسجيل الثاني", "التسجيل الثالث", "التسجيل الرابع", "التسجيل الخامس"],
            "المستند الثاني": ["التسجيل السادس", "التسجيل السابع", "التسجيل الثامن", "التسجيل التاسع", "التسجيل العاشر", "التسجيل الحادي عشر"]
        },
        "🔬 أحياء دقيقة نظري": {
            "المستند الأول": ["التسجيل الأول"], "المستند الثاني": ["التسجيل الثاني"],
            "المستند الثالث": [], "المستند الرابع": [], "المستند الخامس": [], 
            "المستند السادس": [], "المستند السابع": [], "المستند الثامن": []
        },
        "🧪 تقنية صيدلانية نظري": {
            "المستند الأول": ["التسجيل الأول", "التسجيل الثاني"],
            "المستند الثاني": ["التسجيل الثالث", "التسجيل الرابع"],
            "المستند الثالث": ["التسجيل الخامس"]
        }
    },
    "🛠️ القسم العملي": {
        "💊 تقنية صيدلانية عملي": {f"المستند {i}": [] for i in range(1, 6)},
        "🔬 أحياء دقيقة عملي": {"المستند الوحيد": []},
        "🧬 تحليل آلي عملي": {f"المستند {i}": [] for i in range(1, 7)}
    }
}

# --- لوحة التحكم والردود ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 القسم النظري", "🛠️ القسم العملي")
    bot.reply_to(message, "مرحباً بك دكتور محمد! اختر القسم المطلوب للوصول للمحاضرات:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in COURSES.keys())
def show_subjects(message):
    section = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    subjects = list(COURSES[section].keys())
    markup.add(*[types.KeyboardButton(s) for s in subjects])
    markup.add("⬅️ عودة")
    bot.send_message(message.chat.id, f"مواد {section}:", reply_markup=markup)

@bot.message_handler(func=lambda m: any(m.text in COURSES[sec] for sec in COURSES))
def show_docs(message):
    subject = message.text
    section = "📚 القسم النظري" if subject in COURSES["📚 القسم النظري"] else "🛠️ القسم العملي"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for doc in COURSES[section][subject].keys():
        markup.add(f"📄 {subject} - {doc}")
    markup.add("⬅️ عودة")
    bot.send_message(message.chat.id, f"محاضرات {subject}:", reply_markup=markup)

@bot.message_handler(func=lambda m: "📄" in m.text)
def handle_file_request(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, "⏳ هذا الملف سيتم رفعه قريباً من قبل الإدارة. ترقبوا التحديث!")

@bot.message_handler(func=lambda m: m.text == "⬅️ عودة")
def back(message):
    send_welcome(message)

# --- تشغيل البوت مع السيرفر ---
if __name__ == "__main__":
    keep_alive() # تشغيل Flask في الخلفية
    print("البوت يعمل الآن...")
    bot.infinity_polling()
