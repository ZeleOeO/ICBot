import asyncio
from telebot.async_telebot import types
import message_handler

bot = message_handler.bot


def get_handler(call_data: str):
    match call_data:
        case "check_wallet": return message_handler.wallet
        case "buy_tokens": return message_handler.buy
        case "sell_tokens": return message_handler.sell
        case "help": return message_handler.help
        case "refer_friends": return message_handler.refer
        case "deposit_icp": return message_handler.deposit_icp
        case "withdraw_all_icp": return message_handler.withdraw_all_icp
        case "withdraw_x_icp": return message_handler.withdraw_x_icp
        case "pin": return message_handler.pin
        case "close": return message_handler.close
        case _: return message_handler.unknown_handler


@bot.callback_query_handler(func=lambda call: True)
async def handle_button_click(call):

    handler = get_handler(call.data)
    await handler(call.message)


# To start the function
message_handler.start(types.Message)

# To keep the stuff running, asyncrhonously
asyncio.run(bot.polling())
