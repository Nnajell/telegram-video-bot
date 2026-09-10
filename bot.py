import os
import re
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ["8885274698:AAFvoRG9oNjms3plNq87WX9d-8SrtQpxs1o"]
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

URL_REGEX = re.compile(r'https?://\S+')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Kirim link video dari TikTok, X, YouTube, atau Instagram, "
        "nanti akan saya download dan kirim balik tanpa watermark."
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    match = URL_REGEX.search(text)
    if not match:
        await update.message.reply_text("Kirim link yang valid ya.")
        return

    url = match.group(0)
    msg = await update.message.reply_text("Sedang memproses, mohon tunggu...")

    filename = os.path.join(DOWNLOAD_DIR, f"{update.message.message_id}.mp4")

    ydl_opts = {
        "outtmpl": filename,
        "format": "mp4/best",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(filename):
            await update.message.reply_video(video=open(filename, "rb"))
            os.remove(filename)
        else:
            await msg.edit_text("Gagal mengunduh video. Cek kembali linknya.")
    except Exception as e:
        await msg.edit_text(f"Terjadi kesalahan: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()

if __name__ == "__main__":
    main()