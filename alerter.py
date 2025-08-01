import telegram
import asyncio
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

async def send_telegram_message(token, chat_id, message):
    """Asynchronously sends a message to a Telegram chat."""
    try:
        bot = telegram.Bot(token=token)
        await bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')
        return True
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")
        return False

def send_alert(message: str):
    """
    [cite_start]Wrapper to send a Telegram alert for signals or errors[cite: 34].
    
    Args:
        message (str): The message to be sent.
    """
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            # Running the async function in a blocking way for script simplicity
            success = asyncio.run(send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message))
            return success
        except RuntimeError: # Handles 'cannot run loop while another is running' in some environments like Jupyter
            try:
                loop = asyncio.get_event_loop()
                task = loop.create_task(send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message))
                return True
            except Exception as e:
                print(f"Failed to send Telegram alert: {e}")
                return False
    else:
        print("Telegram credentials not configured. Skipping alert.")
        return False