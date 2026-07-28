class LeagueDetector:

    LEAGUES = {

        "Premier League": [
            "premier league",
            "epl",
        ],

        "Champions League": [
            "champions league",
            "ucl",
        ],

        "Europa League": [
            "europa league",
        ],

        "Conference League": [
            "conference league",
        ],

        "FA Cup": [
            "fa cup",
        ],

        "Carabao Cup": [
            "carabao cup",
            "league cup",
        ],

        "La Liga": [
            "la liga",
        ],

        "Serie A": [
            "serie a",
        ],

        "Bundesliga": [
            "bundesliga",
        ],

        "Ligue 1": [
            "ligue 1",
        ],

        "MLS": [
            "mls",
            "major league soccer",
        ],

        "NBA": [
            "nba",
        ],

        "WNBA": [
            "wnba",
        ],

        "ATP Tour": [
            "atp",
            "atp tour",
        ],

        "WTA Tour": [
            "wta",
            "wta tour",
        ],

        "Wimbledon": [
            "wimbledon",
        ],

        "US Open": [
            "us open",
        ],

        "Australian Open": [
            "australian open",
        ],

        "French Open": [
            "roland garros",
            "french open",
        ],

        "Formula 1": [
            "formula 1",
            "formula one",
            "f1",
        ],

        "MotoGP": [
            "motogp",
        ],

        "UFC": [
            "ufc",
        ],

        "Cricket": [
            "cricket",
            "icc",
        ],
    }

    @staticmethod
    def detect(title: str):

        title = title.lower()

        leagues = []

        for league, keywords in LeagueDetector.LEAGUES.items():

            if any(keyword in title for keyword in keywords):
                leagues.append(league)

        return leagues
