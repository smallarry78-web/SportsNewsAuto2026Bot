class Hashtags:

    @staticmethod
    def generate(title: str) -> str:

        title = title.lower()

        tags = []

        keywords = {

            "#Football": [
                "football",
                "premier league",
                "champions league",
                "fifa",
                "uefa",
            ],

            "#NBA": [
                "nba",
                "basketball",
            ],

            "#Tennis": [
                "tennis",
                "wimbledon",
                "atp",
                "wta",
                "us open",
                "roland garros",
            ],

            "#Formula1": [
                "formula 1",
                "formula",
                "f1",
                "grand prix",
            ],

            "#Liverpool": [
                "liverpool",
            ],

            "#Arsenal": [
                "arsenal",
            ],

            "#Chelsea": [
                "chelsea",
            ],

            "#ManchesterCity": [
                "manchester city",
                "man city",
            ],

            "#ManchesterUnited": [
                "manchester united",
                "man utd",
                "man united",
            ],

            "#RealMadrid": [
                "real madrid",
            ],

            "#Barcelona": [
                "barcelona",
            ],

            "#PSG": [
                "psg",
                "paris saint-germain",
            ],

            "#Juventus": [
                "juventus",
            ],

            "#InterMilan": [
                "inter milan",
                "inter",
            ],

            "#PremierLeague": [
                "premier league",
            ],

            "#ChampionsLeague": [
                "champions league",
            ],

            "#LaLiga": [
                "la liga",
            ],

            "#SerieA": [
                "serie a",
            ],

            "#Bundesliga": [
                "bundesliga",
            ],

            "#Lakers": [
                "lakers",
            ],

            "#Warriors": [
                "warriors",
            ],

            "#Celtics": [
                "celtics",
            ],

            "#Bucks": [
                "bucks",
            ],

            "#Ferrari": [
                "ferrari",
            ],

            "#RedBull": [
                "red bull",
            ],

            "#Mercedes": [
                "mercedes",
            ],
        }

        for tag, words in keywords.items():

            if any(word in title for word in words):
                tags.append(tag)

        if not tags:
            tags.append("#Sports")

        return " ".join(dict.fromkeys(tags))
