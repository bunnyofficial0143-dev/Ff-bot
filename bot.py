import os
import logging
import base64
import httpx
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ============================================
# SETTINGS — এখানে তোমার token ও key বসাও
# ============================================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "এখানে_তোমার_telegram_token")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "এখানে_তোমার_gemini_key")
# ============================================

logging.basicConfig(level=logging.INFO)
genai.configure(api_key=GEMINI_API_KEY)

PROMPT = """You are extracting Free Fire (Battle Royale) match result data from a screenshot.

Extract ALL teams and players. Format EXACTLY like this:

TeamName:                     Rank: 1                    KillScore: 7                    RankScore: 12                    TotalScore: 19                   
NAME: PlayerName          ID: 1234567890           KILL: 3                   
NAME: PlayerName2         ID: 9876543210           KILL: 2                   

Rules:
- Keep special characters in names exactly as shown
- RankScore: Rank1=12, Rank2=9, Rank3=8, Rank4=7, Rank5=6, Rank6=5, Rank7=4, Rank8=3, Rank9=2, Rank10=1, below=0
- TotalScore = KillScore + RankScore
- If TeamName is blank, leave blank
- If player ID not visible, use 0000000000
- Output ONLY the formatted data, nothing else"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 FF Match Result Extractor Bot\n\n"
        "Match result এর screenshot পাঠাও — আমি .txt file বানিয়ে দেবো!\n\n"
        "📸 শুধু screenshot send করো"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Processing... একটু অপেক্ষা করো")

    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        async with httpx.AsyncClient() as client_http:
            resp = await client_http.get(file.file_path)
            img_bytes = resp.content

        import PIL.Image
        from io import BytesIO
        img = PIL.Image.open(BytesIO(img_bytes))

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([PROMPT, img])
        result_text = response.text.strip()

        file_bytes = BytesIO(result_text.encode("utf-8"))
        file_bytes.name = "MatchResult.txt"

        await update.message.reply_document(
            document=file_bytes,
            filename="MatchResult.txt",
            caption="✅ Match result extract হয়েছে!"
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 শুধু screenshot (photo) পাঠাও!")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(~filters.PHOTO & ~filters.COMMAND, handle_other))
    print("Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
