from django.db import models
from django.contrib.auth.models import User

# Referal:
class Referal(models.Model):
   description = models.CharField(max_length=255)
   alwaysShow = models.BooleanField()

#
# Personel/attendee level models:
#

# Attendee: someone who goes to WGF
# first name, last name, e-mail, login/password fields are already included
class Attendee(models.Model):
   user = models.OneToOneField(User)
   isUcsd = models.BooleanField()                        # Is the player a UCSD student?
   isSixth = models.BooleanField()                       # Is this player from Sixth?
   gender = models.CharField(max_length=30)              # What is this attendee's gender?
   referals = models.ManyToManyField(Referal)            # How did this attendee hear about WGF?

# Checkins of an attendee at an event
class Checkin(models.Model):
    attendee = models.ForeignKey(Attendee)              # The person who checked in
    event = models.ForeignKey(Event)                    # The event checked into

# Guest: a user who is not a player
class Guest(Attendee):
      
   def __unicode__(self):
      return "User: " + self.user.username + " | Name: " + self.user.first_name + " " + self.user.last_name
   
# Player: A user who is a player in the Event.
class Player(Attendee):
   phoneNumber = models.CharField(max_length=10)         # Optional field                 
   #isBusy = models.BooleanField()                        # Is the player CURRENTLY busy - may be used for something

   def __unicode__(self):
      return "User: " + self.user.username + " | Name: " + self.user.first_name + " " + self.user.last_name

#   
# Event level models:
#

# TL: The PRIMARY administrator/s of the tournament
class TournamentLeader(models.Model):
   user = models.OneToOneField(User)
   contact = models.CharField(max_length=255)        # Aggregate contact information here
   
# TA: Someone who administrates a tournament, but does not make the primary
# decisions. A lackey.
class TournamentAssistant(models.Model):
   user = models.OneToOneField(User)
   superior = models.ManyToManyField(TournamentLeader)   # Who is the TL for this person?
   contact = models.CharField(max_length=255)        # Aggregate contact information here

# Event: The highest level of the Tournament. 
class Event(models.Model):                               
   name = models.CharField(max_length=255)               # The name of the tournament.
   
# Tournament: a tournament for a single game.
class Tournament(models.Model):
   event = models.ForeignKey(Event)                      # What Event does this Tournament belong to?
   name = models.CharField(max_length=255)               # Tournament name
   date = models.TimeField()                             # Tournament date
   curNumTeams = models.IntegerField()                   # What is the current number of teams in this tournament?
   maxNumTeams = models.IntegerField()                   # The maximum number of teams in this tournament?
   maxTeamSize = models.IntegerField()                   # What is the maximum number of players on a team in this tournament?
   tournamentLeaders = models.ManyToManyField(TournamentLeader)         # Who are the TLs?
   tournamentAssistants = models.ManyToManyField(TournamentAssistant)   # Who are the TAs?
   prizes = models.CharField(max_length=500)             # Textfield for prizes
   isSeededByRank = models.BooleanField()                # Is this tournament seeded according to rank (metadata)?
   bracket = models.CharField(max_length=1024)           # Bracket field - contains a string describing the current state/structure of the tournament
   playersIn = models.ManyToManyField(Player)            # What Players are in the Tournament?
   chatChannel = models.CharField(max_length=30)                      # What chat channel in-game should players join?

# Team: Can be a single player or a collection of players, but ONLY teams are part of Games. The participants
# in a game
class Team(models.Model):
   name = models.CharField(max_length=30)                               # What is the name of this team?
   tournament = models.ForeignKey(Tournament)                           # What tournament is this team playing in?
   numOfPlayers = models.IntegerField()                                 # How many players are on this team?
   players = models.ManyToManyField(Player, related_name = 'players')   # What players are on the this team?
   captain = models.ForeignKey(Player, related_name = 'captain')        # Who is the team captain? 
   metadata = models.IntegerField()                                     # Data for matchmaking - if a matchmaking algorithm is specified, use this to determine rankings
   
# Match: single Match for the tournament (one node of the tournament) - a Match can consist of many games
class Match(models.Model):
   tournament = models.ForeignKey(Tournament)            # What tournament does this match belong to?
   description = models.CharField(max_length=64)         # What is this match's description? 
   teams = models.ManyToManyField(Team)                  # What teams are participaiting?
   winnerParent = models.OneToOneField('self', related_name = '+', verbose_name = 'match for winners')   # Where should the winners go?
   loserParent = models.OneToOneField('self', related_name = '+', verbose_name = 'match for losers')     # Where should the losers go?
   matchWinners = models.ManyToManyField(Team, related_name = 'matchWinners', verbose_name = 'teams who won the match') # Who are the winners?
   matchLosers = models.ManyToManyField(Team, related_name = 'matchLosers', verbose_name = 'teams who lost the match')  # Who are the losers?

# Results: results of all teams in a game
class Result(models.Model):
   team = models.ForeignKey(Team)   # The team whose score is here
   score = models.IntegerField()    # The score of the team
   
# Games: a Match consists of any number of games
# CAN support round robin/pool play.
class Game(models.Model):
   match = models.ForeignKey(Match)                                  # The Match the Game is associated with
   teams = models.ManyToManyField(Team, related_name = 'teams')      # Who are the teams in this game (may be more than just 2)
   verified = models.BooleanField()                                  # Has the game been verified?
   startTime = models.TimeField()                                    # When should the game start?
   gameWinners = models.ManyToManyField(Team, related_name = 'gameWinners', verbose_name = 'teams who won the game')  # Who were the winners?
   gameLosers = models.ManyToManyField(Team, related_name = 'gameLosers', verbose_name = 'teams who lost the game')    # Who were the losers?
   results = models.ManyToManyField(Result)                          # Score results of teams in this game

