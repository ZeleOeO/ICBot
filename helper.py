from typing import List, Optional, Union
import telebot.types as types
from user import User
from telebot.async_telebot import AsyncTeleBot

bot_state = {}

user_secrets: dict[str, str] = {}

global_user = User()

global_chat_id = 0
global_message_ids = []


async def send_message(bot: AsyncTeleBot, chat_id: Union[int, str], text: str,
                       parse_mode: Optional[str] = None,
                       entities: Optional[List[types.MessageEntity]] = None,
                       disable_web_page_preview: Optional[bool] = None,
                       disable_notification: Optional[bool] = None,
                       protect_content: Optional[bool] = None,
                       reply_to_message_id: Optional[int] = None,
                       allow_sending_without_reply: Optional[bool] = None,
                       reply_markup=None,
                       timeout: Optional[int] = None,
                       message_thread_id: Optional[int] = None,
                       reply_parameters: Optional[types.ReplyParameters] = None,
                       link_preview_options: Optional[types.LinkPreviewOptions] = None,
                       business_connection_id: Optional[str] = None):
    """
    Handles message actions
    """
    global global_chat_id
    global_chat_id = chat_id
    sent_message = await bot.send_message(chat_id, text, reply_markup=reply_markup,
                                          timeout=timeout, protect_content=protect_content, parse_mode=parse_mode,
                                          entities=entities, disable_web_page_preview=disable_web_page_preview,
                                          disable_notification=disable_notification, reply_to_message_id=reply_to_message_id,
                                          allow_sending_without_reply=allow_sending_without_reply,
                                          message_thread_id=message_thread_id, reply_parameters=reply_parameters,
                                          link_preview_options=link_preview_options, business_connection_id=business_connection_id
                                          )
    global_message_ids.append(sent_message.message_id)


async def delete_messages(bot: AsyncTeleBot):
    "Handles delete messages"
    await bot.delete_messages(global_chat_id, global_message_ids)


def create_buttons(button_text, button_callback, url=None):
    "Creates a Button on an InlineKeyboardButton"
    return types.InlineKeyboardButton(button_text, callback_data=button_callback, url=url)


def wait_for_user_input(message):
    "Changes the state of the bot when waiting for users input"
    return bot_state.get(message.chat.id) == 'waiting_for_user_input'


close_button = create_buttons("Close", "close")
pin_button = create_buttons("Pin Message", "pin")
