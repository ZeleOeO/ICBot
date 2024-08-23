import os
from telebot.async_telebot import AsyncTeleBot, types
from telebot.types import InlineKeyboardMarkup, ForceReply
from dotenv import load_dotenv
from prompt import get_prompt
import helper as helper
from transactions import Transaction
from user import User

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_TOKEN = "" if BOT_TOKEN is None else BOT_TOKEN

bot = AsyncTeleBot(BOT_TOKEN)
force_reply_markup = ForceReply(selective=False)


@bot.message_handler(commands=["start", "hello"])
async def start(message: types.Message):
    start_menu = InlineKeyboardMarkup(row_width=8)

    set_wallet_phrase = helper.create_buttons(
        "Set Wallet Phrase", "set_wallet_phrase")
    check_wallet = helper.create_buttons("Wallet", "check_wallet")
    buy_button = helper.create_buttons("Buy Tokens", "buy_tokens")
    sell_button = helper.create_buttons("Sell & Manage", "sell_tokens")
    help_button = helper.create_buttons("Help", "help")
    refer_friends_button = helper.create_buttons(
        "Refer Friends", "refer_friends")
    alerts_button = helper.create_buttons(
        "Alerts", "alerts", url="https://t.me/Official_ICP/"
    )

    print(message.from_user.username)

    if helper.global_user.username == "":
        start_menu.row(set_wallet_phrase)

    start_menu.row(check_wallet)
    start_menu.row(buy_button, sell_button)
    start_menu.row(refer_friends_button, alerts_button)
    start_menu.row(help_button, helper.pin_button)

    target_prompt = get_prompt("ICP-Start", message.from_user.username)
    target_prompt = "" if target_prompt is None else target_prompt

    await helper.send_message(bot,
                              message.chat.id,
                              target_prompt,
                              reply_markup=start_menu,
                              parse_mode="markdown",
                              )


async def set_wallet_phrase(message: types.Message):
    await helper.send_message(bot, message.chat.id, "Enter your secret phrase")
    helper.bot_state[message.chat.id] = "waiting_for_secret_phrase"


@bot.message_handler(
    func=lambda message: helper.bot_state.get(message.chat.id)
    == "waiting_for_secret_phrase"
)
async def respond_to_secret_phrase(message: types.Message):
    message.text = "" if message.text is None else message.text
    helper.user_secrets[message.chat.username] = message.text
    await helper.send_message(bot, message.chat.id, "Secret key set")

    helper.global_user.set_username(message.from_user.username)

    helper.bot_state[message.chat.id] = ""
    await wallet(message)


@bot.message_handler(commands=["wallet"])
async def wallet(message: types.Message):
    print(helper.global_user.wallet_address)
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

    await helper.send_message(bot,
                              message.chat.id,
                              get_prompt("Wallet-Menu",
                                         message.from_user.username),
                              reply_markup=wallet_menu,
                              parse_mode="markdown",
                              )


async def buy(message: types.Message):
    # user = User(message.from_user.id)
    buy_menu = InlineKeyboardMarkup(row_width=8)

    buy_menu.row(helper.close_button)

    await helper.send_message(bot,
                              message.chat.id,
                              get_prompt(
                                  "Buy-Menu", message.from_user.username),
                              reply_markup=buy_menu,
                              parse_mode="markdown",
                              )
    if message.from_user.is_bot is False:
        await helper.send_message(bot,
                                  message.chat.id, f"the token_address you sent is {
                                      message.text}"
                                  )


async def sell(message: types.Message):
    sell_menu = InlineKeyboardMarkup(row_width=8)

    sell_menu.row(helper.close_button)

    await helper.send_message(bot,
                              message.chat.id,
                              get_prompt(
                                  "Sell-Menu", message.from_user.username),
                              reply_markup=sell_menu,
                              parse_mode="markdown",
                              )


@bot.message_handler(commands=["/help", "/assist"])
async def help(message: types.Message):
    help_menu = InlineKeyboardMarkup(row_width=8)

    help_menu.row(helper.close_button)

    await helper.send_message(bot,
                              message.chat.id,
                              get_prompt(
                                  "Help-Menu", message.from_user.username),
                              reply_markup=help_menu,
                              parse_mode="markdown",
                              )


async def refer(message: types.Message):
    refer_menu = InlineKeyboardMarkup(row_width=8)

    refer_menu.row(helper.close_button)

    await helper.send_message(bot,
                              message.chat.id,
                              get_prompt(
                                  "Refer-Menu", message.from_user.username),
                              reply_markup=refer_menu,
                              parse_mode="markdown",
                              )


async def deposit_icp(message: types.Message):
    await helper.send_message(bot,
                              message.chat.id, text="To deposit send ICP to the following adress"
                              )
    await helper.send_message(bot,
                              message.chat.id, text=f"`{helper.global_user.wallet_address}`", parse_mode="markdown"
                              )
    helper.global_user.set_balance(200.00)


async def withdraw_all_icp(message: types.Message):
    helper.bot_state[message.chat.id] = "waiting_for_destination"
    await handle_reply_wait_for_destination(message)


async def withdraw_x_icp(message: types.Message):
    helper.bot_state[message.chat.id] = "waiting_for_amount"
    await handle_reply_wait_for_amount(message)


async def pin(message: types.Message):
    await bot.pin_chat_message(message.chat.id, message.message_id)


async def close(message: types.Message):
    print(helper.global_chat_id)
    await helper.delete_messages(bot)


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


@bot.message_handler(
    func=lambda message: helper.bot_state.get(
        message.chat.id) == "waiting_for_amount"
)
async def handle_reply_wait_for_amount(message: types.Message):
    chat_id = message.chat.id
    text = "You don't have any ICTokens at the moment\nTry depositing tokens to your wallet" if helper.global_user.balance == 0 else f"""Reply with the amount (0 - {
        helper.global_user.balance}) to deposit"""

    await helper.send_message(bot,
                              chat_id,
                              text,
                              reply_markup=force_reply_markup if helper.global_user.balance > 0 else None,
                              )

    # Update user state
    if helper.global_user.balance > 0:
        helper.bot_state[chat_id] = "waiting_for_amount_response"

    await start(message)


@bot.message_handler(
    func=lambda message: helper.bot_state.get(message.chat.id)
    == "waiting_for_amount_response"
)
async def handle_amount_response(message: types.Message):
    print("Handling amount response...")
    chat_id = message.chat.id

    transaction = Transaction()

    message.text = "" if message.text is None else ""

    if message.from_user.is_bot:
        return

    transaction.amount = int(message.text)
    print("Amount", Transaction.amount)

    # Perform further processing, e.g., validate the amount

    # Update user state to next step
    helper.bot_state[chat_id] = "waiting_for_destination"
    await handle_reply_wait_for_destination(message)


@bot.message_handler(
    func=lambda message: helper.bot_state.get(message.chat.id)
    == "waiting_for_destination"
)
async def handle_reply_wait_for_destination(message: types.Message):
    chat_id = message.chat.id

    if message.from_user.is_bot:
        return

    await helper.send_message(bot,
                              chat_id,
                              text="Reply with the destination address",
                              reply_markup=force_reply_markup,
                              )

    # Update user state
    helper.bot_state[chat_id] = "waiting_for_destination_response"


@bot.message_handler(
    func=lambda message: helper.bot_state.get(message.chat.id)
    == "waiting_for_destination_response"
)
async def handle_destination_response(message: types.Message):
    chat_id = message.chat.id
    message.text = "" if message.text is None else message.text

    transaction = Transaction()

    if message.from_user.is_bot:
        return

    transaction.des_address = message.text
    print("Address", transaction.des_address)

    # Perform further processing, e.g., validate the destination address

    # Reset the state
    helper.bot_state.pop(chat_id, None)

    # Continue with additional logic if needed


# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
