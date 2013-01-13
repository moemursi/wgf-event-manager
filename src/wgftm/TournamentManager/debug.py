#
# General file for debugging classes
#

import datetime
from TournamentManager.models import *
from django.contrib.auth.models import User
from django.utils import timezone

#
# Generates dummy objects for every model in the app
# 
class dummyGenerator:
   #
   # Creates a dummy object in the database for every model we currently have
   # Update deleteDummies whenever this is modified, if needed
   #
   @staticmethod
   def createDummies():
      now = timezone.now()
      
      #Dummy keys:
      #  Referal: name = "Dummy Referal"
      #
      #  All the model types have these associated users
      #  User - Player 1: username = "dummyPlayer1"
      #  User - Player 2: username = "dummyPlayer2"
      #  User - Guest:  username = "dummyGuest"
      #  User - TL:     username = "dummyAdmin"
      #  User - TA:     username = "dummyHelper"
      #
      #  Event:         name = "Dummy Event"
      #  Tournament:    name = "Dummy Tournament"
      #  Team 1:        name = "Dummy Team 1"
      #  Team 2:        name = "Dummy Team 2"
      #  Match 1:       name = "Dummy Match 1"
      #  Match 2:       name = "Dummy Match 2"
      #  Result 1:      team = Team 1
      #  Result 2:      team = Team 2
      #  Game:          match.name = "Dummy Match"
      #  Checkin:       attendee.username = "dummyPlayer1"
      r = Referal(description = "Dummy Referal", alwaysShow = True)
      r.save()
      
      userPlayer1 = User.objects.create_user("dummyPlayer1", "dummy@dummy.com", "abc123")
      userPlayer1.first_name = "Dumb"
      userPlayer1.last_name = "Player"
      userPlayer1.save()
      
      userPlayer2 = User.objects.create_user("dummyPlayer2", "dummy@dummy.com", "abc123")
      userPlayer2.first_name = "Dumber"
      userPlayer2.last_name = "Player"
      userPlayer2.save()
      
      player1 = Player(user = userPlayer1, isUcsd = True, isSixth = True, gender = "Male", phoneNumber = "8675309")
      player1.save()
      player1.referals.add(r)
      player1.save()
      
      player2 = Player(user = userPlayer2, isUcsd = True, isSixth = True, gender = "Male", phoneNumber = "8675309")
      player2.save()
      player2.referals.add(r)
      player2.save()
      
      userGuest = User.objects.create_user("dummyGuest", "dummy@dummy.com", "abc123")
      userGuest.first_name = "Dumb"
      userGuest.last_name = "Guest"
      userGuest.save()
      
      guest = Guest(user = userGuest, isUcsd = True, isSixth = True, gender = "Male")
      guest.save()
      guest.referals.add(r)
      guest.save()
      
      userAdmin = User.objects.create_user("dummyAdmin", "dummy@dummy.com" "abc123")
      tl = TournamentLeader(user=userAdmin,contact="Meet me at the hole in the men's handicap stall restroom")
      tl.save()
      
      userAssistant = User.objects.create_user("dummyHelper", "dummy@dummy.com", "abc123")
      ta = TournamentAssistant(user=userAssistant, contact="On the hole in the men's handicap stall")
      ta.save()
      ta.superior.add(tl)
      ta.save()
      
      e = Event(name="Dummy Event")
      e.save()
      
      c = Checkin(attendee=player1, event=e)
      c.save()
      
      t = Tournament(event=e, name="Dummy Tournament", date = now, curNumTeams = 2, maxNumTeams = 2, maxTeamSize = 1, prizes="NOTHING!", isSeededByRank = True, bracket = "", chatChannel = "#dummies")
      t.save()
      t.tournamentLeaders.add(tl)
      t.tournamentAssistants.add(ta)
      t.playersIn.add(player1)
      t.playersIn.add(player2)
      t.save()
      
      team1 = Team(name="Dummy Team 1", tournament=t, numOfPlayers = 1, captain=player1, metadata = 1)
      team1.save()
      team1.players.add(player1)
      team1.save()
      
      team2 = Team(name="Dummy Team 2", tournament=t, numOfPlayers = 1, captain=player2, metadata = 2)
      team2.save()
      team2.players.add(player2)
      team2.save()

      #Dummy match to test game bubble up
      match2 = Match(tournament = t, description = "Dummy Match 2", winnerParent = None, loserParent = None)
      match2.save()
      
      match1 = Match(tournament = t, description = "Dummy Match 1", winnerParent = match2, loserParent = None)
      match1.save()
      match1.teams.add(team1)
      match1.teams.add(team2)
      match1.matchWinners.add(team1)
      match1.matchLosers.add(team2)
      match1.save()
      
      result1 = Result(team = team1, score = 1 )
      result1.save()
      result2 = Result(team = team2, score = 0 )
      result2.save()
      
      game = Game(match = match1, verified = True, startTime = now)
      game.save()
      game.teams.add(team1)
      game.teams.add(team2)
      game.results.add(result1)
      game.results.add(result2)
      game.save()

   @staticmethod
   # 
   # Deletes all dummy objects created by createDummies
   #
   def deleteDummies():
      #Dummy keys:
      #  Referal: name = "Dummy Referal"
      #
      #  All the model types have these associated users
      #  User - Player 1: username = "dummyPlayer1"
      #  User - Player 2: username = "dummyPlayer2"
      #  User - Guest:  username = "dummyGuest"
      #  User - TL:     username = "dummyAdmin"
      #  User - TA:     username = "dummyHelper"
      #
      #  Event:         name = "Dummy Event"
      #  Tournament:    name = "Dummy Tournament"
      #  Team 1:        name = "Dummy Team 1"
      #  Team 2:        name = "Dummy Team 2"
      #  Match 1:       name = "Dummy Match 1"
      #  Match 2:       name = "Dummy Match 2"
      #  Result 1:      team = Team 1
      #  Result 2:      team = Team 2
      #  Game:          match.name = "Dummy Match"
      #  Checkin:       attendee.username = "dummyPlayer1"
   
      Referal.objects.filter(description="Dummy Referal").delete()
      User.objects.filter(username="dummyPlayer1").delete()
      User.objects.filter(username="dummyPlayer2").delete()
      User.objects.filter(username="dummyGuest").delete()
      User.objects.filter(username="dummyAdmin").delete()
      User.objects.filter(username="dummyHelper").delete()
      Event.objects.filter(name="Dummy Event").delete()