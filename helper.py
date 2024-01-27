from telebot.types import InlineKeyboardButton

bot_state = {}


def create_buttons(button_text, button_callback, url=None):
    return InlineKeyboardButton(button_text, callback_data=button_callback, url=url)


def wait_for_user_input(message):
    return bot_state.get(message.chat.id) == 'waiting_for_user_input'


close_button = create_buttons("Close", "close")
pin_button = create_buttons("Pin Message", "pin")
