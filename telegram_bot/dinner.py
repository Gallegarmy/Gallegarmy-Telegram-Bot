import functools
from contextlib import suppress

import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, Message
from telegram.ext import ContextTypes
import json
from collections import defaultdict
import structlog

logger = structlog.get_logger()

#FOOD_THREAD_ID = 4226


def default_factory():
    return defaultdict(int)


def async_only_dinner_chat(func):
    """
    Decorator to ensure requests are only handled within the Food Topic thread.
    """

    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if (
            update.effective_message
            #and update.effective_message.message_thread_id == FOOD_THREAD_ID
        ):
            logger.info(
                "Handling request in Food Topic thread",
                user_id=update.effective_user.id if update.effective_user else None,
                chat_id=update.effective_chat.id if update.effective_chat else None,
            )
            return await func(update, context)
        else:
            logger.warning(
                "Request not in Food Topic thread",
                user_id=update.effective_user.id if update.effective_user else None,
                chat_id=update.effective_chat.id if update.effective_chat else None,
            )

    return wrapper


fullOrder = defaultdict(default_factory)
beerOrder = defaultdict(int)

with open("menu.json", "r", encoding="utf-8") as archive:
    menu = json.load(archive)
    names = {int(obj["id"]): obj["Name"] for obj in menu["Menu"]}

orderRound = defaultdict(int)
hasDinnerStarted = False

ADMINS = [line.strip() for line in open("admins.txt")]


@async_only_dinner_chat
async def start_dinner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global hasDinnerStarted
    logger.info(
        "Start dinner command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    thread_id = await get_thread_id(update)
    part = None

    if (
        update.message
        and update.message.from_user
        and update.message.from_user.username in ADMINS
    ):
        menu = load_menu_json()

        orderMessages = []
        for item in menu["Menu"]:
            orderMessages.append(
                f"{item['id']} - ({item['Price']} €) {item['Name'].capitalize()} "
            )
        orderMessage = "\n".join(orderMessages)

        MAX_MESSAGE_LENGTH = 4096
        for i in range(0, len(orderMessage), MAX_MESSAGE_LENGTH):
            part = orderMessage[i : i + MAX_MESSAGE_LENGTH]

        keyb = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("\U0001f37a", callback_data="beer"),
                    InlineKeyboardButton("\U0001f4b6", callback_data="bill"),
                ],
                [InlineKeyboardButton("\U0001f37d", callback_data="dinner")],
            ]
        )
        if update.effective_chat and part is not None:
            await update.effective_chat.send_message(
                part, reply_markup=keyb, message_thread_id=thread_id
            )

        hasDinnerStarted = True


def load_menu_json():
    with open("menu.json", "r", encoding="utf-8") as archive:
        menu = json.load(archive)
    return menu


def find_menu_item(data, menu_item_id):
    itemName = None
    for item in data["Menu"]:
        if item["id"] == int(menu_item_id):
            itemName = item["Name"]
            break
    return itemName


async def show_dinner_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Show dinner keyboard command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    thread_id = update.message.message_thread_id if update.message else None
    keyb = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("\U0001f37a", callback_data="beer"),
                InlineKeyboardButton("\U0001f4b6", callback_data="bill"),
            ],
            [InlineKeyboardButton("\U0001f37d", callback_data="dinner")],
        ]
    )
    if update.effective_chat:
        await update.effective_chat.send_message(
            "A puta mensaxede texto que me obriga a meter",
            reply_markup=keyb,
            message_thread_id=thread_id,
        )


async def dinner_keyboard_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update and update.callback_query:
        command = update.callback_query.data

        logger.info(
            "Dinner keyboard command received",
            command=command,
            user_id=update.effective_user.id if update.effective_user else None,
            chat_id=update.effective_chat.id if update.effective_chat else None,
        )

        if command == "beer":
            await beer_taker(update, context)
            with suppress(telegram.error.BadRequest):
                await update.callback_query.answer("Popup molon de birra")
        elif command == "bill":
            await end_dinner(update, context)
            with suppress(telegram.error.BadRequest):
                await update.callback_query.answer("Popup molon de dinero")
        elif command == "dinner":
            await dinner_taker(update, context)
            with suppress(telegram.error.BadRequest):
                await update.callback_query.answer("Popup molon de comida")


async def beer_taker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Triggered by /beer and the beer button,
    this assigns one beer to the user that triggered the event
    :param update: the update
    :param context: the context
    """
    global hasDinnerStarted, beerOrder

    logger.info(
        "Beer taker command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    if hasDinnerStarted:
        if update and update.callback_query:
            request_user = await get_user(update)

            beerOrder[request_user] += 1
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"Agregado un vaso de cervexa para {request_user}",
                    message_thread_id=await get_thread_id(update),
                )


async def dinner_taker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Triggered by /dinner and the dinner button, this adds a user to the dictionary as a dinnerTaker
    :param update: the update
    :param context: the context
    """
    global fullOrder

    logger.info(
        "Dinner taker command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    request_user = await get_user(update)
    if request_user in fullOrder:
        msg = f"O usuario {request_user} xa está rexistrado para cear."
    else:
        msg = f"Rexistrado o usuario {request_user} para a cea."

    if update.effective_chat:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg,
            message_thread_id=await get_thread_id(update),
        )

@async_only_dinner_chat
async def dinner_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await add_or_remove(update, context, True)


@async_only_dinner_chat
async def remove_item_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await add_or_remove(update, context, False)


async def add_or_remove(update: Update, context: ContextTypes.DEFAULT_TYPE, add):
    """
    Adds or removes something from the order for a specific user
    :param update: the update
    :param context: the context
    :param add: True if the user want to add something to the order, False if he/she wants to remove something
    """
    global fullOrder, hasDinnerStarted, orderRound

    logger.info(
        "Add or remove item command received",
        add=add,
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    if not add and (
        update.message
        and update.message.from_user
        and update.message.from_user.username not in ADMINS
    ):
        return

    thread_id = await get_thread_id(update)
    if hasDinnerStarted:
        if not context.args:
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="É necesario enviar un item para modificar o pedido",
                    message_thread_id=thread_id,
                )
            return

        if len(context.args) < 3:
            quantity = 1
            if len(context.args) > 1:
                try:
                    quantity = int(context.args[1])
                except ValueError:
                    if update.effective_chat:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="A cantidade non é válida",
                            message_thread_id=thread_id,
                        )
                    return

            if add:
                if not is_quantity_in_range(quantity):
                    if update.effective_chat:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="A cantidade non é válida",
                            message_thread_id=thread_id,
                        )
                    return

            request_user = await get_user(update)

            menu_item_id = context.args[0]
            if not menu_item_id.isnumeric():
                if update.effective_chat:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="O ide non é válido",
                        message_thread_id=thread_id,
                    )
                return

            menu_item_id = int(menu_item_id)
            if menu_item_id not in names:
                if update.effective_chat:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="O ide non é válido",
                        message_thread_id=thread_id,
                    )
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

            await show_order(update, context)
            return
        else:
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Non se admiten máis de dous argumentos para esta función",
                    message_thread_id=thread_id,
                )
            return


def is_quantity_in_range(quantity):
    return 0 < quantity <= 5


@async_only_dinner_chat
async def end_dinner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global fullOrder, hasDinnerStarted, orderRound, beerOrder
    finalBill = {}

    logger.info(
        "End dinner command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    with open("menu.json") as f:
        data = json.load(f)

    menu_prices = {item["id"]: item["Price"] for item in data["Menu"]}

    if hasDinnerStarted:
        if (
            update.message
            and update.message.from_user
            and update.message.from_user.username in ADMINS
        ):
            #if context.args:
                #category = str(context.args[0])
                totalbill = 0
                totalbeer = 0
                beeramount = 0
                for user in fullOrder:
                    user_order = fullOrder.get(user, {})
                    finalBill[user] = 0
                    for item_id in user_order:
                        item_price = menu_prices.get(item_id, 0)
                        if (
                            item_id >= 100
                            and item_id < 200
                            #and category in ["bebidas", "bebidasypostres"]
                        ):
                            if item_id in (103, 104, 105, 106):
                                totalbeer += item_price * user_order[item_id]
                            else:
                                finalBill[user] += item_price * user_order[item_id]
                        elif (
                            item_id >= 200
                            and item_id < 300
                            #and category in ["postres", "bebidasypostres"]
                        ):
                            finalBill[user] += item_price * user_order[item_id]
                        else:
                            totalbill += item_price * user_order[item_id]

                #if category in ["bebidas", "postres", "bebidasypostres"]:
                personaltotal = totalbill / len(fullOrder)
                for user in finalBill:
                        finalBill[user] += personaltotal

                for beer_user, beer_glasses in beerOrder.items():
                    beeramount += beer_glasses
                    if beer_user not in finalBill:
                        finalBill[beer_user] = 0

                #if category in ["bebidas", "bebidasypostres"]:
                if beeramount > 0:
                        beer_price = totalbeer / beeramount
                        for user in finalBill:
                            if user in beerOrder:
                                finalBill[user] += beer_price * beerOrder[user]

                billMessage = "\n".join(
                    [
                        f"{key} - {round(float(value), 2)}€"
                        for key, value in finalBill.items()
                    ]
                )
                if update.effective_message:
                    await context.bot.send_message(
                        chat_id=update.effective_message.chat_id,
                        text=billMessage,
                        message_thread_id=await get_thread_id(update),
                    )
                orderRound = defaultdict(int)
                beerOrder = defaultdict(int)
                fullOrder = defaultdict(default_factory)
                if context.chat_data and "order_msg" in context.chat_data:
                    del context.chat_data["order_msg"]
                hasDinnerStarted = False
            #else:
            #    totalbill = 0
            #    for user in fullOrder:
            #        user_order = fullOrder.get(user, {})
            #        finalBill[user] = 0
            #        for item_id in user_order:
            #            item_price = menu_prices.get(item_id, 0)
            #            totalbill += item_price * user_order[item_id]

            #    personaltotal = totalbill / len(fullOrder)
            #    for user in finalBill:
            #        finalBill[user] += personaltotal

            #    billMessage = "\n".join(
            #        [f"{key} - {value}€" for key, value in finalBill.items()]
            #    )
            #    if update.effective_message:
            #        await context.bot.send_message(
            #            chat_id=update.effective_message.chat_id,
            #            text=billMessage,
            #            message_thread_id=await get_thread_id(update),
            #        )
            #    orderRound = defaultdict(int)
            #    fullOrder = defaultdict(default_factory)
            #    if context.chat_data and "order_msg" in context.chat_data:
            #        del context.chat_data["order_msg"]
            #    hasDinnerStarted = False


@async_only_dinner_chat
async def round_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global hasDinnerStarted, orderRound, fullOrder
    logger.info(
        "Round order command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    if hasDinnerStarted:
        if context.chat_data and "order_msg" in context.chat_data:
            del context.chat_data["order_msg"]
        orderRound = defaultdict(int)


async def show_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global orderRound
    logger.info(
        "Show order command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    order_msg = None
    orderMessage = "PEDIDO:\n\n"
    orderMessage += "\n".join(
        [f"{value} - {names[key]}" for key, value in orderRound.items()]
    )
    new_order = f"{orderMessage}"

    if context.chat_data is None:
        context.chat_data = {}
    if "order_msg" not in context.chat_data:
        if update.effective_message:
            order_msg = await context.bot.send_message(
                chat_id=update.effective_message.chat_id,
                text=new_order,
                message_thread_id=await get_thread_id(update),
            )
        context.chat_data["order_msg"] = order_msg
    else:
        msg: Message = context.chat_data["order_msg"]
        if msg.text and msg.text.strip() != new_order.strip():
            order_msg = await context.chat_data["order_msg"].edit_text(text=new_order)
            context.chat_data["order_msg"] = order_msg


@async_only_dinner_chat
async def change_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Change price command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    thread_id = update.message.message_thread_id if update.message else None
    f = open("menu.json")
    data = json.load(f)
    if (
        update.message
        and update.message.from_user
        and update.message.from_user.username in ADMINS
    ):
        if context.args:
            if context.args[0].isnumeric():
                if len(context.args) == 2:
                    for item in data["Menu"]:
                        if item["id"] == int(context.args[0]):
                            item["Price"] = float(context.args[1])
                            break
                    with open("menu.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False)
                    if update.effective_chat:
                        await context.bot.send_message(
                            chat_id=update.message.chat_id,
                            text="Prezo cambiado.",
                            message_thread_id=thread_id,
                        )
                else:
                    if update.effective_chat:
                        await context.bot.send_message(
                            chat_id=update.message.chat_id,
                            text="Necesítase un ide e un prezo para cambiar o prezo dun produto.",
                            message_thread_id=thread_id,
                        )
            else:
                if update.effective_chat:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="O ide non é válido",
                        message_thread_id=thread_id,
                    )


@async_only_dinner_chat
async def change_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Change menu command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    thread_id = await get_thread_id(update)

    try:
        data = await open_menu_file(update, context)
    except json.JSONDecodeError:
        return

    if (
        update.message
        and update.message.from_user
        and update.message.from_user.username in ADMINS
    ):
        if context.args and len(context.args) == 3:
            if context.args[0].isnumeric():
                item_id = int(context.args[0])
                name = context.args[1]
                price = context.args[2]

                if not price.isnumeric():
                    if update.effective_chat:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="O prezo debe ser un número válido.",
                            message_thread_id=thread_id,
                        )
                    return

                price = int(price)

                item_updated = False
                for item in data:
                    if item["id"] == item_id:
                        item.update({"Name": name, "Description": "", "Price": price})
                        item_updated = True
                        break

                if not item_updated:
                    data.append(
                        {"id": item_id, "Name": name, "Description": "", "Price": price}
                    )

                try:
                    with open("menu.json", "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                except IOError:
                    if update.effective_chat:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Erro ao gardar os cambios no arquivo de menú.",
                            message_thread_id=thread_id,
                        )
                    return

                message = "Menú cambiado." if item_updated else "Item agregado."
                if update.effective_chat:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=message,
                        message_thread_id=thread_id,
                    )
            else:
                if update.effective_chat:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="O IDE non é válido.",
                        message_thread_id=thread_id,
                    )
        else:
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Faltan argumentos para executar a función.",
                    message_thread_id=thread_id,
                )


async def open_menu_file(update, context):
    try:
        with open("menu.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        if update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Error al leer el archivo de menú.",
                message_thread_id=await get_thread_id(update),
            )
        raise e
    except FileNotFoundError:
        data = []
    return data


async def get_user(update):
    logger.info(
        "Get user function called",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    user = None
    if update.message and update.message.from_user:
        user = update.message.from_user
    elif update.callback_query and update.callback_query.from_user:
        user = update.callback_query.from_user

    if user is None:
        if update.effective_chat:
            await update.effective_chat.send_message(
                text="Necesítase un username ou nome en Telegram para interactuar co bot.",
                message_thread_id=await get_thread_id(update),
            )
        return None

    if user.username:
        request_user = user.username
    elif user.first_name:
        request_user = user.first_name
    else:
        if update.effective_chat:
            await update.effective_chat.send_message(
                text="Necesítase un username ou nome en Telegram para interactuar co bot.",
                message_thread_id=await get_thread_id(update),
            )
        return None
    return request_user


async def get_thread_id(update: Update):
    if update.effective_message:
        thread_id = update.effective_message.message_thread_id
        return thread_id
    return None
