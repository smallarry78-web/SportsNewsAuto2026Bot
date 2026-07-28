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
    ADMIN_ID,
)

from membership import (
    has_joined_all,
    join_keyboard,
)

from database import db
from rss import RSSFetcher
from publisher import Publisher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()


# =====================================================
# START COMMAND
# =====================================================

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
            "You must join all required channels before using this bot.\n\n"
            "After joining, tap <b>✅ I've Joined</b>.",
            reply_markup=join_keyboard(),
        )

        return

    await message.answer(
        "🏆 <b>Welcome to Sports News Auto Bot</b>\n\n"
        "✅ Verification successful.\n\n"
        "You'll now receive the latest sports updates."
    )


# =====================================================
# VERIFY BUTTON
# =====================================================

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
            "❌ Please join all required channels first.",
            show_alert=True,
        )


# =====================================================
# RSS ENGINE
# =====================================================

async def rss_worker():

    while True:

        try:

            articles = RSSFetcher.fetch_new_articles()

            if articles:

                logging.info(
                    f"Found {len(articles)} new article(s)."
                )

            for article in articles:

                success = await Publisher.publish(
                    bot,
                    article
                )

                if success:

                    db.save_post(
                        article["id"],
                        article["channel"]
                    )

                await asyncio.sleep(2)

        except Exception as e:

            logging.exception(
                f"RSS Worker Error: {e}"
            )

        await asyncio.sleep(CHECK_INTERVAL)


# =====================================================
# ADMIN
# =====================================================

@dp.message(F.text == "/users")
async def users(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    total = db.total_users()

    await message.answer(
        f"👥 <b>Total Users:</b> {total}"
    )


# =====================================================
# STARTUP
# =====================================================

async def on_startup():

    logging.info("=" * 50)
    logging.info("SportsNewsAuto2026Bot Started")
    logging.info("RSS Monitor Running")
    logging.info("=" * 50)

    asyncio.create_task(
        rss_worker()
    )


# =====================================================
# MAIN
# =====================================================

async def main():

    await on_startup()

    await dp.start_polling(bot)


if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        logging.info("Bot stopped.")
