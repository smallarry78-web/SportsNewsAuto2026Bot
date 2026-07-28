class NewsType:

    @staticmethod
    def detect(title: str) -> str:

        title = title.lower()

        # =====================================
        # TRANSFERS
        # =====================================

        transfer = [
            "transfer",
            "sign",
            "signs",
            "signed",
            "deal",
            "contract",
            "joins",
            "join",
            "loan",
            "medical",
            "bid",
            "release clause",
        ]

        # =====================================
        # MATCH RESULTS
        # =====================================

        result = [
            "beat",
            "beats",
            "defeat",
            "defeats",
            "defeated",
            "win",
            "wins",
            "won",
            "draw",
            "draws",
            "drawn",
            "lose",
            "loses",
            "lost",
            "victory",
            "result",
        ]

        # =====================================
        # INJURY
        # =====================================

        injury = [
            "injury",
            "injured",
            "injuries",
            "ruled out",
            "out for",
            "fitness",
            "hamstring",
            "knee",
            "ankle",
            "return date",
        ]

        # =====================================
        # LIVE
        # =====================================

        live = [
            "live",
            "live updates",
            "minute by minute",
        ]

        # =====================================
        # FOOTBALL
        # =====================================

        football = [
            "football",
            "premier league",
            "champions league",
            "arsenal",
            "chelsea",
            "liverpool",
            "manchester",
            "barcelona",
            "real madrid",
            "fifa",
            "uefa",
        ]

        # =====================================
        # NBA
        # =====================================

        nba = [
            "nba",
            "basketball",
            "lakers",
            "warriors",
            "celtics",
            "bucks",
        ]

        # =====================================
        # TENNIS
        # =====================================

        tennis = [
            "tennis",
            "atp",
            "wta",
            "wimbledon",
            "us open",
        ]

        # =====================================
        # FORMULA 1
        # =====================================

        formula = [
            "formula",
            "formula 1",
            "f1",
            "grand prix",
            "verstappen",
            "hamilton",
        ]

        # =====================================
        # DETECTION
        # =====================================

        if any(word in title for word in transfer):
            return "🔥 TRANSFER NEWS"

        if any(word in title for word in injury):
            return "🚑 INJURY UPDATE"

        if any(word in title for word in result):
            return "⚽ MATCH RESULT"

        if any(word in title for word in live):
            return "🔴 LIVE"

        if any(word in title for word in nba):
            return "🏀 NBA NEWS"

        if any(word in title for word in tennis):
            return "🎾 TENNIS"

        if any(word in title for word in formula):
            return "🏎 FORMULA 1"

        if any(word in title for word in football):
            return "⚽ FOOTBALL"

        return "🚨 BREAKING"
