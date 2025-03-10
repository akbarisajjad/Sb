from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from tools.scraper import scrape_website
import os

# توکن ربات را از متغیر محیطی دریافت می‌کنیم
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# منوی اصلی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 اسکرپ سایت", callback_data='scrape')],
        [InlineKeyboardButton("🔑 تحلیل کلمات کلیدی", callback_data='keywords')],
        [InlineKeyboardButton("🔗 بررسی بک‌لینک‌ها", callback_data='backlinks')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام! ابزار موردنظر خود را انتخاب کنید:", reply_markup=reply_markup)

# مدیریت انتخاب‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'scrape':
        await query.edit_message_text(text="لینک سایت را ارسال کنید:")
        context.user_data['current_action'] = 'scrape'
    else:
        await query.edit_message_text(text="ابزار انتخاب‌شده هنوز پیاده‌سازی نشده است.")

# دریافت پیام و انجام عملیات
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get('current_action')

    if action == 'scrape':
        url = update.message.text
        result = scrape_website(url)
        await update.message.reply_text(result)
        context.user_data['current_action'] = None
    else:
        await update.message.reply_text("لطفاً ابتدا یک ابزار را از منو انتخاب کنید.")

# اجرای ربات
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
