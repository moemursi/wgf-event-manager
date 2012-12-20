from django.db import models
# Personel/attendee level models:
class Guest(models.Model):
   name = models.CharField(max_length=60)

class Player(models.Model):
   name = models.CharField(max_length=60)
   email = models.EmailField()
   phoneNumber = models.CharField(max_length=10)
   isUcsd = models.BooleanField()
   age = models.IntegerField()
   isBusy = models.BooleanField()
   tournamentsIn = models.ManyToManyField(Tournament)

# The PRIMARY administrator/s of the tournament
class TournamentLeader(models.Model):
   name = models.CharField(max_length=255)
   
# Someone who administrates a tournament, but does not make the primary
# decisions. A lackey.
class TournamentAssistant(models.Model):
   name = models.CharField(max_length=255)
   superior = models.ManyToManyField(TournamentLeader)
   
class Team:
   numOfPlayers = models.IntegerField()
   players = models.ForeignKey(Player)
   captain = models.OneToOneField(Player)
   metadata = models.IntegerField()
   
#   
# Event level models:
#
class Event(models.Model):
   name = models.CharField(max_length=255)
   headcount = models.IntegerField()
   
class Tournament(models.Model):
   event = models.ForeignKey(Event)
   name = models.CharField(max_length=255)
   date = models.TimeField()
   curNumTeams = models.IntegerField()
   maxNumTeams = models.IntegerField()
   tournamentLeaders = models.ManyToManyField(TournamentLeader)
   tournamentAssistants = models.ManyToManyField(TournamentAssitant)
   prizes = models.CharField(max_length=500)
   bracket = models.CharField(max_length=2048)
   
class Match(models.Model):
   tournament = models.ForeignKey(Tournament)
   name = models.CharField(max_length=255)
   teams = models.ManyToManyField(Team)
   winnerParent = models.OneToOneField(Match)
   loserParent = models.OneToOneField(Match)
   winners = models.ManyToManyField(Team)
   losers = models.ManyToManyField(Team)
   
#
# Games: a Match consists of any number of games
# CAN support round robin/pool play.
#   
class Game(models.Model):
   match = models.ForeignKey(Match) # The Match the Game is associated with
   teams = models.ManyToManyField(Team)
   verified = models.BooleanField()
   startTime = models.TimeField()
   winners = models.ManyToManyField(Team)
   losers = models.ManyToManyField(Team)