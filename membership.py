from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import REQUIRED_CHANNELS


def join_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📢 Breaking Sports News",
                    url="https://t.me/breakingsportsnews"
                )
            ],

            [
                InlineKeyboardButton(
                    text="⚽ Football Daily News",
                    url="https://t.me/footballdnews"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏆 Sports World Update",
                    url="https://t.me/sportworldupdate"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✅ I've Joined",
                    callback_data="verify_join"
                )
            ]

        ]
    )


async def has_joined_all(bot, user_id):

    try:

        for channel in REQUIRED_CHANNELS:

            member = await bot.get_chat_member(
                chat_id=channel,
                user_id=user_id
            )

            if member.status in [
                "left",
                "kicked"
            ]:

                return False

        return True

    except Exception as e:

        print(e)

        return False
