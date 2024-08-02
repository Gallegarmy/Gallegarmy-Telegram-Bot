from contextlib import suppress

import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import json
from collections import defaultdict


def default_factory():
    return defaultdict(int)


"""
    En este diccionario no hay que crear cada subdiccionario 
    ni comprobar que existan las claves.

    De este modo al hacer:
        fullOrder['user']['1906']
        fullOrder['user']['patatas']

    las entradas se crean si no existen con valor a cero por defecto.

    Si en lugar de lo anterior escribiesemos, por ej:
        fullOrder['user']['1906'] += valor
        fullOrder['user']['patatas'] += valor

    además de lo anterior, crear las entradas a cero si no existen, 
    y siempre sumaría valor al valor ya contenido en la entrada.
"""
fullOrder = defaultdict(default_factory)

with open("menu.json", 'r', encoding='utf-8') as archive:
    menu = json.load(archive)
    names = {int(obj['id']): obj['Name'] for obj in menu['Menu']}

orderRound = defaultdict(int)
hasDinnerStarted = False

ADMINS = [line.strip() for line in open('admins.txt')]


async def startDinner(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    global hasDinnerStarted
    thread_id = update.message.message_thread_id

    if str(update.message.from_user.username) in ADMINS:
        with open("menu.json", 'r', encoding='utf-8') as archive:
            menu = json.load(archive)
        
        orderMessages = []
        for item in menu["Menu"]:
            orderMessages.append(f"{item['id']} - {item['Name'].capitalize()} ({item['Price']} €)")        
        orderMessage = "\n".join(orderMessages)
        
        MAX_MESSAGE_LENGTH = 4096
        for i in range(0, len(orderMessage), MAX_MESSAGE_LENGTH):
            part = orderMessage[i:i + MAX_MESSAGE_LENGTH]
            await context.bot.send_message(chat_id=update.message.chat_id, text=part, message_thread_id=thread_id)

        keyb = InlineKeyboardMarkup([
            [InlineKeyboardButton('\U0001F37A', callback_data=f'beer,{thread_id}'), InlineKeyboardButton('\U0001F4B6', callback_data=f'bill,{thread_id}')],
            [InlineKeyboardButton('\U0000261D', callback_data=f'order,{thread_id}')],
        ])
        await update.effective_chat.send_message('A puta mensaxede texto que me obriga a meter', reply_markup=keyb, message_thread_id=thread_id)

        hasDinnerStarted = True


def find_menuitem(data, menu_item_id):
    itemName = None
    for item in data["Menu"]:
        if item["id"] == int(menu_item_id):
            itemName = item["Name"]
            break
    return itemName


def is_quantity_in_range(quantity):
    return 0 < quantity <= 5


async def show_dinner_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id
    keyb = InlineKeyboardMarkup([
        [InlineKeyboardButton('\U0001F37A', callback_data='beer'), InlineKeyboardButton('\U0001F4B6', callback_data='bill')],
        [InlineKeyboardButton('\U0000261D', callback_data='order')],
    ])
    await update.effective_chat.send_message('A puta mensaxede texto que me obriga a meter', reply_markup=keyb, message_thread_id=thread_id)


async def dinnerkeyb_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update and update.callback_query:

        parts = update.callback_query.data.split(',')
        command = parts[0]
        thread_id = parts[1]

        example_msg = f'Recibido datos de boton: {update.callback_query.data}'
        if command == 'beer':
            await beerTaker(update, context, thread_id)
            # Suprimimos o erro en caso de timeout
            # (prefiro isto a un try/except que non fai nada coa excepcion)
            with suppress(telegram.error.BadRequest):
                await update.callback_query.answer('Popup molon de birra')
        elif command == 'bill':
            # Hai que escribir text= porque se non se pensa que o argumento é un chat_id
            await endDinner(update,context, thread_id)
            with suppress(telegram.error.BadRequest):
                await update.callback_query.answer('Popup molon de dinero')
        elif command == 'order':
            await roundOrder(update,context, thread_id)
            with suppress(telegram.error.BadRequest):
                await update.callback_query.answer('Popup molon de dinero')


async def beerTaker(update: Update, context: ContextTypes.DEFAULT_TYPE, id_thread):
    global orderRound, fullOrder, hasDinnerStarted
    thread_id = update.message.message_thread_id if update.message.message_thread_id is not None else id_thread
    if hasDinnerStarted:
        request_user = await get_user(update, context)

        fullOrder[request_user]["1906"] += 1
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Agregado un vaso de cervexa para o usuario.', message_thread_id=thread_id)


async def dinnerOrder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await addOrRemove(update, context, True)


async def removeItemOrder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await addOrRemove(update, context, False)


async def addOrRemove(update: Update, context: ContextTypes.DEFAULT_TYPE, add):
    global fullOrder, hasDinnerStarted, orderRound

    if not add and str(update.message.from_user.username) not in ADMINS:
        return
    thread_id = update.message.message_thread_id
    if hasDinnerStarted:
        if not context.args:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='É necesario enviar un item para modificar o pedido', message_thread_id=thread_id)
            return

        if len(context.args) < 3:
            quantity = 1
            if len(context.args) > 1:
                try:
                    quantity = int(context.args[1])
                except ValueError as e:
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text='A cantidade non é válida',
                                                   message_thread_id=thread_id)
                    return

            if add:
                if not is_quantity_in_range(quantity):
                    await context.bot.send_message(chat_id=update.effective_chat.id,
                                                   text='A cantidade non é valida', message_thread_id=thread_id)
                    return

            request_user = await get_user(update, context)


            # Recuperamos o item (prato, bebida, postre) do menu
            menu_item_id = context.args[0]
            if not menu_item_id.isnumeric():
                await context.bot.send_message(chat_id=update.effective_chat.id, text='O ide non é válido',
                                               message_thread_id=thread_id)
                return

            menu_item_id = int(menu_item_id)
            if not menu_item_id in names:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='O ide non é válido',
                                               message_thread_id=thread_id)
                return

            if add:
                orderRound[menu_item_id] += quantity
                fullOrder[request_user][menu_item_id] += quantity
            else:
                if menu_item_id in orderRound:
                    orderRound[menu_item_id] -= quantity

                    if orderRound[menu_item_id] <= 0:
                        del orderRound[menu_item_id]

                if menu_item_id in fullOrder:
                    fullOrder[request_user][menu_item_id] -= quantity

                    if fullOrder[request_user][menu_item_id] <= 0:
                        del fullOrder[request_user][menu_item_id]

            orderMessage = "\n".join([f"{value} - {names[key]}" for key, value in orderRound.items()])
            await context.bot.send_message(chat_id=update.message.chat_id,
                                           text=f"{orderMessage}",
                                           message_thread_id=thread_id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Orde modificada',
                                           message_thread_id=thread_id)
            return
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Non se admiten máis de dous argumentos para esta funcion', message_thread_id=thread_id)
            return


async def endDinner(update: Update, context: ContextTypes.DEFAULT_TYPE, id_thread):
    global fullOrder, hasDinnerStarted, orderRound
    finalBill = {}
    thread_id = update.message.message_thread_id if update.message.message_thread_id is not None else id_thread
    with open('menu.json') as f:
        data = json.load(f)

    if hasDinnerStarted:
        if await get_user(update, context) in ADMINS:
            if context.args:
                category = str(context.args[0])
                totalbill = 0
                totalbeer = 0
                beeramount = 0
                beerusers = []
                for user in fullOrder:
                    user_order = fullOrder.get(user, {})
                    finalBill[user] = 0
                    for item_id in user_order:
                        item_price = 0
                        if item_id >= 100 and item_id < 200 and category in ["bebidas", "bebidasypostres"]:
                            if str(item_id) in ('103', '104', '105', '106'):
                                totalbeer += item_price * user_order[item_id]
                            else:
                                finalBill[user] += item_price * user_order[item_id]
                        elif item_id >= 200 and item_id < 300 and category in ["postres", "bebidasypostres"]:
                            finalBill[user] += item_price * user_order[item_id]
                        elif item_id == 1906 and category in ["bebidas", "bebidasypostres"]:
                            beerusers.append(user)
                            beeramount += fullOrder[user]["1906"]
                        else:
                            totalbill += item_price * user_order[item_id]

                if category in ["bebidas", "postres", "bebidasypostres"]:
                    personaltotal = totalbill / len(fullOrder)
                    for user in finalBill:
                        finalBill[user] += personaltotal
                if category in ["bebidas", "bebidasypostres"]:
                    personalbeer = totalbeer / beeramount
                    if personalbeer > 0:
                        for user in finalBill:
                            if user in beerusers:
                                finalBill[user] += personalbeer * fullOrder[user]["1906"]
                billMessage = "\n".join([f"{key} - {round(float(value),2)}€" for key, value in finalBill.items()])
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"{billMessage}", message_thread_id=thread_id)
                orderRound = {}
                fullOrder = {}
                hasDinnerStarted = False
            else:
                totalbill = 0
                for user in fullOrder:
                    user_order = fullOrder.get(user, {})
                    finalBill[user] = 0
                    for item_id in user_order:
                        item_price = 0
                        for item in data["Menu"]:
                            if item["id"] == item_id:
                                item_price = item["Price"]
                                break
                        totalbill += item_price * user_order[item_id]
                personaltotal = totalbill / len(fullOrder)
                for user in finalBill:
                    finalBill[user] += personaltotal

                billMessage = "\n".join([f"{key} - {value}€" for key, value in finalBill.items()])
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"{billMessage}", message_thread_id=thread_id)
                orderRound = {}
                fullOrder = {}
                hasDinnerStarted = False


async def roundOrder(update: Update, context: ContextTypes.DEFAULT_TYPE, id_thread):
    thread_id = update.message.message_thread_id if update.message is not None else id_thread
    global hasDinnerStarted, orderRound, fullOrder
    if hasDinnerStarted:
        orderMessage = "\n".join([f"{value} - {names[key]}" for key, value in orderRound.items()])
        await context.bot.send_message(chat_id=update.message.chat_id, text=f"{orderMessage}", message_thread_id=thread_id)
        orderRound = {}


async def changePrice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id
    f = open('menu.json')
    data = json.load(f)
    if str(update.message.from_user.username) in ADMINS:
        if context.args:
                if context.args[0].isnumeric():
                    if len(context.args) == 2:
                        for item in data["Menu"]:
                            if item["id"] == int(context.args[0]):
                                item["Price"] = float(context.args[1])
                                break
                        with open('menu.json', 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False)
                        await context.bot.send_message(chat_id=update.message.chat_id, text="Prezo cambiado.", message_thread_id=thread_id)
                    else:
                        await context.bot.send_message(chat_id=update.message.chat_id, text="Necesítase un ide e un prezo para cambiar o prezo dun produto.", message_thread_id=thread_id)
                else:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='O ide non é válido', message_thread_id=thread_id)


async def changeMenu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = await get_thread_id(update)

    try:
        data = await open_menu_file(update, context)
    except json.JSONDecodeError:
        return

    if get_user(update, context) in ADMINS:
        if context.args and len(context.args) == 3:
            if context.args[0].isnumeric():
                item_id = int(context.args[0])
                name = context.args[1]
                price = context.args[2]

                if not price.isnumeric():
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='O prezo debe ser un número válido.', message_thread_id=thread_id)
                    return

                price = int(price)

                item_updated = False
                for item in data:
                    if item['id'] == item_id:
                        item.update({"Name": name, "Description": "", "Price": price})
                        item_updated = True
                        break

                if not item_updated:
                    data.append({"id": item_id, "Name": name, "Description": "", "Price": price})

                try:
                    with open('menu.json', 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                except IOError:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='Erro ao gardar os cambios no arquivo de menú.', message_thread_id=thread_id)
                    return

                message = 'Menú cambiado.' if item_updated else 'Item agregado.'
                await context.bot.send_message(chat_id=update.effective_chat.id, text=message, message_thread_id=thread_id)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='O IDE non é válido.', message_thread_id=thread_id)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Faltan argumentos para executar a función.', message_thread_id=thread_id)


def get_thread_id(update):
    thread_id = update.message.message_thread_id if update.message is not None else id_thread
    return thread_id


async def open_menu_file(update, context):
    """
    Abre el menu.json con el menu de Fire Capitano
    :param update:
    :param context:
    :param thread_id: el thread_id
    :return: el diccionario con el contenido del menu de Fire Capitano
    """
    try:
        with open('menu.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Error al leer el archivo de menú.',
                                       message_thread_id=get_thread_id(update))
        raise e
    except FileNotFoundError:
        data = []
    return data


async def get_user(update, context):
    if update.message.from_user.username:
        request_user = str(update.message.from_user.username)
    elif update.message.from_user.first_name:
        request_user = str(update.message.from_user.first_name)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Necesítase un username ou nome en Telegram para interactuar co bot.',
                                       message_thread_id=get_thread_id(update))
        return


    return request_user
  