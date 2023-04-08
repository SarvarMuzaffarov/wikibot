import logging
import wikipediaapi
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up the logging module
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up the Wikipedia API for the Uzbek language
wiki = wikipediaapi.Wikipedia('uz')

# Define a function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Assalomu alaykum! Men Vikipediadan ma'lumot izlovchi botman. Iltimos, so'rov jo'nating!")

# Define a function to handle Wikipedia search queries
def handle_message(update, context):
    query = update.message.text
    page = wiki.page(query)
    if page.exists():
        summary = page.summary[0:3000]
        context.bot.send_message(chat_id=update.effective_chat.id, text=summary, 
                                 parse_mode='Markdown', disable_web_page_preview=True)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                                 text="Uzr, bu mavzu haqida ma'lumot topilmadi. Boshqa mavzu nomini kiriting yoki so'zlar to'g'ri yozilganiga ishoch hosil qiling .")

# Define a function to handle errors
def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Set up the Telegram bot
def main():
    # Set up the API token and start the bot
    updater = Updater("5858976372:AAFeCP9p_nM247ByOB3oxB-GsQuYmO-FD9k", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))

    # Register message handler for Wikipedia searches
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Register error handler
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
