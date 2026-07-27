import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from config import (
    BOT_TOKEN,
    CHECK_INTERVAL,
)

from membership import (
    has_joined_all,
    join_keyboard,
)

from database import db
from rss import RSSFetcher

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

# ==========================================
# START COMMAND
# ==========================================

@dp.message(CommandStart())
async def start(message: Message):

    db.add_user(message.from_user.id)

    joined = await has_joined_all(
        bot,
        message.from_user.id
    )

    if not joined:

        await message.answer(
            "🚫 <b>Access Denied</b>\n\n"
            "You must join all three channels before using this bot.\n\n"
            "After joining, tap <b>✅ I've Joined</b>.",
            reply_markup=join_keyboard(),
        )

        return

    await message.answer(
        "🏆 <b>Welcome to Sports News Auto Bot</b>\n\n"
        "✅ Verification successful.\n\n"
        "You'll now receive the latest sports updates."
    )

# ==========================================
# VERIFY BUTTON
# ==========================================

@dp.callback_query(F.data == "verify_join")
async def verify(callback: CallbackQuery):

    joined = await has_joined_all(
        bot,
        callback.from_user.id
    )

    if joined:

        db.add_user(callback.from_user.id)

        await callback.message.edit_text(
            "✅ <b>Verification Successful!</b>\n\n"
            "Welcome to Sports News Auto Bot."
        )

    else:

        await callback.answer(
            "❌ Please join all three channels first.",
            show_alert=True,
        )# ==========================================
# RSS POSTING ENGINE
# ==========================================

async def rss_worker():

    while True:

        try:

            articles = RSSFetcher.fetch_new_articles()

            if articles:

                logging.info(
                    f"Found {len(articles)} new article(s)."
                )

            for article in articles:

                try:

                    await bot.send_message(
                        chat_id=article["channel"],
                        text=article["message"],
                        disable_web_page_preview=False
                    )

                    db.save_post(
                        article["id"],
                        article["channel"]
                    )

                    logging.info(
                        f"Posted -> {article['channel']}"
                    )

                    # Small delay to avoid Telegram flood limits
                    await asyncio.sleep(2)

                except Exception as e:

                    logging.error(
                        f"Failed posting to {article['channel']}: {e}"
                    )

        except Exception as e:

            logging.error(
                f"RSS Worker Error: {e}"
            )

        await asyncio.sleep(CHECK_INTERVAL)


# ==========================================
# ADMIN COMMAND
# ==========================================

@dp.message(F.text == "/users")
async def users(message: Message):

    if message.from_user.id != 8856521475:
        return

    total = db.total_users()

    await message.answer(
        f"👥 Total Users: <b>{total}</b>"
    )# ==========================================
# STARTUP
# ==========================================

async def on_startup():

    logging.info("====================================")
    logging.info("SportsNewsAuto2026Bot Started")
    logging.info("RSS Monitor Running...")
    logging.info("====================================")

    asyncio.create_task(rss_worker())


# ==========================================
# MAIN
# ==========================================

async def main():

    await on_startup()

    await dp.start_polling(bot)


if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        logging.info("Bot stopped.")
