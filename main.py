from telegram.ext import Updater, CommandHandler, ApplicationBuilder, MessageHandler, filters
from start import start
from newmembers import new_members
from cerveza import cerveza
from help import help
from pina import pinacolada
from fiestas import festivos
from karma import kup
import tracemalloc
tracemalloc.start()

def main():
    
    # Create an updater object with your bot's token
    application = ApplicationBuilder().token('6836403587:AAFaoLBovQo-Sd69RcgUk_uFTkZctRcyqZY').build()


    # Add a handler for the /start command
    application.add_handler(CommandHandler("start", start))

    # Add a handler for the /cañas command
    application.add_handler(CommandHandler("cerveza", cerveza))

     # Add a handler for the /cañas command
    application.add_handler(CommandHandler("help", help))

    # Add a handler for the /festivos command
    application.add_handler(CommandHandler("festivos", festivos))

    #Add a handler for the new member entering the chat
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_members))

    #Add a handler for adding karma to user
    application.add_handler(CommandHandler("kup", kup))

    #Add a handler for the Pina command
    application.add_handler(CommandHandler("pineapple", pinacolada))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()