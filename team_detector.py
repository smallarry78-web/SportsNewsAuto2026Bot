class TeamDetector:

    TEAMS = {

        # =========================
        # ENGLAND
        # =========================

        "Liverpool": [
            "liverpool",
            "lfc",
        ],

        "Arsenal": [
            "arsenal",
            "gunners",
        ],

        "Chelsea": [
            "chelsea",
            "blues",
        ],

        "Manchester City": [
            "manchester city",
            "man city",
            "city",
        ],

        "Manchester United": [
            "manchester united",
            "man utd",
            "man united",
            "united",
        ],

        "Tottenham": [
            "tottenham",
            "spurs",
        ],

        "Newcastle": [
            "newcastle",
        ],

        "Aston Villa": [
            "aston villa",
            "villa",
        ],

        # =========================
        # SPAIN
        # =========================

        "Real Madrid": [
            "real madrid",
        ],

        "Barcelona": [
            "barcelona",
            "barca",
        ],

        "Atletico Madrid": [
            "atletico madrid",
            "atlético madrid",
        ],

        # =========================
        # ITALY
        # =========================

        "Juventus": [
            "juventus",
        ],

        "Inter Milan": [
            "inter milan",
            "inter",
        ],

        "AC Milan": [
            "ac milan",
            "milan",
        ],

        "Napoli": [
            "napoli",
        ],

        # =========================
        # FRANCE
        # =========================

        "PSG": [
            "psg",
            "paris saint-germain",
        ],

        # =========================
        # GERMANY
        # =========================

        "Bayern Munich": [
            "bayern",
            "bayern munich",
        ],

        "Borussia Dortmund": [
            "dortmund",
            "borussia dortmund",
        ],

        # =========================
        # NBA
        # =========================

        "Lakers": [
            "lakers",
            "los angeles lakers",
        ],

        "Warriors": [
            "warriors",
            "golden state warriors",
        ],

        "Celtics": [
            "celtics",
            "boston celtics",
        ],

        "Bucks": [
            "bucks",
            "milwaukee bucks",
        ],

        "Knicks": [
            "knicks",
            "new york knicks",
        ],

        "Heat": [
            "heat",
            "miami heat",
        ],

        # =========================
        # FORMULA 1
        # =========================

        "Ferrari": [
            "ferrari",
        ],

        "Mercedes": [
            "mercedes",
        ],

        "Red Bull": [
            "red bull",
        ],

        "McLaren": [
            "mclaren",
        ],
    }

    @staticmethod
    def detect(title: str):

        title = title.lower()

        found = []

        for team, keywords in TeamDetector.TEAMS.items():

            if any(keyword in title for keyword in keywords):
                found.append(team)

        return found
