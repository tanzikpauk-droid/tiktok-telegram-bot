import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

TOKEN = os.getenv("BOT_TOKEN")

TIKTOK_REGEX = r"(https?://(www\.)?tiktok\.com/.+/video/\d+)"

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if not text or not re.search(TIKTOK_REGEX, text):
        update.message.reply_text("❌ Это не ссылка на TikTok видео")
        return

    update.message.reply_text("⏳ Скачиваю видео...")

    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "mp4",
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as f:
            update.message.reply_video(video=f)

        os.remove(filename)

    except Exception:
        update.message.reply_text("⚠️ Ошибка при скачивании видео")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "👋 Отправь ссылку на TikTok — я пришлю видео для скачивания 🎥"
    )

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
dp.add_handler(MessageHandler(Filters.command, start))

print("🤖 Бот запущен")
updater.start_polling()
updater.idle()
