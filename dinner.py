from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from state import orderRound, fullOrder, hasDinnerStarted
import json

async def startDinner(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    global hasDinnerStarted
    admins = [line.strip() for line in open('admins.txt')]
    thread_id = update.message.message_thread_id

    if str(update.message.from_user.username) in admins:
        with open("menu.json", 'r') as archive:
            menu = json.load(archive)
        
        orderMessages = []
        for item in menu["Menu"]:
            orderMessages.append(f"{item['id']} - {item['Name']} \n Precio: {item['Price']} €")        
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
                    if str(update.message.from_user.username) in fullOrder and context.args[0] in fullOrder[str(update.message.from_user.username)]:
                        fullOrder[str(update.message.from_user.username)][context.args[0]] += 1
                    elif str(update.message.from_user.username) in fullOrder:
                        fullOrder[str(update.message.from_user.username)][context.args[0]] = 1
                    else:
                        fullOrder[str(update.message.from_user.username)] = {}
                        fullOrder[str(update.message.from_user.username)][context.args[0]] = 1
                    print(fullOrder)
                elif int(context.args[1]) <= 0:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='A cantidade non é valida', message_thread_id=thread_id)
                    return
                elif context.args[1] and context.args[1].isnumeric():
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
                    print(fullOrder)
                elif context.args[1] and not context.args[1].isnumeric():
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='Se vas enviar unha cantidade de pratos, a mesma debe ser numérica', message_thread_id=thread_id)
                    
                elif itemName is None:
                    await context.bot.send_message(chat_id=update.effective_chat.id, text='O ide non é válido', message_thread_id=thread_id)
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='O ide non é válido', message_thread_id=thread_id)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='É necesario enviar un item para ordenar', message_thread_id=thread_id)

async def endDinner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global fullOrder, hasDinnerStarted, orderRound
    admins = [line.strip() for line in open('admins.txt')]
    finalBill = {}
    thread_id = update.message.message_thread_id
    f = open('menu.json')
    data = json.load(f)
    if hasDinnerStarted:
        if str(update.message.from_user.username) in admins:
            if context.args:
                if str(context.args[0]) == "bebidas":
                    totalbill=0
                    for user in fullOrder:
                        finalBill[str(user)] = 0
                        for id in fullOrder[user]:                            
                            for item in data["Menu"]:
                                if item["id"] == int(id) and int(id) >= 100 and int(id) < 200:
                                    print(item["Price"] * int(fullOrder[user][id]))
                                    finalBill[str(user)] += item["Price"] * int(fullOrder[user][id])
                                elif item["id"] == int(id):
                                    totalbill += item["Price"] * int(fullOrder[user][id])
                    personaltotal = totalbill / len(fullOrder)
                    print(finalBill)
                    for user in finalBill:
                        finalBill[user] += personaltotal
                    billMessage = "\n".join([f"{key} - {value}€" for key, value in finalBill.items()])
                    await context.bot.send_message(chat_id=update.message.chat_id, text=f"{billMessage}", message_thread_id=thread_id)
                    orderRound = {}
                    fullOrder = {}
                    hasDinnerStarted = False
                elif str(context.args[0]) == "postres":
                    totalbill=0
                    for user in fullOrder:
                        finalBill[str(user)] = 0
                        for id in fullOrder[user]:                            
                            for item in data["Menu"]:
                                if item["id"] == int(id) and int(id) >= 200 and int(id) < 300:
                                    print(item["Price"] * int(fullOrder[user][id]))
                                    finalBill[str(user)] += item["Price"] * int(fullOrder[user][id])
                                elif item["id"] == int(id):
                                    totalbill += item["Price"] * int(fullOrder[user][id])
                    personaltotal = totalbill / len(fullOrder)
                    for user in finalBill:
                        finalBill[user] += personaltotal
                    billMessage = "\n".join([f"{key} - {value}€" for key, value in finalBill.items()])
                    await context.bot.send_message(chat_id=update.message.chat_id, text=f"{billMessage}", message_thread_id=thread_id)
                    orderRound = {}
                    fullOrder = {}
                    hasDinnerStarted = False
                elif str(context.args[0]) == "bebidasypostres":
                    totalbill=0
                    for user in fullOrder:
                        finalBill[str(user)] = 0
                        for id in fullOrder[user]:                            
                            for item in data["Menu"]:
                                if item["id"] == int(id) and int(id) >= 100 and int(id) < 300:
                                    print(item["Price"] * int(fullOrder[user][id]))
                                    finalBill[str(user)] += item["Price"] * int(fullOrder[user][id])
                                elif item["id"] == int(id):
                                    totalbill += item["Price"] * int(fullOrder[user][id])
                    personaltotal = totalbill / len(fullOrder)
                    for user in finalBill:
                        finalBill[user] += personaltotal
                    billMessage = "\n".join([f"{key} - {value}€" for key, value in finalBill.items()])
                    await context.bot.send_message(chat_id=update.message.chat_id, text=f"{billMessage}", message_thread_id=thread_id)
                    orderRound = {}
                    fullOrder = {}
                    hasDinnerStarted = False
            else:
                totalbill=0
                for user in fullOrder:
                        finalBill[str(user)] = 0
                        for id in fullOrder[user]:                            
                            for item in data["Menu"]:
                                if item["id"] == int(id):
                                    totalbill += item["Price"] * int(fullOrder[user][id])
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
                