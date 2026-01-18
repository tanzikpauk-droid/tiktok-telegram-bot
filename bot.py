import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os
TOKEN = os.getenv("BOT_TOKEN")

TIKTOK_REGEX = r"(https?://(www\.)?tiktok\.com/.+/video/\d+)"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if not re.search(TIKTOK_REGEX, text):
        await update.message.reply_text("❌ Это не ссылка на TikTok видео")
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
        await update.message.reply_text("⚠️ Ошибка при скачивании видео")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Отправь ссылку на TikTok — я пришлю видео для скачивания 🎥"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.COMMAND, start))

print("🤖 Бот запущен")
app.run_polling()
