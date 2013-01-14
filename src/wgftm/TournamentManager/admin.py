from TournamentManager.models import Referal, Attendee, Guest, Player, TournamentLeader, TournamentAssistant, Event, Checkin, Tournament, Team, Match, Result, Game

from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.db import transaction

class ReferalAdmin(admin.ModelAdmin):
    list_display = ('description', 'alwaysShow')
admin.site.register(Referal, ReferalAdmin)

class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'isUcsd', 'isSixth', 'gender')
    #TODO: list referals
admin.site.register(Attendee, AttendeeAdmin)

class GuestAdmin(admin.ModelAdmin):
    list_display = ('user', 'isUcsd', 'isSixth', 'gender')
admin.site.register(Guest, GuestAdmin)

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'isUcsd', 'isSixth', 'gender', 'phoneNumber',)
admin.site.register(Player, PlayerAdmin)

class TournamentLeaderAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact')
admin.site.register(TournamentLeader, TournamentLeaderAdmin)

class TournamentAssistantAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact')
admin.site.register(TournamentAssistant, TournamentAssistantAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Event, EventAdmin)

class CheckinAdmin(admin.ModelAdmin):
    list_display = ('event', 'attendee')
admin.site.register(Checkin, CheckinAdmin)

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'date', 'curNumTeams', 'maxTeamSize', 'prizes', 'isSeededByRank', 'chatChannel')
admin.site.register(Tournament, TournamentAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'numOfPlayers', 'captain', 'metadata')
admin.site.register(Team, TeamAdmin)

class MatchAdmin(admin.ModelAdmin):
    list_display = ('tournament', 'description', 'winnerParent', 'loserParent')
admin.site.register(Match, MatchAdmin)

class ResultAdmin(admin.ModelAdmin):
    list_display = ('team', 'score')
admin.site.register(Result, ResultAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display = ('match', 'verified', 'startTime')
admin.site.register(Game, GameAdmin)
