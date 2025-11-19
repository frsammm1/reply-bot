import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get credentials from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OWNER_ID = int(os.environ.get('OWNER_ID'))

# Store message mappings: {owner_message_id: user_chat_id}
message_map = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    user_id = update.effective_user.id
    
    if user_id == OWNER_ID:
        await update.message.reply_text(
            "👋 Welcome back, Sam! You're all set.\n\n"
            "Reply to any forwarded message to respond to users."
        )
    else:
        await update.message.reply_text(
            "👋 Hi! Please send a message to Sam, he'll reply soon."
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    user_id = update.effective_user.id
    message = update.message
    
    if user_id == OWNER_ID:
        # Owner is replying to a user
        if message.reply_to_message:
            replied_msg_id = message.reply_to_message.message_id
            
            if replied_msg_id in message_map:
                target_user_id = message_map[replied_msg_id]
                
                try:
                    # Send owner's reply to the user
                    if message.text:
                        await context.bot.send_message(
                            chat_id=target_user_id,
                            text=message.text
                        )
                    elif message.photo:
                        await context.bot.send_photo(
                            chat_id=target_user_id,
                            photo=message.photo[-1].file_id,
                            caption=message.caption
                        )
                    elif message.video:
                        await context.bot.send_video(
                            chat_id=target_user_id,
                            video=message.video.file_id,
                            caption=message.caption
                        )
                    elif message.document:
                        await context.bot.send_document(
                            chat_id=target_user_id,
                            document=message.document.file_id,
                            caption=message.caption
                        )
                    elif message.voice:
                        await context.bot.send_voice(
                            chat_id=target_user_id,
                            voice=message.voice.file_id
                        )
                    elif message.audio:
                        await context.bot.send_audio(
                            chat_id=target_user_id,
                            audio=message.audio.file_id,
                            caption=message.caption
                        )
                    
                    await message.reply_text("✅ Message sent!")
                    
                except Exception as e:
                    await message.reply_text(f"❌ Failed to send message: {str(e)}")
            else:
                await message.reply_text("⚠️ Cannot find the original sender. Please reply to a forwarded message.")
    else:
        # User is sending a message to owner
        user = update.effective_user
        username = f"@{user.username}" if user.username else "No username"
        full_name = user.full_name or "Unknown"
        
        # Create message header
        header = (
            f"📨 New message from:\n"
            f"👤 Name: {full_name}\n"
            f"🆔 ID: {user.id}\n"
            f"📱 Username: {username}\n"
            f"{'─' * 30}\n"
        )
        
        try:
            # Forward different types of messages
            if message.text:
                sent_msg = await context.bot.send_message(
                    chat_id=OWNER_ID,
                    text=f"{header}{message.text}"
                )
            elif message.photo:
                sent_msg = await context.bot.send_photo(
                    chat_id=OWNER_ID,
                    photo=message.photo[-1].file_id,
                    caption=f"{header}{message.caption or ''}"
                )
            elif message.video:
                sent_msg = await context.bot.send_video(
                    chat_id=OWNER_ID,
                    video=message.video.file_id,
                    caption=f"{header}{message.caption or ''}"
                )
            elif message.document:
                sent_msg = await context.bot.send_document(
                    chat_id=OWNER_ID,
                    document=message.document.file_id,
                    caption=f"{header}{message.caption or ''}"
                )
            elif message.voice:
                sent_msg = await context.bot.send_voice(
                    chat_id=OWNER_ID,
                    voice=message.voice.file_id,
                    caption=header
                )
            elif message.audio:
                sent_msg = await context.bot.send_audio(
                    chat_id=OWNER_ID,
                    audio=message.audio.file_id,
                    caption=f"{header}{message.caption or ''}"
                )
            elif message.sticker:
                await context.bot.send_message(
                    chat_id=OWNER_ID,
                    text=f"{header}[Sticker received]"
                )
                sent_msg = await context.bot.send_sticker(
                    chat_id=OWNER_ID,
                    sticker=message.sticker.file_id
                )
            else:
                sent_msg = await context.bot.send_message(
                    chat_id=OWNER_ID,
                    text=f"{header}[Unsupported message type]"
                )
            
            # Store mapping for replies
            message_map[sent_msg.message_id] = user_id
            
            await message.reply_text("✅ Your message has been sent to Sam. He'll reply soon!")
            
        except Exception as e:
            logger.error(f"Error forwarding message: {e}")
            await message.reply_text("❌ Sorry, there was an error sending your message. Please try again.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors"""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot"""
    if not BOT_TOKEN or not OWNER_ID:
        logger.error("BOT_TOKEN and OWNER_ID must be set in environment variables!")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("🤖 Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
