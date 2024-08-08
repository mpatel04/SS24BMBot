import logging
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler
from datetime import datetime
import pytz

from tokens import TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Time zone
desired_tz = pytz.timezone('America/New_York')

# Start date of the event
EVENT_START_DATE = 1

# Message will send when the user first uses the bot or logs out of their id
async def send_welcome_message(update: Update, context: CallbackContext) -> None:
    user_first_name = update.message.from_user.first_name
    welcome_message = (
        f'Jay Swaminarayan {user_first_name}bhai,\n\nWelcome to Bal Summer Shibir 2024! We are thrilled to have you join us for this exciting event. To make your experience as seamless as possible, I will be here to assist you every step of the way!'
    )

    image_path = 'Assets/splashlogo.jpg'
    if os.path.exists(image_path):
        with open(image_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=photo,
                caption=welcome_message
            )
    else:
        logger.error('Image file not found.')
        await context.bot.send_message(chat_id=update.message.chat_id, text=welcome_message)

# Sends the menu with all the buttons
async def send_start_message(chat_id: int, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Schedule", callback_data='schedule')],
        [InlineKeyboardButton("Emergency POCs", callback_data='poc')],
        [InlineKeyboardButton("Flow Maps", callback_data='flowmaps')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await context.bot.send_message(chat_id=chat_id, text='What would you like to know?', reply_markup=reply_markup)
    return message.message_id

# Inline keyboard for selecting days
async def send_days_keyboard(chat_id: int, context: CallbackContext) -> int:
    days_keyboard = [
        [InlineKeyboardButton("Day 1", callback_data=f'schedule_day1')],
        [InlineKeyboardButton("Day 2", callback_data=f'schedule_day2')],
        [InlineKeyboardButton("Day 3", callback_data=f'schedule_day3')],
        [InlineKeyboardButton("Day 4", callback_data=f'schedule_day4')]
    ]
    reply_markup = InlineKeyboardMarkup(days_keyboard)
    message = await context.bot.send_message(chat_id=chat_id, text='Select a day:', reply_markup=reply_markup)
    return message.message_id

async def send_flow_keyboard(chat_id: int, context: CallbackContext) -> int:
    flow_keyboard = [
        [InlineKeyboardButton("Site Map", callback_data=f'flow_map1')],
        [InlineKeyboardButton("Arrival Flow", callback_data=f'flow_map2')],
        [InlineKeyboardButton("Dining Flow", callback_data=f'flow_map3')],
        [InlineKeyboardButton("Hotel Departure Flow", callback_data=f'flow_map4')],
        [InlineKeyboardButton("Morning Arrival Flow", callback_data=f'flow_map5')],
        [InlineKeyboardButton("Group Activity Flow", callback_data=f'flow_map6')]
    ]
    reply_markup = InlineKeyboardMarkup(flow_keyboard)
    message = await context.bot.send_message(chat_id=chat_id, text='Select Flow Map:', reply_markup=reply_markup)
    return message.message_id

# Runs when /start is typed
async def start(update: Update, context: CallbackContext) -> None:
    await send_welcome_message(update, context)
    await asyncio.sleep(1)
    message_id = await send_start_message(update.message.chat_id, context)
    context.user_data['menu_message_id'] = message_id

# Runs whenever a button is pressed
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if 'menu_message_id' in context.user_data:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data['menu_message_id'])
        del context.user_data['menu_message_id']

    if 'day_selection_message_id' in context.user_data:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data['day_selection_message_id'])
        del context.user_data['day_selection_message_id']

    if 'flow_selection_message_id' in context.user_data:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data['flow_selection_message_id'])
        del context.user_data['flow_selection_message_id']

    if query.data == 'schedule':
        #message_id = await send_days_keyboard(query.message.chat_id, context)
        #context.user_data['day_selection_message_id'] = message_id

        media = [InputMediaPhoto(open(f'Assets/day1schedule.png', 'rb'))]
        caption = "Arrival Day Schedule"

        try:
            await context.bot.send_media_group(
                chat_id=query.message.chat_id,
                media=media
            )
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=caption
            )
        except Exception as e:
            logger.error(f'Error sending media: {e}')
            await query.message.reply_text(f'Error sending {caption}')

        return

    elif query.data == 'flowmaps':
        message_id_2 = await send_flow_keyboard(query.message.chat_id, context)
        context.user_data['flow_selection_message_id'] = message_id_2
        return

    


    elif query.data.startswith('flow_map'):

        if query.data == 'flow_map1':
            logger.info(f"Selected Flow Map 1")
            media = [InputMediaPhoto(open(f'Assets/flowMap1.png', 'rb'))]
            caption = "Site Map"

        elif query.data == 'flow_map2':
            logger.info(f"Selected Flow Map 2")
            media = [InputMediaPhoto(open(f'Assets/flowMap2.png', 'rb'))]
            caption = "Arrival Flow"

        elif query.data == 'flow_map3':
            logger.info(f"Selected Flow Map 3")
            media = [InputMediaPhoto(open(f'Assets/flowMap3.png', 'rb'))]
            caption = "Dining Flow"

        elif query.data == 'flow_map4':
            logger.info(f"Selected Flow Map 4")
            media = [InputMediaPhoto(open(f'Assets/flowMap4.png', 'rb'))]
            caption = "Hotel Departure Flow"

        elif query.data == 'flow_map5':
            logger.info(f"Selected Flow Map 5")
            media = [InputMediaPhoto(open(f'Assets/flowMap5.png', 'rb'))]
            caption = "Morning Arrival Flow"

        elif query.data == 'flow_map6':
            logger.info(f"Selected Flow Map 6")
            media = [InputMediaPhoto(open(f'Assets/flowMap6.png', 'rb'))]
            caption = "Group Activity Flow"

        try:
            await context.bot.send_media_group(
                chat_id=query.message.chat_id,
                media=media
            )
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=caption
            )
        except Exception as e:
            logger.error(f'Error sending media: {e}')
            await query.message.reply_text(f'Error sending {caption}')

    elif query.data == 'poc':
        message = "*Medical Emergencies:*\nPrimary Contact: TBD\nPhone Number: 123\-456\-7890"
        await query.message.reply_text(message, parse_mode='MarkdownV2')

    # Resend the inline keyboard after posting the content
    message_id = await send_start_message(query.message.chat_id, context)
    context.user_data['menu_message_id'] = message_id

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    button_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={},
        fallbacks=[]
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={},
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.add_handler(button_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
