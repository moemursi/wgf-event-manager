class NoMatchesInTourney(Exception):
    def __str__(self):
        return "No matches are in this tournament yet."

class TourneyMalformed(Exception):
    def __str__(self):
        return "Tournament is malformed!"
   