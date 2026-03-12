import os
import logging
import httpx
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

logging.basicConfig(level=logging.INFO)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT = """Extract Free Fire match result data from this screenshot.

Format EXACTLY like this example:

TeamName:                     Rank: 1                    KillScore: 7                    RankScore: 12                    TotalScore: 19                   
NAME: PlayerName          ID: 1234567890           KILL: 3                   
NAME: PlayerName2         ID: 9876543210           KILL: 2                   
NAME: PlayerName3         ID: 1111111111           KILL: 1                   
NAME: PlayerName4         ID: 2222222222           KILL: 1                   
TeamName:                      Rank: 2                    KillScore: 5                    RankScore: 9                    TotalScore: 14                   
NAME: PlayerName          ID: 3333333333           KILL: 3                   

Rules:
- Keep ALL special characters in player names exactly as shown
- RankScore: Rank1=12, Rank2=9, Rank3=8, Rank4=7, Rank5=6, Rank6=5, Rank7=4, Rank8=3, Rank9=2, Rank10=1, others=0
- TotalScore = KillScore + RankScore
- If TeamName blank, leave blank
- If player ID not visible, write 0000000000
- Output ONLY the formatted data, nothing else"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 FF Match Result Bot\n\nMatch result এর screenshot পাঠাও → .txt file পাবে!\n\n📸 শুধু photo send করো"
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Processing... একটু অপেক্ষা করো")
    try:
        photo = update.message.photo[-1]
        tg_file = await context.bot.get_file(photo.file_id)

        async with httpx.AsyncClient() as c:
            resp = await c.get(tg_file.file_path)
            img_bytes = resp.content

        img = Image.open(BytesIO(img_bytes))
        response = model.generate_content([PROMPT, img])
        result_text = response.text.strip()

        out = BytesIO(result_text.encode("utf-8"))
        out.name = "MatchResult.txt"

        await update.message.reply_document(
            document=out,
            filename="MatchResult.txt",
            caption="✅ Done!"
        )
    except Exception as e:
        logging.error(e)
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 শুধু screenshot (photo) পাঠাও!")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(~filters.PHOTO & ~filters.COMMAND, handle_other))
    print("Bot started!")
    app.run_polling()
