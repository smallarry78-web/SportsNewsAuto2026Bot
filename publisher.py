import logging

from image_extractor import ImageExtractor


class Publisher:

    @staticmethod
    async def publish(bot, article):

        entry = article["entry"]

        channel = article["channel"]

        message = article["message"]

        image = ImageExtractor.get_image(entry)

        try:

            if image:

                await bot.send_photo(
                    chat_id=channel,
                    photo=image,
                    caption=message,
                    parse_mode="HTML"
                )

                logging.info(
                    f"Photo posted -> {channel}"
                )

            else:

                await bot.send_message(
                    chat_id=channel,
                    text=message,
                    disable_web_page_preview=False
                )

                logging.info(
                    f"Text posted -> {channel}"
                )

            return True

        except Exception as e:

            logging.warning(
                f"Photo failed ({channel}): {e}"
            )

            try:

                await bot.send_message(
                    chat_id=channel,
                    text=message,
                    disable_web_page_preview=False
                )

                logging.info(
                    f"Fallback text posted -> {channel}"
                )

                return True

            except Exception as err:

                logging.error(
                    f"Publishing failed ({channel}): {err}"
                )

                return False
