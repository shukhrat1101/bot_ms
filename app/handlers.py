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
        "Xizmat sifatini yaxshilash maqsadida, Iltimos, telefon raqamingizni yuboring:",
        reply_markup=markup
    )

def about_us(update: Update, context):
    if update.message.chat.type != 'private':
        return

    update.message.reply_text(
        "📢 *Biz haqimizda*\n\n"
        "Assalomu aleykum. Siz Mudofaa sanoati agentligining murojaat botiga tashrif buyurdingiz.\n\n"
        "Ushbu bot orqali Agentlik rahbariyatiga oʻz murojaatingizni yuborishingiz mumkin.\n"
        "Murojaatchi toʻgʻrisidagi maʼlumotlar toʻliq sir saqlanadi.",
        parse_mode="Markdown"
    )

def handle_message(update: Update, context):
    if update.message.chat.type != 'private':
        return

    user_id = update.message.chat_id
    state = user_state.get(user_id)

    if update.message.text == "ℹ️ Biz haqimizda":
        return about_us(update, context)

    if update.message.contact:
        phone = update.message.contact.phone_number
        if is_valid_phone(phone):
            user_state[user_id] = "WAITING_APPLICATION"
            context.user_data["phone"] = phone
            update.message.reply_text("✅ Raqam to‘g‘ri! Endi ariza yozing:")
        else:
            update.message.reply_text("❌ Noto‘g‘ri format! Raqam: +998XXXXXXXXX ko‘rinishida bo‘lishi kerak.")

    elif state == "WAITING_APPLICATION":
        ariza = update.message.text
        phone = context.user_data.get("phone", "Nomaʼlum")
        user = update.message.from_user

        text = f"📩 *Yangi ariza:*\n👤 {user.full_name}\n🔗 @{user.username or 'yo‘q'}\n📞 {phone}\n📝 {ariza}"
        bot.send_message(chat_id=GROUP_ID, text=text, parse_mode="Markdown")

        update.message.reply_text("✅ Arizangiz muvaffaqiyatli yuborildi!")
        user_state[user_id] = None

    else:
        update.message.reply_text("Iltimos, /start buyrug‘ini yuboring.")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("about", about_us))
dispatcher.add_handler(MessageHandler(Filters.private & (Filters.contact | Filters.text), handle_message))