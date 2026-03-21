import telebot
from telebot import types

# ضع التوكن الخاص بك هنا
API_TOKEN = '8728241420:AAF6rmQfHyLRBJx-CfyBf44ol3F4atSOZXg'
bot = telebot.TeleBot(API_TOKEN)

# --- قاعدة بيانات المواد والمستندات ---
# ملاحظة: يمكنك إضافة أو تعديل التسجيلات بسهولة هنا
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
            "المستند الأول": ["التسجيل الأول"],
            "المستند الثاني": ["التسجيل الثاني"],
            "المستند الثالث": [], "المستند الرابع": [], "المستند الخامس": [], "المستند السادس": [], "المستند السابع": [], "المستند الثامن": []
        },
        "🧪 تقنية صيدلانية نظري": {
            "المستند الأول": ["التسجيل الأول", "التسجيل الثاني"],
            "المستند الثاني": ["التسجيل الثالث", "التسجيل الرابع"],
            "المستند الثالث": ["التسجيل الخامس"]
        }
    },
    "🛠️ القسم العملي": {
        "💊 تقنية صيدلانية عملي": {f"المستند {i}": [] for i in range(1, 6)},
        "🔬 أحياء دقيقة عملي": {"المستند": []},
        "🧬 تحليل آلي عملي": {f"المستند {i}": [] for i in range(1, 7)}
    }
}

# --- لوحة التحكم والردود ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("📚 القسم النظري")
    item2 = types.KeyboardButton("🛠️ القسم العملي")
    markup.add(item1, item2)
    bot.reply_to(message, "أهلاً بك يا دكتور! اختر القسم المطلوب:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in COURSES.keys())
def show_subjects(message):
    section = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in COURSES[section].keys():
        markup.add(types.KeyboardButton(subject))
    markup.add(types.KeyboardButton("⬅️ العودة للقائمة الرئيسية"))
    bot.send_message(message.chat.id, f"اختر المادة من {section}:", reply_markup=markup)

@bot.message_handler(func=lambda message: any(message.text in subjects for subjects in [COURSES[s].keys() for s in COURSES]))
def show_documents(message):
    subject_name = message.text
    # البحث عن القسم الذي تنتمي له المادة
    section = "📚 القسم النظري" if subject_name in COURSES["📚 القسم النظري"] else "🛠️ القسم العملي"
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for doc in COURSES[section][subject_name].keys():
        markup.add(types.KeyboardButton(f"{subject_name} - {doc}"))
    markup.add(types.KeyboardButton("⬅️ العودة للقائمة الرئيسية"))
    bot.send_message(message.chat.id, f"اختر المحاضرة (المستند):", reply_markup=markup)

@bot.message_handler(func=lambda message: " - المستند" in message.text or " - المستند" in message.text)
def deliver_files(message):
    # هذه الدالة ستنفذ عند اختيار مستند معين
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, "⏳ جارٍ تجهيز الملفات من قبل الإدارة، ستكون متاحة هنا فور رفعها. شكراً لصبرك!")

@bot.message_handler(func=lambda message: message.text == "⬅️ العودة للقائمة الرئيسية")
def back_home(message):
    send_welcome(message)

# تشغيل البوت
if __name__ == "__main__":
    print("البوت يعمل الآن...")
    bot.infinity_polling()
