import telebot
from telebot import types

bot = telebot.TeleBot("8728241420:AAF6rmQfHyLRBJx-CfyBf44ol3F4atSOZXg")

# 🔹 عدّل هذا فقط لإضافة/حذف المحتوى
DATA = {
    "السنة الأولى": {
        "الترم الأول": {
            "كيمياء": {
                "محاضرة 1": {"pdf": "قريباً", "audio": "قريباً"},
                "محاضرة 2": {"pdf": "قريباً", "audio": "قريباً"}
            },
            "أحياء": {
                "محاضرة 1": {"pdf": "قريباً", "audio": "قريباً"}
            }
        }
    },
    "السنة الثانية": {
        "الترم الأول": {
            "فيزياء": {
                "محاضرة 1": {"pdf": "قريباً", "audio": "قريباً"}
            }
        }
    }
}

# 🔹 لتتبع حالة كل مستخدم
user_state = {}

# 🔹 إنشاء أزرار مع زر رجوع
def make_buttons(options, back=False):
    markup = types.InlineKeyboardMarkup()
    for item in options:
        markup.add(types.InlineKeyboardButton(item, callback_data=item))
    if back:
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back"))
    return markup

# 🔹 البداية
@bot.message_handler(commands=['start'])
def start(message):
    user_state[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "📚 اختر السنة الدراسية:",
        reply_markup=make_buttons(DATA.keys())
    )

# 🔹 التحكم في التنقل
@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    uid = call.message.chat.id
    state = user_state.setdefault(uid, {})

    # 🔙 الرجوع
    if call.data == "back":
        if "type" in state:
            state.pop("type")
            bot.send_message(uid, "اختر المحاضرة:",
                reply_markup=make_buttons(
                    DATA[state["year"]][state["term"]][state["subject"]].keys(),
                    back=True
                ))
        elif "lecture" in state:
            state.pop("lecture")
            bot.send_message(uid, "اختر المادة:",
                reply_markup=make_buttons(
                    DATA[state["year"]][state["term"]].keys(),
                    back=True
                ))
        elif "subject" in state:
            state.pop("subject")
            bot.send_message(uid, "اختر الترم:",
                reply_markup=make_buttons(
                    DATA[state["year"]].keys(),
                    back=True
                ))
        elif "term" in state:
            state.pop("term")
            bot.send_message(uid, "اختر السنة:",
                reply_markup=make_buttons(DATA.keys())
            )
        return

    # 🔽 التنقل للأمام
    if "year" not in state:
        state["year"] = call.data
        bot.send_message(uid, "📘 اختر الترم:",
            reply_markup=make_buttons(DATA[state["year"]].keys(), back=True))

    elif "term" not in state:
        state["term"] = call.data
        bot.send_message(uid, "📗 اختر المادة:",
            reply_markup=make_buttons(DATA[state["year"]][state["term"]].keys(), back=True))

    elif "subject" not in state:
        state["subject"] = call.data
        bot.send_message(uid, "📖 اختر المحاضرة:",
            reply_markup=make_buttons(DATA[state["year"]][state["term"]][state["subject"]].keys(), back=True))

    elif "lecture" not in state:
        state["lecture"] = call.data
        bot.send_message(uid, "📂 اختر نوع الملف:",
            reply_markup=make_buttons(["📄 PDF", "🎧 Audio"], back=True))

    else:
        lecture = DATA[state["year"]][state["term"]][state["subject"]][state["lecture"]]

        if call.data == "📄 PDF":
            bot.send_message(uid, lecture["pdf"])
        elif call.data == "🎧 Audio":
            bot.send_message(uid, lecture["audio"])

bot.polling()
