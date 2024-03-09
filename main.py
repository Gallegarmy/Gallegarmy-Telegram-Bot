from telegram.ext import Updater, CommandHandler, ApplicationBuilder, MessageHandler, filters
from start import start
from newmembers import new_members
import tracemalloc
tracemalloc.start()

def main():
    # Create an updater object with your bot's token
    application = ApplicationBuilder().token('6836403587:AAFaoLBovQo-Sd69RcgUk_uFTkZctRcyqZY').build()


    # Add a handler for the /start command
    application.add_handler(CommandHandler("start", start))

    #Add a handler for the new member entering the chat
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_members))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()