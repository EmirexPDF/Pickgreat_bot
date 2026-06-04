import os
import random
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send introduction message."""
    await update.message.reply_text(
        "✨ **Welcome to Pickgreat_bot!** ✨\n\n"
        "Stuck making a decision? Let me choose the absolute best option for you.\n\n"
        "📥 **How to use:**\n"
        "Simply send me your options separated by commas.\n"
        "👉 *Example: Pizza, Burgers, Sushi, Tacos*"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message."""
    await update.message.reply_text("Just type out your choices separated by a comma (`,`) and I will pick the greatest one!")

async def pick_option(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process the user text, split by commas, and pick the best option."""
    text = update.message.text

    # Split the input text by commas and strip out extra spaces
    options = [opt.strip() for opt in text.split(",") if opt.strip()]

    # If there's only one option or it's empty
    if len(options) < 2:
        await update.message.reply_text(
            "⚠️ Please provide at least **two** choices separated by a comma so I can pick the best one!\n"
            "👉 *Example: Watch a movie, Read a book, Go for a walk*"
        )
        return

    # Let the user know the bot is thinking
    await update.message.reply_chat_action(action="typing")

    # Pick the "greatest" option
    chosen_selection = random.choice(options)

    # Celebratory phrases to match the "excellent decision" theme
    hype_phrases = [
        "🏆 Excellent choice! The absolute best option is:",
        "✨ A phenomenal decision has been made. Go with:",
        "🔥 After careful consideration, the winning pick is:",
        "🎯 You've picked great! The top option is definitely:"
    ]
    intro_phrase = random.choice(hype_phrases)

    # Reply with the result
    response_message = f"{intro_phrase}\n\n👑 **{chosen_selection}** 👑"
    await update.message.reply_text(response_message, parse_mode="Markdown")

def main() -> None:
    """Start Pickgreat_bot."""
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found in environment variables!")
        return

    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, pick_option))

    # Run bot via polling
    application.run_polling()

if __name__ == "__main__":
    main()
