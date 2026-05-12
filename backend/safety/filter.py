import re


class SafetyFilter:

    def __init__(self):

        # Unsafe keywords
        self.banned_words = {
            "hate",
            "violence",
            "kill",
            "murder",
            "terror",
            "bomb",
            "abuse",
            "suicide"
        }

        self.block_message = (
            "⚠️ Content blocked for safety reasons."
        )

    def clean_text(self, text):

        text = text.lower()

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        return text

    def check(self, text):

        text = self.clean_text(text)

        # Match complete words only
        words = re.findall(r"\b\w+\b", text)

        for word in words:

            if word in self.banned_words:
                return False

        return True

    def apply(self, text):

        if self.check(text):
            return text

        return self.block_message