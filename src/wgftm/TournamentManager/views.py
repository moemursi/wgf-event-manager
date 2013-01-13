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
         form = LoginForm()
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

   # Get all the tournaments for which the current user is a player
   inTourneys = Tournament.objects.filter(playersIn=curUser)
   # Get all the tournaments for which the current user is not a player
   notInTourneys = Tournament.objects.exclude(playersIn=curUser)
   return render(request, 'tm_viewuser.html', { 'data' : data , 'user' : curUser, 'usertype' : usertype, 'inTourneys' : inTourneys, 'notInTourneys' : notInTourneys })

#def view_teams(request):
   

#def add_team(request):
   
def tourneyDetail(request, tourney_id):
   t = None
   try:
      Tournament.objects.get(id=tourney_id)
   except ObjectDoesNotExist:
      errors = ["Tournament with id " + tourney_id + "does not exist!"]
      return render( request, 'tm_tourneydetail.html', { 'errors' : errors } )
   matches = Match.objects.filter(tournament=t)
   if not matches:
      errors = ["Tournament selected contains no matches to view."]
      return render( request, 'tm_tourneydetail.html', { 'errors' : errors } )
   
   # Find root match (i.e.: the final game, has no parent matches)
   root = None
   for match in matches:
      if match.matchWinners is None and match.matchLosers is None:
         root = match
         matches = matches.exclude(id=root.id)
         break
   
   if root is None:
      errors = ["ERROR: Tournament is malformed! Has no final match!"]
      return render( request, 'tm_tourneydetail.html', { 'errors' : errors } )
   
   
   
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

@login_required
def editProfile(request):
   curUser = request.user
   if request.method == 'POST':
      form = EditForm(request.POST)
      if form.is_valid():
         curUser.username = form.cleaned_data['username']
         curUser.first_name = form.cleaned_data['first_name']
         curUser.last_name = form.cleaned_data['last_name']
         curUser.set_password(form.cleaned_data['password'])
         curUser.isUcsd = form.cleaned_data['is_ucsd']
         curUser.isSixth = form.cleaned_data['is_sixth']
         curUser.save()
         return HttpResponseRedirect('/postedit/') # Redirect to thank you page
   else:
      form = EditForm(initial={'first_name': curUser.first_name, 'last_name': curUser.last_name, 
         'username': curUser.username, 'email': curUser.email, 'is_ucsd': Attendee.objects.get(user=curUser).isUcsd,
         'is_sixth': Attendee.objects.get(user=curUser).isSixth})
      
   return render(request, 'tm_editProfile.html', { 'form': form })

def postedit(request):
   return render(request, 'tm_postedit.html')
