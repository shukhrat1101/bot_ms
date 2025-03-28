from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from config import BOT_TOKEN, GROUP_ID

bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

user_state = {}

def is_valid_phone(phone):
    return (phone.startswith('+998') and len(phone) == 13) or \
           (phone.startswith('998') and len(phone) == 12)

def start(update: Update, context):
    user_id = update.message.chat_id
    user_state[user_id] = "WAITING_PHONE"

    contact_button = KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)
    about_button = KeyboardButton("ℹ️ Biz haqimizda")
    markup = ReplyKeyboardMarkup([[contact_button], [about_button]], resize_keyboard=True)

    update.message.reply_text(
        "Xizmat sifatini yaxshilash maqsadida, Iltimos, telefon raqamingizni yuboring:",
        reply_markup=markup
    )

def handle_message(update: Update, context):
    user_id = update.message.chat_id
    state = user_state.get(user_id)
    text = update.message.text

    if text == "ℹ️ Biz haqimizda":
        update.message.reply_text(
            "Assalomu aleykum! Siz Mudofaa sanoati agentligining murojaat botiga tashrif buyurdingiz.\n\n"
            "Ushbu bot orqali Agentlik rahbariyatiga oʻz murojaatingizni yuborishingiz mumkin.\n\n"
            "Murojaatchi toʻgʻrisidagi maʼlumotlar toʻliq sir saqlanadi."
        )
        return

    if update.message.contact:
        phone = update.message.contact.phone_number
        if is_valid_phone(phone):
            user_state[user_id] = "WAITING_APPLICATION"
            context.user_data["phone"] = phone
            update.message.reply_text("✅ Raqam to‘g‘ri! Endi ariza yozing:")
        else:
            update.message.reply_text("❌ Noto‘g‘ri format! Raqam: +998XXXXXXXXX ko‘rinishida bo‘lishi kerak.")
        return

    if state == "WAITING_APPLICATION":
        ariza = text
        phone = context.user_data.get("phone", "Nomaʼlum")
        user = update.message.from_user

        message = (
            f"📩 Yangi ariza:\n"
            f"👤 {user.full_name}\n"
            f"🔗 @{user.username or 'yo‘q'}\n"
            f"📞 {phone}\n"
            f"📝 {ariza}"
        )
        bot.send_message(chat_id=GROUP_ID, text=message)

        update.message.reply_text("✅ Arizangiz muvaffaqiyatli yuborildi!")
        user_state[user_id] = None
    else:
        update.message.reply_text("Iltimos, /start buyrug‘ini yuboring.")


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.contact | Filters.text, handle_message))



# from telegram import Bot, Update, ReplyKeyboardMarkup, KeyboardButton
# from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
# from config import BOT_TOKEN, GROUP_ID
#
# bot = Bot(token=BOT_TOKEN)
# dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
#
# user_state = {}
#
# def is_valid_phone(phone):
#     return (phone.startswith('+998') and len(phone) == 13) or \
#            (phone.startswith('998') and len(phone) == 12)
#
# def start(update: Update, context):
#     user_id = update.message.chat_id
#     user_state[user_id] = "WAITING_PHONE"
#
#     button = KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)
#     markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True)
#
#     update.message.reply_text("Xizmat sifatini yaxshilash maqsadida, Iltimos, telefon raqamingizni yuboring:", reply_markup=markup)
#
# def handle_message(update: Update, context):
#     user_id = update.message.chat_id
#     state = user_state.get(user_id)
#
#     if update.message.contact:
#         phone = update.message.contact.phone_number
#         if is_valid_phone(phone):
#             user_state[user_id] = "WAITING_APPLICATION"
#             context.user_data["phone"] = phone
#             update.message.reply_text("✅ Raqam to‘g‘ri! Endi ariza yozing:")
#         else:
#             update.message.reply_text("❌ Noto‘g‘ri format! Raqam: +998XXXXXXXXX ko‘rinishida bo‘lishi kerak.")
#
#     elif state == "WAITING_APPLICATION":
#         ariza = update.message.text
#         phone = context.user_data.get("phone", "Nomaʼlum")
#         user = update.message.from_user
#
#         text = f"📩 Yangi ariza:\n👤 {user.full_name}\n🔗 @{user.username or 'yo‘q'}\n📞 {phone}\n📝 {ariza}"
#         bot.send_message(chat_id=GROUP_ID, text=text)
#
#         update.message.reply_text("✅ Arizangiz muvaffaqiyatli yuborildi!")
#         user_state[user_id] = None
#
#     else:
#         update.message.reply_text("Iltimos, /start buyrug‘ini yuboring.")
#
# # Handlers
# dispatcher.add_handler(CommandHandler("start", start))
# dispatcher.add_handler(MessageHandler(Filters.contact | Filters.text, handle_message))
