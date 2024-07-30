from telegram.ext import Updater, CommandHandler, ApplicationBuilder, MessageHandler, filters
from start import start
from newmembers import new_members
from cerveza import cerveza, cervezahora, cervezalugar, cervezamapa, cervezaasistencia,cervezalink
from help import help
from pina import pinacolada
from fiestas import festivos
from karma import kup, kdown, kshow, klist
from dinner import startDinner, dinnerOrder, roundOrder, changePrice, endDinner, beerTaker
import tracemalloc
tracemalloc.start()


def main():
    
    # Create an updater object with your bot's token
    application = ApplicationBuilder().token('6836403587:AAFaoLBovQo-Sd69RcgUk_uFTkZctRcyqZY').build()


    # Add a handler for the /start command
    application.add_handler(CommandHandler("start", start))

    # Add a handler for the /cañas command
    application.add_handler(CommandHandler("cerveza", cerveza))

    # Add a handler for changing the cañas time
    application.add_handler(CommandHandler("cervezahora", cervezahora))

    # Add a handler for changing the cañas place
    application.add_handler(CommandHandler("cervezalugar", cervezalugar))

    # Add a handler for changing the cañas map
    application.add_handler(CommandHandler("cervezamapa", cervezamapa))

    # Add a handler for changing the cañas assistance
    application.add_handler(CommandHandler("cervezamapa", cervezaasistencia))

    # Add a handler for changing the cañas link
    application.add_handler(CommandHandler("cervezalink", cervezalink))

     # Add a handler for the /cañas command
    application.add_handler(CommandHandler("help", help))

    # Add a handler for the /festivos command
    application.add_handler(CommandHandler("festivos", festivos))

    #Add a handler for the new member entering the chat
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_members))

    #Add a handler for adding karma to user
    application.add_handler(CommandHandler("kup", kup))

    #Add a handler for removing karma to user
    application.add_handler(CommandHandler("kdown", kdown))

    #Add a handler for showing karma of user
    application.add_handler(CommandHandler("kshow", kshow))

    #Add a handler for showing karma top
    application.add_handler(CommandHandler("klist", klist))

    #Add a handler for the Pina command
    application.add_handler(CommandHandler("pineapple", pinacolada))

    #Add a handler for Starting Dinner
    application.add_handler(CommandHandler("startdinner", startDinner))

    #Add a handler for Ordering Dinner
    application.add_handler(CommandHandler("order", dinnerOrder))

    #Add a handler for Closing Order Round
    application.add_handler(CommandHandler("roundorder", roundOrder))

    #Add a handler for Changing Item Price
    application.add_handler(CommandHandler("pricechange", changePrice))

    #Add a handler for Ending Dinner
    application.add_handler(CommandHandler("enddinner", endDinner))

    #Add a handler for Drinking Beer
    application.add_handler(CommandHandler("beertaker", beerTaker))


    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()