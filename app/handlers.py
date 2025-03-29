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
#     if update.message.chat.type != 'private':
#         return
#
#     user_id = update.message.chat_id
#     user_state[user_id] = "WAITING_PHONE"
#
#     buttons = [
#         [KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)],
#         [KeyboardButton("ℹ️ Biz haqimizda")]
#     ]
#     markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
#
#     update.message.reply_text(
#         "Xizmat sifatini yaxshilash maqsadida telefon raqamingizni yuboring:",
#         reply_markup=markup
#     )
#
# def about_us(update: Update, context):
#     if update.message.chat.type != 'private':
#         return
#
#     update.message.reply_text(
#         "📢 *Biz haqimizda*\n\n"
#         "Assalomu alaykum! Siz Mudofaa sanoati agentligining murojaat botiga tashrif buyurdingiz.\n"
#         "Ushbu bot orqali agentlik rahbariyatiga oʻz murojaatingizni yuborishingiz mumkin.\n"
#         "Murojaatchi toʻgʻrisidagi maʼlumotlar toʻliq sir saqlanadi.",
#         parse_mode="Markdown"
#     )
#
# def handle_message(update: Update, context):
#     if update.message.chat.type != 'private':
#         return
#
#     user_id = update.message.chat_id
#     state = user_state.get(user_id)
#
#     if update.message.text == "ℹ️ Biz haqimizda":
#         return about_us(update, context)
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
#         text = f"📩 *Yangi ariza:*\n👤 {user.full_name}\n🔗 @{user.username or 'yo‘q'}\n📞 {phone}\n📝 {ariza}"
#         bot.send_message(chat_id=GROUP_ID, text=text, parse_mode="Markdown")
#
#         update.message.reply_text("✅ Arizangiz muvaffaqiyatli yuborildi!")
#         user_state[user_id] = None
#
#     else:
#         update.message.reply_text("Iltimos, /start buyrug‘ini yuboring.")
#
# dispatcher.add_handler(CommandHandler("start", start))
# dispatcher.add_handler(CommandHandler("about", about_us))
# dispatcher.add_handler(MessageHandler(Filters.private & (Filters.contact | Filters.text), handle_message))

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
    if update.message.chat.type != 'private':
        return

    user_id = update.message.chat_id
    user_state[user_id] = "WAITING_PHONE"

    buttons = [
        [KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)],
        [KeyboardButton("ℹ️ Biz haqimizda")]
    ]
    markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    update.message.reply_text(
        "Xizmat sifatini yaxshilash maqsadida telefon raqamingizni yuboring:",
        reply_markup=markup
    )

def about_us(update: Update, context):
    if update.message.chat.type != 'private':
        return

    update.message.reply_text(
        "📢 *Biz haqimizda*\n\n"
        "Assalomu alaykum! Siz Mudofaa sanoati agentligining murojaat botiga tashrif buyurdingiz.\n"
        "Ushbu bot orqali agentlik rahbariyatiga oʻz murojaatingizni yuborishingiz mumkin.\n"
        "Murojaatchi toʻgʻrisidagi maʼlumotlar toʻliq sir saqlanadi.",
        parse_mode="Markdown"
    )

def handle_message(update: Update, context):
    if update.message.chat.type != 'private':
        return

    user_id = update.message.chat_id
    user = update.message.from_user
    state = user_state.get(user_id)

    # Telefon yuborilgan
    if update.message.contact:
        phone = update.message.contact.phone_number
        if is_valid_phone(phone):
            context.user_data["phone"] = phone
            user_state[user_id] = "WAITING_APPLICATION"
            update.message.reply_text("✅ Raqam to‘g‘ri! Endi ariza yozing:")
        else:
            update.message.reply_text("❌ Noto‘g‘ri format! Raqam: +998XXXXXXXXX ko‘rinishida bo‘lishi kerak.")
        return

    # "Biz haqimizda" tugmasi bosilgan
    if update.message.text == "ℹ️ Biz haqimizda":
        return about_us(update, context)

    # Faqat media yuborilgan (voice, photo, video) → Guruhga yuborish
    if update.message.voice:
        bot.send_voice(chat_id=GROUP_ID, voice=update.message.voice.file_id)
        return

    if update.message.photo:
        bot.send_photo(chat_id=GROUP_ID, photo=update.message.photo[-1].file_id)
        return

    if update.message.video:
        bot.send_video(chat_id=GROUP_ID, video=update.message.video.file_id)
        return

    # Matnli ariza → faqat telefon raqamdan keyin
    if state == "WAITING_APPLICATION" and update.message.text:
        phone = context.user_data.get("phone", "Nomaʼlum")
        caption = (
            f"📩 *Yangi ariza:*\n"
            f"👤 {user.full_name}\n"
            f"🔗 @{user.username or 'yo‘q'}\n"
            f"📞 {phone}\n"
            f"📝 {update.message.text}"
        )
        bot.send_message(chat_id=GROUP_ID, text=caption, parse_mode="Markdown")
        update.message.reply_text("✅ Arizangiz muvaffaqiyatli yuborildi!")
        user_state[user_id] = None
        return

    # Agar boshqa holat bo‘lsa:
    update.message.reply_text("Iltimos, /start buyrug‘ini yuboring.")

# Handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("about", about_us))
dispatcher.add_handler(MessageHandler(
    Filters.private & (
        Filters.text |
        Filters.contact |
        Filters.photo |
        Filters.video |
        Filters.voice
    ),
    handle_message
))
