from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from .models import Game
from .models import Scores
from .models import Gameplay
from .models import PlayerItem
from .models import UserProfile
from .models import Transaction
from .models import Comment
from .models import DeveloperGame
from .files import *
from django.forms.models import model_to_dict
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
import json
from django.http import JsonResponse
from hashlib import md5
import cloudinary, cloudinary.uploader, cloudinary.forms
import datetime
from datetime import date, timedelta, datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#For banking service
secret_key = "26d3858162e10dc081f786319f286025" #This is from the secret key generator they provided. Dunno if this is the right way to put it

import cloudinary, cloudinary.uploader, cloudinary.api
#from cloudinary.uploader import upload
#from cloudinary.utils import cloudinary_url
#from cloudinary.api import delete_resources_by_tag, resources_by_tag
from django import forms
from cloudinary.forms import cl_init_js_callbacks
#from .models import GameImage, ProfileImage
#from .files import GameImageForm, ProfileImageForm
from .files import UploadPhoto
from cloudinary.models import CloudinaryField
import string
import random

cloudinary.config(
  cloud_name = "sakshyam",
  api_key = "623965587187774",
  api_secret = "Lf7ULK0njrZJlVdwopnjsMeLdfM"
)


#For Email Verification
fromaddr='wsdAwsomeProject@gmail.com'
username=fromaddr
password='reljathegreat'

def random_string_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@login_required(login_url ='/login/')
def registerForAPI(request):
    user = UserProfile.objects.get(user=request.user)
    if user.isDeveloper:
        # If user has unchanged key, assign him new one
        # If user has already requested key, just reming him what is it
        if user.key == "":
            user.key = random_string_generator()
            user.save()
        return render(request, "registration/api.html", {"key" : user.key})
    else:
        return HttpResponse(status=404)

def searchGamesAPI(request):
    #Cheeck identity through API key
    try:
        user = UserProfile.objects.get(key=request.GET['key'])
    except UserProfile.DoesNotExist:
        user = None

    # GET requests are only valid ones
    if request.method == "GET" and 'key' in request.GET and request.GET['key'] != "" and user != None:
        #q is gane of the game, if ommited, all games are shown
        if 'q' not in request.GET:
            games = Game.objects.all()
        else:
            games = Game.objects.all().filter(name=request.GET['q'])
        response = {"games" : []}
        for game in games:
            # .first() is only used to force database call
            developer = DeveloperGame.objects.all().filter(game=game).first()
            #highScore data is None unless the game has scores
            highScore = 'None'
            highScoreUser = 'None'
            if Gameplay.objects.all().filter(game=game).exists(): #if the game has an entry in the Gameplay table (i.e. there is a score)
                #then calculate the highScore
                Gameplays = Gameplay.objects.all().filter(game=game)
                scores = []
                for gameplayInstance in Gameplays:
                    scores.append(gameplayInstance.score)
                highScore = max(scores)
                highScoreUser = Gameplay.objects.get(score=highScore).user.username

            response["games"].append({"name" : game.name, "description" : game.description, "price" : game.price, "category" : game.category,
                "created" : game.created, "developed by" : developer.user.username, "High Score": highScore, "High Score User": highScoreUser })
        return JsonResponse({"response" : response})
    else:
        return JsonResponse({"response" : "Did you register to use API?"})

def searchGameSalesAPI(request):
    #Check identity through API key
    try:
        user = UserProfile.objects.get(key=request.GET['key'])
    except UserProfile.DoesNotExist:
        user = None
    # GET requests are only valid ones for simplicity sake

    if request.method == "GET" and 'key' in request.GET and request.GET['key'] != "" and user != None:
        if 'q' not in request.GET:
            games = Game.objects.all()
        else:
            games = Game.objects.all().filter(name=request.GET['q'])
        response = {"games" : []}
        for game in games:
            # first() is used to force database call
            developer = DeveloperGame.objects.all().filter(game=game).first()
            buyersAndTimestamps = []
            if Transaction.objects.all().filter(game=game, status='completed').exists(): #if the game has an entry in the Transactions table (i.e. someone bought it)
                #then assign the transation values
                Purchases = Transaction.objects.all().filter(game=game, status='completed') #Querying from the transactions game table all objects whose game matches game_name
                for purchase in Purchases:
                    buyersAndTimestamps.append({"bought by" : purchase.user.username, "on" : purchase.timestamp})

            response["games"].append({"name" : game.name, "price" : game.price, "category" : game.category,
                "created" : game.created, "developed by" : developer.user.username, "sales" : buyersAndTimestamps}) #"transactions": transactions issues with zip: not json serializeable
        return JsonResponse({"response" : response})
    else:
        return JsonResponse({"response" : "Did you register to use API?"})


def searchHighScoresAPI(request):
    #Check identity through API key
    try:
        user = UserProfile.objects.get(key=request.GET['key'])
    except UserProfile.DoesNotExist:
        user = None
    # GET requests are only valid ones for simplicity sake
    if request.method == "GET" and 'key' in request.GET and request.GET['key'] != "" and user != None:
        if 'q' not in request.GET:
            games = Game.objects.all()
        else:
            games = Game.objects.all().filter(name=request.GET['q'])
        response = {"games" :[]}
        for game in games:
            scores = Scores.objects.all().filter(game=game).order_by("-score")
            scoreList = []
            for score in scores:
                scoreList.append({'user' : score.user.username, "score": score.score})
            response["games"].append({"name" : game.name, "scores" : scoreList})
        return JsonResponse({"response": response})
    else:
        return JsonResponse({"response" : "Did you register to use API?"})


# Landing page showing recent uploaded games
def home(request):
    enddate = date.today()
    startdate = enddate - timedelta(days=31)
    games = Game.objects.filter(created__range=[startdate, enddate])
    return render(request, 'home.html', {'games': games })

@login_required(login_url='/login/')
def createGitHubProfile(request):
    try:
        userProfile = UserProfile.objects.get(user = request.user)
    except UserProfile.DoesNotExist:
        userProfile = None

    if userProfile == None:
        gitHubUser = UserProfile(user = request.user, isDeveloper = True)
        gitHubUser.save()

    return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def myProfile(request):
	userProfile = UserProfile.objects.get(user=request.user)
	context = dict( backend_form = UploadGameForm())

	if userProfile.isDeveloper:
		if request.method == 'POST':
			form = UploadGameForm(request.POST, request.FILES)
			context['posted'] = form.instance
			success = False
			if form.is_valid():
				#game = Game(name=form.cleaned_data['name'], url=form.cleaned_data['url'], price=form.cleaned_data['price'], description=form.cleaned_data['description'], image=form.cleaned_data['image'])
				#game.save()
				#form = UploadGameForm()
				success = True
				form.save()
				devGame = DeveloperGame(user=request.user, game=Game.objects.get(name=form.cleaned_data['name']))
				devGame.save()
				form = UploadGameForm()
				context = UploadGameForm()
		else:
			form = UploadGameForm()
			success = False

		DeveloperGames = DeveloperGame.objects.all().filter(user=request.user)
		#Querying from the developer game table all objects whose user matches request.user
		games = []
		numberOfPurchasesList = []
		for developerGame in DeveloperGames:
			#put the games in a list
			games.append(developerGame.game) # developerGame is an instance (a row in the database table) of DeveloperGames
			#print(games)
			Purchases = Transaction.objects.all().filter(game=developerGame.game, status='completed')	# Querying from the Transaction table
																					# all transactions objects with games matching the chosen game
			numberOfPurchasesList.append(len(Purchases))

		gamePurchases = zip(games, numberOfPurchasesList)	# gamePurchases referes to no of people purchased a game
		#gamePurchases.append

		PurchasedGames = Transaction.objects.all().filter(user=request.user, status='completed') #accessing purchased games list from Transaction Table
		purchasedGames = []
		purchasedWhen = []
		counts = []
		i = 0
		for boughtGame in PurchasedGames:
			purchasedGames.append(boughtGame.game)
			purchasedWhen.append(boughtGame.timestamp)
			i += 1
			counts.append(i)

		boughtGames = zip(purchasedGames, purchasedWhen, counts)	#boughtGame refers to no. of games the user bought

		return render(request, "myProfile.html", {"userProfile" : userProfile, "form" : form, "success" : success,
						"context" : context, "gamePurchases": gamePurchases, "boughtGames": boughtGames })

	else:
		#All games the user purchased
		PurchasedGames = Transaction.objects.all().filter(user=request.user, status='completed') #accessing purchased games list from Transaction Table
		purchasedGames = []
		purchasedWhen = []
		counts = []
		i = 0
		for boughtGame in PurchasedGames:
			purchasedGames.append(boughtGame.game)
			purchasedWhen.append(boughtGame.timestamp)
			i += 1
			counts.append(i)

		boughtGames = zip(purchasedGames, purchasedWhen, counts)	#boughtGame refers to no. of games the user bought

		return render(request, "myProfile.html", {"userProfile" : userProfile, "boughtGames": boughtGames })


@login_required(login_url='/login/')
@csrf_protect
def editProfile(request):
	if request.method == 'POST':
		form = UpdateProfileForm(data=request.POST, instance=request.user)
		success = False
		if form.is_valid():
			update = form.save(commit=False)
			update.set_password(form.cleaned_data['password'])
			success = True
			update.save()
			#User.objects.get().update(email=form.cleaned_data['email'], password=form.cleaned_data['password1'])
	else:
		form = UpdateProfileForm()
		success = False
	return render(request, "editProfile.html", {'form' : form, "success":success} )

def browseGames(request):
    all = Game.objects.all()
    action = all.filter(category='Action')
    adventure = all.filter(category='Adventure')
    sports = all.filter(category='Sports')
    strategy = all.filter(category='Strategy')
    puzzle = all.filter(category='Puzzle')
    return render(request, "browseGames.html", {"action" : action, "adventure" : adventure, "sports" : sports, "strategy" : strategy, "puzzle" : puzzle, "all" : all })


# About page- introduction to the project and Team members
def about(request):
    return render(request, "about.html", {})


@login_required(login_url='/login/')
def buyGame(request, game_name):
        #I am defining the variables here and then the buyGame.html will only have the variable names
        #This is querying the game object with the name parameter
        game = Game.objects.get(name = game_name)  #game primary key to be queried from the game table
        pid = random_string_generator()
        sid = "pandareljasharbel" #this is fxed for our service
        amount = game.price #this is game price queried form game table

        if  Transaction.objects.filter(game=game, user=request.user, status = "ongoing").exists(): #if the user hasn already gone to the transaction page previously
            transaction = Transaction.objects.get(game=game, user=request.user, status = "ongoing")
            transaction.pid = pid
            transaction.save()
        else:
            transaction = Transaction(user = request.user, game = game, pid = pid) #create a transaction row for them with the status "in process
        #The next three could e implemented in one url and then the response parameter from the paymen service will be different
        success_url = request.build_absolute_uri("../payment")
        cancel_url =  success_url
        error_url =  success_url

        #The checksum is calculated from pid, sid, amount, and your secret key. The string is formed like this:
        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)

        # checksumstr is the string concatenated above
        m = md5(checksumstr.encode("ascii"))
        # checksum is the value that should be used in the payment request
        checksum = m.hexdigest()




        return render(request, "buyGame.html", {"pid": pid, "sid":sid, "amount":amount,
            "success_url": success_url, "cancel_url":cancel_url, "error_url":error_url,
            "checksum":checksum, "game_name":game_name})

#TODO: implement the different pages for the different results
@login_required
def buyGameResult(request,game_name):
    if request.method == "GET":
        #this is supposed to be the result from the payment service, whether success, error, or cancel. (Step 3 in bank api)
        #print(game_name)
        root = request.GET
        pid = root['pid']
        ref = root['ref']
        result = root['result']
        checksum_from_url = root['checksum']

        #The checksum is calculated from pid, sid, amount, and your secret key. The string is formed like this:
        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secret_key)

        # checksumstr is the string concatenated above
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        if checksum != checksum_from_url:
            print('la ya 7abeebi')
            response = "No Habeebi, don't even try that"
            return render(request, "buyGameResult.html", {'response' : response})
            #return HttpResponseRedirect('/game/'+game_name+'/')
            #raise Http404

        else:
            if( result == 'error'):
                #'pass' if you comment the rest and don't want to do anything here
                response = "Oops.. Something went wrong with the payment. Don't worry, your money is still in your pocket, though."
                return render(request, "buyGameResult.html", {'response' : response})

            if( result == 'success'):
                game= Game.objects.get(name=game_name) #query the game from the Game object
                try:
                    transaction = Transaction.objects.get(user = request.user, game = game, status = "ongoing", pid = pid)
                except Transaction.DoesNotExist:
                    transaction = None
                if transaction != None:
                    transaction.status = "completed"
                    transaction.timestamp = datetime.now()
                    transaction.save() #save the transactio to the database

                    return HttpResponseRedirect('/game/'+game_name+'/')
                else:
                    return HttpResponseRedirect('/')


            if( result == 'cancel'):
                game= Game.objects.get(name=game_name) #query the game from the Game object
                try:
                    transaction = Transaction.objects.get(user = request.user, game = game, status = "ongoing", pid = pid)
                except Transaction.DoesNotExist:
                    transaction = None
                if transaction != None:
                    transaction.status = "canceled"
                    transaction.save()
                return HttpResponseRedirect('/game/'+game_name+'/')
    else:
        return HttpResponse('Not authorised')

#Main view where user plays game
@login_required(login_url='/login/')
def game(request, game_name):
    try:
        game = Game.objects.get(name=game_name)
        gameURL = request.build_absolute_uri(reverse("game", args = (game_name, )))
        #gameURL = "google.com"

        # TODO: What if highscores dont exist
        scores = Scores.objects.all().filter(game=game).order_by("-score")
        #check if user has bought the game a.k.a. has access to it
        if Transaction.objects.filter(game=game, user=request.user, status='completed').exists():
            gameBought = True
        else:
            gameBought = False
            # If the user uploadded game, let him play it
            if DeveloperGame.objects.filter(user=request.user, game=game).exists():
                gameBought = True
        comments = Comment.objects.all().filter(game=game).order_by("-created")

        # userComments holds information about comments and userProfile of users who made comments
        userComments = []
        for comment in comments:
            userProfile = UserProfile.objects.filter(user=comment.user).first()
            userComments.append([comment,userProfile])
        #print(userComments)
    # In case game does not exist, display 404
    except Game.DoesNotExist:
        raise Http404()
    return render(request, "game.html", {"game" : game, "scores" : scores, "gameBought" : gameBought, "userComments": userComments, "gameURL" : gameURL})

@login_required(login_url='/login/')
@csrf_protect
def saveScore(request):
	# Only available as ajax post call
	if request.method == "POST" and request.is_ajax():
		#create python dictionary from data sent through post request
		#root = dict(request.POST.iterlists())	#python2.7
		root = dict(request.POST.lists()) #python3
		user = request.user
		#extract data from root
		game = Game.objects.get(pk = root['game'][0])
		score = root['score'][0]
		# Do not save dupicates of Scores (same score from same user for same game)
		if not Scores.objects.filter(user=user, game=game, score=score).exists():
			data = Scores(user=user, game=game, score=score)
			data.save()
		return HttpResponse("Score Saved")
	else:
		return HttpResponse("Not authorized.")


@login_required(login_url='/login/')
@csrf_protect
def saveGame(request):
    if request.method == "POST" and request.is_ajax():
        #create python dictionary from data sent through post request
        root = dict(request.POST)

        user = request.user
        #extract data from root
        game = Game.objects.get(pk = root['game'][0])
        score = root['score'][0]
        #If user has some items. If 'items' array is sent through POST
        if 'items[]' in root:
            items = root['items[]']
        else:
            items = []
        # If USER already has saved games for current game, just update it
        # Save space in the database with this
        if Gameplay.objects.filter(user=user, game=game).exists():
            Gameplay.objects.filter(user=user, game=game).update(score=score)
        #If not, create new save game
        else:
            data = Gameplay(user=user, game=game, score=score)
            data.save()

        # no need to check if gameplay exists, we created it in previous step
        # if it hasnt existed before
        gameplay = Gameplay.objects.get(user=user, game=game)
        # Delete previous items from same Gameplay
        PlayerItem.objects.filter(gameplay=gameplay).delete()
        for item in items:
            data = PlayerItem(gameplay=gameplay, itemName = item)
            data.save()
        return HttpResponse("Game Saved!")
    else:
        return HttpResponse("Not authorized.")

@login_required(login_url='/login/')
@csrf_protect
def loadGame(request):
    if request.method == "POST" and request.is_ajax():
        #create python dictionary from data sent through post request
        #root = dict(request.POST.iterlists())  #python2.7

        root = dict(request.POST)
        user = request.user
        game = Game.objects.get(pk = root['game'][0])

        # If previously saved games exists, load them
        if Gameplay.objects.filter(user=user, game=game).exists():
            gameplay = Gameplay.objects.get(user=user, game=game)
            # Prepare response to send to game
            response = {'messageType' : 'LOAD', 'gameState' : {'playerItems' : [], 'score' : gameplay.score}}
            # Fill items array one item a time
            # Same as PlayerItem.objects.all().filter(gameplay=gameplay)
            for item in PlayerItem.objects.filter(gameplay=gameplay):
                response['gameState']['playerItems'].append(item.itemName)
            return JsonResponse(response)
        else:
            return HttpResponse("No saved games to load.")
    else:
        return HttpResponse("Not authorized.")

@login_required(login_url='/login/')
@csrf_protect
def addComment(request,game_name):
	if request.method == "POST" and request.is_ajax():
		#create python dictionary from data sent through post request
		#root = dict(request.POST.iterlists()) 	#python2.7
		root = dict(request.POST.lists())	#python3
		if (str(root["comment"][0]) != ""):
			comment = Comment(user=request.user,
								game=Game.objects.get(name=game_name),
								commentText=str(root["comment"][0]))
			comment.save()
			return HttpResponse("Success")
		else:
			return HttpResponse("Your comment is empty")
	else:
		return HttpResponse("Not authorized.")

@csrf_protect
def register(request):
    if request.method == 'POST':
        # Render the form from data sent through POST
        form = RegistrationForm(request.POST)
        # If the form is valid, validity of a form is specified in files.py
        # where the form is defined
        if form.is_valid():
            #create user
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            # Create our custom user profile
            userProfile = UserProfile(user=user, isDeveloper=form.cleaned_data['isDeveloper'])
            userProfile.save()

            #Authenticate user
            username=request.POST['username']
            password=request.POST['password1']
            user=authenticate(username=username,password=password)

            #Make it inactive until he/she activates account via email
            user.is_active=False
            user.save()

            #prepare data for sending email to user
            id=user.id
            email=user.email
            url = request.build_absolute_uri(reverse('activation', args=(id, )))
            #Custom function that prepares and sends email to user
            send_email(email,url)

            # redirect to success page
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    return render(request,
    'registration/register.html', {'form' : form}
    )
#after registration user is redirected here, getting further instructions
def register_success(request):
    return render(request,
    'registration/success.html', {}
    )

# After user clicks link provided in email he is redirected here
def activation(request,id):
    #Change user status to active and login him/her
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        raise Http404()
    user.is_active=True
    user.save()
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return HttpResponseRedirect('/')

# Not a view, just a function that sends email to user for validation
def send_email(toaddr,url):
    # Body of email
    text = "Hi!\n To finish registration, follow this link to activate your account:%s" %(url)
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    msg = MIMEMultipart('alternative')
    msg.attach(part1)
    #Subject of email
    subject="Activate your account at WSD Awsome Project"
    msg="""\From: %s\nTo: %s\nSubject: %s\n\n%s""" %(fromaddr,toaddr,subject,msg.as_string())
    #Open server, authenticate and send email
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr,[toaddr],msg)
    server.quit()


def upload(request):
	context = dict( backend_form = UploadPhoto())
	if request.method == 'POST':
		form = UploadPhoto(request.POST, request.FILES)
		print("form instance: ", form.instance)
		context['posted'] = form.instance
		if form.is_valid():
			form.save()

	return render(request, 'test.html', context)

# TODO: @sharbel, As a developer, they should be able to: see list of game sales
@login_required(login_url='/login/')
def manageUploadedGames(request):
    # This should be the view for the developer to see all the games she created, who bought their games,
	# edit game details, and request to remove their uploaded games.
	developerProfile = UserProfile.objects.get(user=request.user)
	if developerProfile.isDeveloper:
		DeveloperGames = DeveloperGame.objects.all().filter(user=request.user) #Querying from the developer game table all objects whose user matches request.user
		games = []
		numberOfPurchasesList = []
		for developerGame in DeveloperGames:
			#put the games in a list
			games.append(developerGame.game) # developerGame is an instance (a row in the database table) of DeveloperGames
			#print(games)

			Purchases = Transaction.objects.all().filter(game=developerGame.game, status='completed') 	# Querying from the Transaction table the all transactions objects
																					# with games matching the chosen game
			numberOfPurchasesList.append(len(Purchases))

		gamePurchases = zip(games, numberOfPurchasesList)
		#gamePurchases.append
	else:
		return HttpResponseRedirect('/') #in case address is typed, this redirects them to home (secure stuff)
	#games = DeveloperGame.objects.get(user=request.user, game = request.game) #QUERY the games by this developer (.get or .filter?)

	PurchasedGames = Transaction.objects.all().filter(user=request.user, status='completed')
	purchasedGames = []
	purchasedWhen = []
	for boughtGame in PurchasedGames:
		purchasedGames.append(boughtGame.game.name)
		purchasedWhen.append(boughtGame.timestamp)

	boughtGames = zip(purchasedGames, purchasedWhen)

	return render(request, "manageUploadedGames.html", {"developerProfile": developerProfile, "gamePurchases": gamePurchases, "boughtGames": boughtGames})

# TODO: @sharbel, When a game is clicked in manageUploadedGames,
#you can Edit its details, request to change the price (or just lock the price), and view the game sales
@login_required(login_url='/login/')
@csrf_protect
def manageGame(request, game_name):
	messageOfUpdate=""
	developerProfile = UserProfile.objects.get(user=request.user)
	if developerProfile.isDeveloper:
		try:
			#Import all editable game details as a form.
			game = Game.objects.get(name = game_name)
			context = dict( backend_form = UpdateGameForm())
			if request.method == 'POST':
				# Create a form instance from POST data.
				form = UpdateGameForm(request.POST, request.FILES, instance = game)

				#context['posted'] = form.instance
				success = False

				if request.POST.get("updateGame"):

					if form.is_valid():
						# Create, but don't save the new author instance.
						updatedGame = form.save(commit=False)   #This enables editng the data in some way before actually saving it to the
																#  database. For example: updatedGame.description = "Forced Description no matter what you write"
						updatedGame.save()
						success = True
						messageOfUpdate = "Game Successfully Updated"
					print("updateGame")

				elif request.POST.get("deleteGame"):
					#Implement Remove Game (Delete from database). Should prompt some confirmation message.
					print("deleteGame")
					print(game.name)
					game.delete() #game is an instance.. game = Game.objects.get(name = game_name)
					return HttpResponseRedirect('/myProfile/')

			else:
				form = UpdateGameForm(initial={"url": game.url, "price": game.price, "description": game.description})
				success = False

			#View game sales in a list of buyer names and timestamps
			Purchases = Transaction.objects.all().filter(game=game, status='completed') #Querying from the transactions game table all objects whose game matches game_name
			buyers = []
			timestamps = []
			counts = []
			i = 0
			for purchase in Purchases:
				buyers.append(purchase.user) #purchase is an instance (a row in the database) of Purchases
				timestamps.append(purchase.timestamp)
				i += 1
				counts.append(i)

			transactions = zip(buyers, timestamps, counts)
			game = Game.objects.get(name = game_name)

		except Game.DoesNotExist:
			raise Http404()

	else:
		return HttpResponseRedirect('/') #in case address is typed, this redirects them to home (secure stuff)

	return render(request, "manageGame.html", {"game": game, "form" : form, "success" : success, "context" : context, "transactions": transactions,
					"messageOfUpdate": messageOfUpdate})
