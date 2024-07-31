from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from state import orderRound, fullOrder, hasDinnerStarted
import json

async def startDinner(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    global hasDinnerStarted
    admins = [line.strip() for line in open('admins.txt')]
    thread_id = update.message.message_thread_id

    if str(update.message.from_user.username) in admins:
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

        hasDinnerStarted = True

async def dinnerOrder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global orderRound, fullOrder, hasDinnerStarted
    f = open('menu.json')
    data = json.load(f)
    thread_id = update.message.message_thread_id
    if hasDinnerStarted:
        if context.args:
            if context.args[0].isnumeric():
                itemName = None
                for item in data["Menu"]:
                    if item["id"] == int(context.args[0]):
                        itemName = item["Name"]
                        break
                if itemName is None:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='O ide non é válido', message_thread_id=thread_id)
                    return
                if len(context.args) < 2:
                    if itemName in orderRound:
                        orderRound[str(itemName)] += 1
                    else:
                        orderRound[str(itemName)] = 1
                    orderMessage = "\n".join([f"{value} - {key}" for key, value in orderRound.items()])
                    await context.bot.send_message(chat_id=update.message.chat_id, text=f"{orderMessage}", message_thread_id=thread_id)
                    if update.message.from_user.username:
                        if str(update.message.from_user.username) in fullOrder and context.args[0] in fullOrder[str(update.message.from_user.username)]:
                            fullOrder[str(update.message.from_user.username)][context.args[0]] += 1
                        elif str(update.message.from_user.username) in fullOrder:
                            fullOrder[str(update.message.from_user.username)][context.args[0]] = 1
                        else:
                            fullOrder[str(update.message.from_user.username)] = {}
                            fullOrder[str(update.message.from_user.username)][context.args[0]] = 1
                    elif update.message.from_user.first_name:
                        if str(update.message.from_user.first_name) in fullOrder and context.args[0] in fullOrder[str(update.message.from_user.first_name)]:
                            fullOrder[str(update.message.from_user.first_name)][context.args[0]] += 1
                        elif str(update.message.from_user.first_name) in fullOrder:
                            fullOrder[str(update.message.from_user.first_name)][context.args[0]] = 1
                        else:
                            fullOrder[str(update.message.from_user.first_name)] = {}
                            fullOrder[str(update.message.from_user.first_name)][context.args[0]] = 1
                    else: 
                        await context.bot.send_message(chat_id=update.effective_chat.id, text='Necesítase un username ou nome en Telegram para ordenar.', message_thread_id=thread_id)
                        return
                elif not context.args[1].isnumeric() or not isinstance(int(context.args[1]), int):
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='Se vas enviar unha cantidade de pratos, a mesma debe ser un numero enteiro (@soulcodex, estou a vixiarche)', message_thread_id=thread_id)
                    return
                elif int(context.args[1]) <= 0 or int(context.args[1]) > 5:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='A cantidade non é valida', message_thread_id=thread_id)
                    return
                elif context.args[1] and context.args[1].isnumeric() and isinstance(context.args[1].isnumeric(), int):
                    if update.message.from_user.username:
                        if itemName in orderRound:
                            orderRound[str(itemName)] += int(context.args[1])
                        else:
                            orderRound[str(itemName)] = int(context.args[1])
                        orderMessage = "\n".join([f"{value} - {key}" for key, value in orderRound.items()])
                        await context.bot.send_message(chat_id=update.message.chat_id, text=f"{orderMessage}", message_thread_id=thread_id)
                        if str(update.message.from_user.username) in fullOrder and context.args[0] in fullOrder[str(update.message.from_user.username)]:
                            fullOrder[str(update.message.from_user.username)][context.args[0]] += int(context.args[1])
                        elif str(update.message.from_user.username) in fullOrder:
                            fullOrder[str(update.message.from_user.username)][context.args[0]] = int(context.args[1])
                        else:
                            fullOrder[str(update.message.from_user.username)] = {}
                            fullOrder[str(update.message.from_user.username)][context.args[0]] = int(context.args[1])
                    elif update.message.from_user.first_name:
                        if itemName in orderRound:
                            orderRound[str(itemName)] += int(context.args[1])
                        else:
                            orderRound[str(itemName)] = int(context.args[1])
                        orderMessage = "\n".join([f"{value} - {key}" for key, value in orderRound.items()])
                        await context.bot.send_message(chat_id=update.message.chat_id, text=f"{orderMessage}", message_thread_id=thread_id)
                        if str(update.message.from_user.first_name) in fullOrder and context.args[0] in fullOrder[str(update.message.from_user.first_name)]:
                            fullOrder[str(update.message.from_user.first_name)][context.args[0]] += int(context.args[1])
                        elif str(update.message.from_user.first_name) in fullOrder:
                            fullOrder[str(update.message.from_user.first_name)][context.args[0]] = int(context.args[1])
                        else:
                            fullOrder[str(update.message.from_user.first_name)] = {}
                            fullOrder[str(update.message.from_user.first_name)][context.args[0]] = int(context.args[1])
                    else: 
                        await context.bot.send_message(chat_id=update.effective_chat.id, text='Necesítase un username ou nome en Telegram para ordenar.', message_thread_id=thread_id)
                        return
                elif context.args[1] and not context.args[1].isnumeric() and not isinstance(context.args[1].isnumeric(), int):
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='Se vas enviar unha cantidade de pratos, a mesma debe ser un numero enteiro (@soulcodex, estou a vixiarche)', message_thread_id=thread_id)
                    
                elif itemName is None:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='O ide non é válido', message_thread_id=thread_id)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='O ide non é válido', message_thread_id=thread_id)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='É necesario enviar un item para ordenar', message_thread_id=thread_id)

async def beerTaker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global orderRound, fullOrder, hasDinnerStarted
    thread_id = update.message.message_thread_id
    if hasDinnerStarted:
        if update.message.from_user.username:
            if str(update.message.from_user.username) in fullOrder and "1906" in fullOrder[str(update.message.from_user.username)]:
                fullOrder[str(update.message.from_user.username)]["1906"] += 1
            elif str(update.message.from_user.username) in fullOrder:
                fullOrder[str(update.message.from_user.username)]["1906"] = 1
            else:
                fullOrder[str(update.message.from_user.username)] = {}
                fullOrder[str(update.message.from_user.username)]["1906"] = 1
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Agregado un vaso de cervexa para o usuario.', message_thread_id=thread_id)
            return
        elif update.message.from_user.first_name:
            if str(update.message.from_user.first_name) in fullOrder and "1906" in fullOrder[str(update.message.from_user.first_name)]:
                fullOrder[str(update.message.from_user.first_name)]["1906"] += 1
            elif str(update.message.from_user.first_name) in fullOrder:
                fullOrder[str(update.message.from_user.first_name)]["1906"] = 1
            else:
                fullOrder[str(update.message.from_user.first_name)] = {}
                fullOrder[str(update.message.from_user.first_name)]["1906"] = 1
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Agregado un vaso de cervexa para o usuario.', message_thread_id=thread_id)
            return
        else: 
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Necesítase un username ou nome en Telegram para ordenar.', message_thread_id=thread_id)
            return
async def endDinner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global fullOrder, hasDinnerStarted, orderRound
    admins = [line.strip() for line in open('admins.txt')]
    finalBill = {}
    thread_id = update.message.message_thread_id
    with open('menu.json') as f:
        data = json.load(f)

    if hasDinnerStarted:
        if str(update.message.from_user.username) in admins:
            if context.args:
                category = str(context.args[0])
                totalbill = 0
                totalbeer = 0
                beeramount = 0
                beerusers = []
                for user in fullOrder:
                    user_order = fullOrder.get(user, {})
                    finalBill[str(user)] = 0
                    for id in user_order:
                        item_price = 0
                        for item in data["Menu"]:
                            if item["id"] == int(id):
                                item_price = item["Price"]
                                break
                        if int(id) >= 100 and int(id) < 200 and category in ["bebidas", "bebidasypostres"]:
                            if str(id) in ['103','104','105','106']:
                                totalbeer += item_price * int(user_order[id])
                            else:
                                finalBill[str(user)] += item_price * int(user_order[id])
                        elif int(id) >= 200 and int(id) < 300 and category in ["postres", "bebidasypostres"]:
                            finalBill[str(user)] += item_price * int(user_order[id])
                        elif int(id) == 1906 and category in ["bebidas", "bebidasypostres"]:
                            beerusers.append(str(user))
                            beeramount += fullOrder[str(user)]["1906"]
                        else:
                            totalbill += item_price * int(user_order[id])

                if category in ["bebidas", "postres", "bebidasypostres"]:
                    personaltotal = totalbill / len(fullOrder)
                    for user in finalBill:
                        finalBill[user] += personaltotal
                if category in ["bebidas","bebidasypostres"]:
                    personalbeer = totalbeer / beeramount
                    if personalbeer > 0:
                        for user in finalBill:
                            if str(user) in beerusers:
                                finalBill[user] += personalbeer * fullOrder[str(user)]["1906"]
                billMessage = "\n".join([f"{key} - {round(float(value),2)}€" for key, value in finalBill.items()])
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"{billMessage}", message_thread_id=thread_id)
                orderRound = {}
                fullOrder = {}
                hasDinnerStarted = False
            else:
                totalbill = 0
                for user in fullOrder:
                    user_order = fullOrder.get(user, {})
                    finalBill[str(user)] = 0
                    for id in user_order:
                        item_price = 0
                        for item in data["Menu"]:
                            if item["id"] == int(id):
                                item_price = item["Price"]
                                break
                        totalbill += item_price * int(user_order[id])
                personaltotal = totalbill / len(fullOrder)
                for user in finalBill:
                    finalBill[user] += personaltotal

                billMessage = "\n".join([f"{key} - {value}€" for key, value in finalBill.items()])
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"{billMessage}", message_thread_id=thread_id)
                orderRound = {}
                fullOrder = {}
                hasDinnerStarted = False

async def roundOrder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id
    global hasDinnerStarted, orderRound, fullOrder
    if hasDinnerStarted:
        orderMessage = "\n".join([f"{value} - {key}" for key, value in orderRound.items()])
        await context.bot.send_message(chat_id=update.message.chat_id, text=f"{orderMessage}", message_thread_id=thread_id)
        orderRound = {}

async def changePrice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = [line.strip() for line in open('admins.txt')]
    thread_id = update.message.message_thread_id
    f = open('menu.json')
    data = json.load(f)
    if str(update.message.from_user.username) in admins:
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
                