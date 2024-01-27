import os
from telebot.async_telebot import AsyncTeleBot, types
from telebot.types import InlineKeyboardMarkup, ForceReply
from dotenv import load_dotenv
import prompt
import helper
from transactions import Transaction
from user import User

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = AsyncTeleBot(BOT_TOKEN)
force_reply_markup = ForceReply(selective=False)


@bot.message_handler(commands=["start", "hello"])
async def start(message: types.Message):
    start_menu = InlineKeyboardMarkup(row_width=8)

    check_wallet = helper.create_buttons("Wallet", "check_wallet")
    buy_button = helper.create_buttons("Buy Tokens", "buy_tokens")
    sell_button = helper.create_buttons("Sell & Manage", "sell_tokens")
    help_button = helper.create_buttons("Help", "help")
    refer_friends_button = helper.create_buttons(
        "Refer Friends", "refer_friends")
    alerts_button = helper.create_buttons(
        "Alerts", "alerts", url="https://t.me/Official_ICP/"
    )

    start_menu.row(check_wallet)
    start_menu.row(buy_button, sell_button)
    start_menu.row(refer_friends_button, alerts_button)
    start_menu.row(help_button, helper.pin_button)

    await bot.send_message(
        message.chat.id,
        prompt.prompt.get("ICP-Start"),
        reply_markup=start_menu,
        parse_mode="markdown",
    )


async def wallet(message: types.Message):
    wallet_menu = InlineKeyboardMarkup(row_width=8)

    deposit_icp_button = helper.create_buttons("Deposit ICP", "deposit_icp")
    withdraw_all_icp_button = helper.create_buttons(
        "Withdraw all ICP", "withdraw_all_icp"
    )
    withdraw_x_icp_button = helper.create_buttons(
        "Withdraw X ICP", "withdraw_x_icp")

    wallet_menu.row(deposit_icp_button)
    wallet_menu.row(withdraw_x_icp_button, withdraw_all_icp_button)
    wallet_menu.row(helper.pin_button, helper.close_button)

    await bot.send_message(
        message.chat.id,
        prompt.prompt.get("Wallet-Menu"),
        reply_markup=wallet_menu,
        parse_mode="markdown",
    )


async def buy(message: types.Message):
    user = User(message.from_user.id)
    buy_menu = InlineKeyboardMarkup(row_width=8)

    buy_menu.row(helper.close_button)

    await bot.send_message(
        message.chat.id,
        prompt.prompt.get("Buy-Menu"),
        reply_markup=buy_menu,
        parse_mode="markdown",
    )
    if message.from_user.is_bot is False:
        await bot.send_message(message.chat.id, f"the token_address you sent is {message.text}")


async def sell(message: types.Message):
    sell_menu = InlineKeyboardMarkup(row_width=8)

    sell_menu.row(helper.close_button)

    await bot.send_message(
        message.chat.id,
        prompt.prompt.get("Sell-Menu"),
        reply_markup=sell_menu,
        parse_mode="markdown",
    )


@bot.message_handler(commands=["/help", "/assist"])
async def help(message: types.Message):
    help_menu = InlineKeyboardMarkup(row_width=8)

    help_menu.row(helper.close_button)

    await bot.send_message(
        message.chat.id,
        prompt.prompt.get("Help-Menu"),
        reply_markup=help_menu,
        parse_mode="markdown",
    )


async def refer(message: types.Message):
    refer_menu = InlineKeyboardMarkup(row_width=8)

    refer_menu.row(helper.close_button)

    await bot.send_message(
        message.chat.id,
        prompt.prompt.get("Refer-Menu"),
        reply_markup=refer_menu,
        parse_mode="markdown",
    )


async def deposit_icp(message: types.Message):
    user = User(message.from_user.id)
    await bot.send_message(
        message.chat.id, text="To deposit send ICP to the following adress"
    )
    await bot.send_message(
        message.chat.id, text=f"`{user.wallet_address}`", parse_mode="markdown"
    )


async def withdraw_all_icp(message: types.Message):
    helper.bot_state[message.chat.id] = "waiting_for_destination"
    await handle_reply_wait_for_destination(message)


async def withdraw_x_icp(message: types.Message):
    helper.bot_state[message.chat.id] = "waiting_for_amount"
    await handle_reply_wait_for_amount(message)


async def pin(message: types.Message):
    await bot.pin_chat_message(message.chat.id, message.message_id)


async def close(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


async def unknown_handler(message: types.Message):
    print("Unkown handler", message.text)


# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# THIS SECTION BELOW IS FOR HANDLING THE REFERRAL MENU AND FUNCTIONS
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
async def get_refer_link(message: types.Message):
    return str(message.from_user.id)

# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# THE SECTION BELOW IS FOR HANDLING PRIMARLY RESPONSES LIKE THE ONES MESSAGED ABOVE
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------


@bot.message_handler(func=lambda message: helper.bot_state.get(message.chat.id) == "waiting_for_amount")
async def handle_reply_wait_for_amount(message: types.Message):
    user = User(message.from_user.id)
    chat_id = message.chat.id

    await bot.send_message(
        chat_id,
        text=f"Reply with the amount (0 - {user.balance}) to deposit",
        reply_markup=force_reply_markup
    )

    # Update user state
    helper.bot_state[chat_id] = "waiting_for_amount_response"


@bot.message_handler(func=lambda message: helper.bot_state.get(message.chat.id) == "waiting_for_amount_response")
async def handle_amount_response(message: types.Message):
    print("Handling amount response...")
    chat_id = message.chat.id

    if message.from_user.is_bot:
        return

    Transaction.amount = message.text
    print("Amount", Transaction.amount)

    # Perform further processing, e.g., validate the amount

    # Update user state to next step
    helper.bot_state[chat_id] = "waiting_for_destination"
    await handle_reply_wait_for_destination(message)


@bot.message_handler(func=lambda message: helper.bot_state.get(message.chat.id) == "waiting_for_destination")
async def handle_reply_wait_for_destination(message: types.Message):
    chat_id = message.chat.id

    if message.from_user.is_bot:
        return

    await bot.send_message(
        chat_id,
        text="Reply with the destination address",
        reply_markup=force_reply_markup,
    )

    # Update user state
    helper.bot_state[chat_id] = "waiting_for_destination_response"


@bot.message_handler(func=lambda message: helper.bot_state.get(message.chat.id) == "waiting_for_destination_response")
async def handle_destination_response(message: types.Message):
    chat_id = message.chat.id

    if message.from_user.is_bot:
        return

    Transaction.des_address = message.text
    print("Address", Transaction.des_address)

    # Perform further processing, e.g., validate the destination address

    # Reset the state
    helper.bot_state.pop(chat_id, None)

    # Continue with additional logic if needed
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
