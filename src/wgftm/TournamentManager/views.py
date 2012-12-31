from django.template import Context, loader
from django.shortcuts import render
from django.http import HttpResponse
from TournamentManager.models import Player
from TournamentManager.models import Guest
from TournamentManager.forms import RegistrationForm
from django.contrib.auth.models import User

# Create your views here.
#def login(request):
   

#def logout(request):
   

#def view_teams(request):
   

#def add_team(request):
   

#def tournament_detail(request):
   

#def view_tournaments(request):
   

def register(request):
   if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
         formUser = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
         formUser.first_name = form.cleaned_data['first_name']
         formUser.last_name = form.cleaned_data['last_name']
         if(form.cleaned_data['is_player']):
            player = Player(user = formUser, isUcsd = form.cleaned_data['is_ucsd'], age=20, isBusy = False, ucsdCollege='ItsASecret', phoneNumber = '1234567890')
            player.save()
         else:
            guest = Guest(user = formUser, isUcsd = form.cleaned_data['is_ucsd'])
            guest.save()
         formUser.save()
         
   else:
      form = RegistrationForm()
      
   return render(request, 'tm_register.html', { 'form': form })
