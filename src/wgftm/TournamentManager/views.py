from django.template import Context, loader

from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from TournamentManager.forms import *
from TournamentManager.models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



# Create your views here.
def tm_login(request):
   if request.method == 'POST':
      form = LoginForm(request.POST)
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(username=username, password=password)
      if user is not None:
         login(request, user)
         return HttpResponseRedirect('/viewuser/')
      else:
         #Bad login
         logout(request)
         return render(request, 'tm_login.html', { 'form' : form, 'status' : 'invalid' })  
   else:
      logout(request)
      form = LoginForm()
      return render(request, 'tm_login.html', { 'form' : form, 'next' : '/viewuser/' })

def tm_logout(request):
   logout(request)
   return HttpResponseRedirect('/postlogout/')

@login_required   
def viewuser(request):
   curUser = request.user
   player = None
   guest = None

   try:
      player = Player.objects.get(user=curUser) 
   except Player.DoesNotExist:
      player = None

   try:
      guest = Guest.objects.get(user=curUser)   
   except Guest.DoesNotExist:
      guest = None

   if player is not None:
      usertype = 'player'
      data = player
   elif guest is not None:
      usertype = 'guest'
      data = guest
   return render(request, 'tm_viewuser.html', { 'data' : data , 'user' : curUser, 'usertype' : usertype})

#def view_teams(request):
   

#def add_team(request):
   
def tourneyDetail(request, tourney_id):
   t = None
   try:
      Tournament.objects.get(id=tourney_id)
   except ObjectDoesNotExist:
      errors = ["Tournament with id " + tourney_id + "does not exist!"]
      return render( request, 'tm_tourneydetail.html', { 'errors' : errors } )
   
   # After this, matches should be sorted into an in-order tier list
   # Figure out how many rows, how many columns you need
   
@login_required
def viewTourneys(request):
   curUser = request.user
   # Get all the tournaments for which the current user is a player
   inTourneys = Tournament.objects.filter(playersIn=curUser)
   # Get all the tournaments for which the current user is not a player
   notInTourneys = Tournament.objects.exclude(playersIn=curUser)
   
   return render( request, 'tm_viewtourneys.html', { 'inTourneys' : inTourneys , 'notInTourneys' : notInTourneys } )
   
  
def postregister(request):
   return render(request, 'tm_postregister.html')

def postlogout(request):
   return render(request, 'tm_postlogout.html')
  
def register(request):
   if request.method == 'POST':
      form = RegistrationForm(request.POST)
      if form.is_valid():
         formUser = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
         formUser.first_name = form.cleaned_data['first_name']
         formUser.last_name = form.cleaned_data['last_name']
         if(form.cleaned_data['is_player']):
            player = Player(user = formUser, isUcsd = form.cleaned_data['is_ucsd'], age = form.cleaned_data['age'], isBusy = form.cleaned_data['age'], isSixth=form.cleaned_data['is_sixth'], phoneNumber = '1234567890')
            player.save()
         else:
            guest = Guest(user = formUser, isUcsd = form.cleaned_data['is_ucsd'])
            guest.save()
         formUser.save()
         return HttpResponseRedirect('/postregister/') # Redirect to thank you page
   else:
      form = RegistrationForm()
      
   return render(request, 'tm_register.html', { 'form': form })