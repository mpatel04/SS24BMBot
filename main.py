import logging
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler
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
        #[InlineKeyboardButton("Flow Maps", callback_data='flowmaps')],
        [InlineKeyboardButton("Program Seating", callback_data='seating')],
        [InlineKeyboardButton("GL Checkpoint Recaps", callback_data='recaps')],
        [InlineKeyboardButton("Parking Pass", callback_data='parking')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await context.bot.send_message(chat_id=chat_id, text='What would you like to know?', reply_markup=reply_markup)
    return message.message_id

async def send_flow_keyboard(chat_id: int, context: CallbackContext) -> int:
    flow_keyboard = [
        [InlineKeyboardButton("Site Map", callback_data=f'flow_map1')],
        [InlineKeyboardButton("Arrival Flow", callback_data=f'flow_map2')],
        [InlineKeyboardButton("Dining Flow", callback_data=f'flow_map3')],
        [InlineKeyboardButton("Hotel Departure Flow", callback_data=f'flow_map4')]
        #[InlineKeyboardButton("Morning Arrival Flow", callback_data=f'flow_map5')],
        #[InlineKeyboardButton("Group Activity Flow", callback_data=f'flow_map6')]
    ]
    reply_markup = InlineKeyboardMarkup(flow_keyboard)
    message = await context.bot.send_message(chat_id=chat_id, text='Select Flow Map:', reply_markup=reply_markup)
    return message.message_id

async def send_checkpoint_keyboard(chat_id: int, context: CallbackContext) -> int:
    checkpoint_keyboard = [
        [InlineKeyboardButton("Dharma", callback_data=f'checkpoint_recap1')],
        [InlineKeyboardButton("Gnan", callback_data=f'checkpoint_recap2')],
        [InlineKeyboardButton("Vairagya", callback_data=f'checkpoint_recap3')],
        [InlineKeyboardButton("Bhakti", callback_data=f'checkpoint_recap4')]
    ]
    reply_markup = InlineKeyboardMarkup(checkpoint_keyboard)
    message = await context.bot.send_message(chat_id=chat_id, text='Select Checkpoint:', reply_markup=reply_markup)
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

    # Clean up previous menus
    if 'menu_message_id' in context.user_data:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data['menu_message_id'])
        del context.user_data['menu_message_id']

    if 'flow_selection_message_id' in context.user_data:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data['flow_selection_message_id'])
        del context.user_data['flow_selection_message_id']

    if 'checkpoint_selection_message_id' in context.user_data:
        await context.bot.delete_message(chat_id=query.message.chat_id, message_id=context.user_data['checkpoint_selection_message_id'])
        del context.user_data['checkpoint_selection_message_id']

    if query.data == 'schedule':
        media = [
                   InputMediaPhoto(open(f'Assets/day2_1schedule.png', 'rb')),
                   InputMediaPhoto(open('Assets/day2_2schedule.png', 'rb'))
                ]
        caption = "Day 2 Schedule"

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

        # Resend the inline keyboard after posting the content
        message_id = await send_start_message(query.message.chat_id, context)
        context.user_data['menu_message_id'] = message_id

    elif query.data == 'seating':
        media = [InputMediaPhoto(open(f'Assets/Program2.jpg', 'rb'))]
        caption = "Program 2 Seating"

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

        # Resend the inline keyboard after posting the content
        message_id = await send_start_message(query.message.chat_id, context)
        context.user_data['menu_message_id'] = message_id

    elif query.data == 'parking':
        media = [InputMediaPhoto(open(f'Assets/ParkingPass.png', 'rb'))]
        caption = "Parking Pass"

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

        # Resend the inline keyboard after posting the content
        message_id = await send_start_message(query.message.chat_id, context)
        context.user_data['menu_message_id'] = message_id

    elif query.data == 'flowmaps':
        #message_id_2 = await send_flow_keyboard(query.message.chat_id, context)
        #context.user_data['flow_selection_message_id'] = message_id_2
        message_id = await send_start_message(query.message.chat_id, context)
        context.user_data['menu_message_id'] = message_id

    elif query.data == 'recaps':
        message_id_3 = await send_checkpoint_keyboard(query.message.chat_id, context)
        context.user_data['checkpoint_selection_message_id'] = message_id_3

    elif query.data.startswith('flow_map'):

        flow_map_paths = {
            'flow_map1': ('flowMap1.png', "Site Map"),
            'flow_map2': ('flowMap2.png', "Arrival Flow"),
            'flow_map3': ('flowMap3.png', "Dining Flow"),
            'flow_map4': ('flowMap4.png', "Hotel Departure Flow")
            #'flow_map5': ('flowMap5.png', "Morning Arrival Flow"),
            #'flow_map6': ('flowMap6.png', "Group Activity Flow")
        }

        selected_map = flow_map_paths.get(query.data)
        if selected_map:
            file_path, caption = selected_map
            if os.path.exists(f'Assets/{file_path}'):
                media = [InputMediaPhoto(open(f'Assets/{file_path}', 'rb'))]
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
            else:
                logger.error(f'File {file_path} not found.')
                await query.message.reply_text(f'Error: {caption} image not found.')

        # Resend the main inline keyboard after posting the content
        message_id = await send_start_message(query.message.chat_id, context)
        context.user_data['menu_message_id'] = message_id

    elif query.data.startswith('checkpoint_recap'):

        if query.data == 'checkpoint_recap1':
            media = [
                InputMediaPhoto(open('Assets/Dharma/1.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Dharma/2.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Dharma/3.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Dharma/4.jpg', 'rb'))
            ]
            caption = "Recap: Dharma Checkpoint"

        elif query.data == 'checkpoint_recap2':
            media = [
                InputMediaPhoto(open('Assets/Gnan/1.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Gnan/2.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Gnan/3.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Gnan/4.jpg', 'rb'))
            ]
            caption = "Recap: Gnan Checkpoint"

        elif query.data == 'checkpoint_recap3':
            media = [
                InputMediaPhoto(open('Assets/Vairagya/1.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Vairagya/2.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Vairagya/3.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Vairagya/4.jpg', 'rb'))
            ]
            caption = "Recap: Vairagya Checkpoint"

        elif query.data == 'checkpoint_recap4':
            media = [
                InputMediaPhoto(open('Assets/Bhakti/1.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Bhakti/2.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Bhakti/3.jpg', 'rb')),
                InputMediaPhoto(open('Assets/Bhakti/4.jpg', 'rb'))
            ]
            caption = "Recap: Bhakti Checkpoint"

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

        # Resend the main inline keyboard after posting the content
        message_id = await send_start_message(query.message.chat_id, context)
        context.user_data['menu_message_id'] = message_id

    elif query.data == 'poc':
        message = "*Medical Emergency Contact:*\nPrimary Contact: Dr\. Parth\nPhone Number: 732\-512\-7890\n\n*Emergency Security Number:*\nPhone Number: 609\-666\-9063"
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
