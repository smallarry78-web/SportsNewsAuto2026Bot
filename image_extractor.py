import re


class ImageExtractor:

    @staticmethod
    def get_image(entry):

        # -----------------------------
        # media_content
        # -----------------------------
        if hasattr(entry, "media_content"):

            media = entry.media_content

            if media:

                image = media[0].get("url")

                if image:
                    return image

        # -----------------------------
        # media_thumbnail
        # -----------------------------
        if hasattr(entry, "media_thumbnail"):

            media = entry.media_thumbnail

            if media:

                image = media[0].get("url")

                if image:
                    return image

        # -----------------------------
        # enclosure
        # -----------------------------
        if hasattr(entry, "links"):

            for link in entry.links:

                if link.get("type", "").startswith("image"):

                    image = link.get("href")

                    if image:
                        return image

        # -----------------------------
        # Search inside summary HTML
        # -----------------------------
        summary = ""

        if hasattr(entry, "summary"):
            summary = entry.summary

        elif hasattr(entry, "description"):
            summary = entry.description

        if summary:

            match = re.search(
                r'<img[^>]+src="([^"]+)"',
                summary
            )

            if match:
                return match.group(1)

        # No image found
        return None
