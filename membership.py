from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import (
    BREAKING_CHANNEL,
    FOOTBALL_CHANNEL,
    WORLD_CHANNEL,
    REQUIRED_CHANNELS,
)


def channel_url(username: str) -> str:
    return f"https://t.me/{username.replace('@', '')}"


def join_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Breaking Sports News",
                    url=channel_url(BREAKING_CHANNEL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="⚽ Football Daily News",
                    url=channel_url(FOOTBALL_CHANNEL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏆 Sports World Update",
                    url=channel_url(WORLD_CHANNEL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ I've Joined",
                    callback_data="verify_join",
                )
            ],
        ]
    )


async def has_joined_all(bot, user_id):

    try:

        for channel in REQUIRED_CHANNELS:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user_id,
            )

            if member.status in ("left", "kicked"):
                return False

        return True

    except Exception as e:
        print(f"Membership check failed: {e}")
        return False
