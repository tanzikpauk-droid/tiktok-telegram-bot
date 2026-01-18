import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")

TIKTOK_REGEX = r"https?://(www\.)?tiktok\.com/.*"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Отправь ссылку на TikTok — я пришлю видео для скачивания"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not re.search(TIKTOK_REGEX, text):
        await update.message.reply_text("❌ Это не ссылка TikTok")
        return

    await update.message.reply_text("⏳ Скачиваю видео...")

    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "mp4",
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(filename, "rb"))
        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
    
